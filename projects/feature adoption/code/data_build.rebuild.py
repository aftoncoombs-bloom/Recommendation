import pandas as pd
import numpy as np
import pickle as pkl

import sys, requests, json
sys.path.insert(1, '../../../scripts/')
from s3_support import *

orgs = get_dataframe_from_file("qgiv-stats-data", "org.exp.csv")
forms = get_dataframe_from_file("qgiv-stats-data", "form.exp.csv")
org_transaction_count = redshift_query_read("select org, count(id) as count from transactions where status='A' group by org")

'''
DATA UPDATES
'''
# update adoption data as foundation of data build
URL = "https://secure.qgiv.com/admin/qgivadmin/statistics/export_feature_adoption.php"
KEY = "DSQR59VwyFhw21PKDF4K"

rsp = requests.post(URL, data={'key': KEY})
data = json.loads(rsp.text)

def get_org_for_form(form):
    if form != 0 and form is not None and len(forms[forms['id']==int(form)]) > 0:
        return forms[forms['id']==int(form)]['org'].iloc[0]
    else:
        return 0
    
normalized_agg_data = {
    'implementation_data': {}, 
    'bidirectional_adoption_data': {},
    'institutional_adoption_data': {}
}
for data_key in ['implementation_data', 'bidirectional_adoption_data']:
    for element_key in data[0][data_key]:
        if data[0][data_key][element_key] is None or data[0][data_key][element_key] == '0' or element_key == 'merchant_accounts' or element_key == 'events_promo':
            continue
        elif len(data[0][data_key][element_key]) == 0:
            continue
        elif type(data[0][data_key][element_key][0]) == str:
            # list of ID's
            if 'org' in element_key:
                cols = ['org']
            else:
                cols = ['form']
            df = pd.DataFrame(data[0][data_key][element_key], columns=cols)
        else:
            df = pd.DataFrame(data[0][data_key][element_key])
            
        # add org if we don't yet have it
        if 'org' not in df.columns:
            if 'form' not in df.columns:
                continue
            df['org'] = df['form'].apply(get_org_for_form)
        
        # normalize count column name
        for c in df.columns:
            if 'count' in c:
                df['count'] = df[c]
                df.drop(c, axis=1, inplace=True)
        
        # type casting
        df['org'] = df['org'].fillna(0).astype(int)
        if 'count' in df.columns:
            df['count'] = df['count'].fillna(0).astype(int)
        
        data_entry = {
            'adoption_rate': float(len(df['org'].unique())) / float(len(orgs)),
            'meta': {
                'count_orgs': len(df['org'].unique())
            }
        }
        
        if 'form' in df.columns:
            data_entry['meta']['count_forms'] = len(df['form'].unique())
            if 'count' in df.columns:
                data_entry['meta']['average_count_per_form'] = df['count'].mean()
                data_entry['meta']['average_count_per_org'] = df[df['org']!=0].groupby("org")['count'].sum().mean()
        else:
            if 'count' in df.columns:
                data_entry['meta']['average_count_per_org'] = df['count'].mean()
            
        normalized_agg_data[data_key][element_key] = data_entry
        
        if data_key == 'bidirectional_adoption_data' and 'count' in df.columns:
            df_orgs = df[df['org']!=0].groupby("org")['count'].sum().reset_index()
            df_orgs = df_orgs[df_orgs['org'].isin(org_transaction_count['org'].tolist())]
            
            df_orgs['len_trans_org'] = df_orgs['org'].apply(lambda x: org_transaction_count[org_transaction_count['org']==x]['count'].iloc[0])
            df_orgs['perc_all_trans'] = df_orgs['count'] / df_orgs['len_trans_org']
            
            normalized_agg_data['institutional_adoption_data'][element_key] = {
                'adoption_rate': float(len(df_orgs[df_orgs['perc_all_trans']>0.15])) / float(len(orgs)),
                'meta': {
                    'count_orgs': len(df_orgs[df_orgs['perc_all_trans']>0.15])
                }
            }
            
for k in normalized_agg_data.keys():
    if 'events_donatiosn' in normalized_agg_data[k]:
        normalized_agg_data[k]['events_donations'] = normalized_agg_data[k]['events_donatiosn']
        
        
'''
UPDATE TABLE DATA
'''
# update table data
TABLES = ['org', 'form', 'embed', 'thermometers', 'facebookfundraiser', 'givi', 
          'badges', 'emailcampaign', 'smscampaign', 'smspledgereminders', 'lists']

def fetch_table(table):
    url = 'https://secure.qgiv.com/admin/qgivadmin/statistics/export_tables.php'
    payload = {'key': 'DSQR59VwyFhw21PKDF4K', 'table': table}

    rsp = requests.post(url, data=payload)
    json_data = json.loads(rsp.content)

    return json_data[0]

for table in TABLES:
    # print("fetching {}".format(table))
    data = fetch_table(table)
    
    if table != 'facebookfundraiser': 
        df = pd.DataFrame(data)

        if len(df) > 0:
            filename = "{}.exp.csv".format(table)
            save_dataframe_to_file("qgiv-stats-data", filename, df, print_output=False)
    else:
        fundraisers = pd.DataFrame(data['facebook_fundraisers'])
        settings = pd.DataFrame(data['social_settings'])

        if len(fundraisers) > 0:
            filename = "facebook_fundraisers.exp.csv"
            save_dataframe_to_file("qgiv-stats-data", filename, fundraisers, print_output=False)

            filename = "social_settings.exp.csv"
            save_dataframe_to_file("qgiv-stats-data", filename, settings, print_output=False)
            
            
'''
UPDATE TRANSACTIONS
'''
q = "select * from transactions where status='A'"
trans = redshift_query_read(q)

trans_src_form = trans.groupby(['form', 'source'])['id'].count().reset_index().pivot(index='form', columns='source', values='id').reset_index().fillna(0)
trans_src_org = trans.groupby(['org', 'source'])['id'].count().reset_index().pivot(index='org', columns='source', values='id').reset_index().fillna(0)

len_forms = len(trans['form'].unique())
len_orgs = len(trans['org'].unique())

all_sources = list(trans['source'].unique())

trans_src_form['all'] = trans_src_form[all_sources].sum(axis=1)
trans_src_org['all'] = trans_src_org[all_sources].sum(axis=1)
for source in all_sources:
    trans_src_form["{}_perc".format(source)] = (trans_src_form[source] / trans_src_form['all']) * 100
    trans_src_org["{}_perc".format(source)] = (trans_src_org[source] / trans_src_org['all']) * 100
trans_src_form.head(3)

source_data = {}

for source in all_sources:
    trans_msk = (trans['source']==source)
    mean_trans_amt = trans[trans_msk]['amount'].mean()
    
    source_data[source] = {
        'average_percentage_per_form': trans_src_form["{}_perc".format(source)].mean(),
        'average_count_per_form': trans_src_form[source].mean(),
        'average_percentage_per_org': trans_src_org["{}_perc".format(source)].mean(),
        'average_count_per_org': trans_src_org[source].mean(),
        'mean_transaction_value': mean_trans_amt,
        'bidirectional_adoption_rate': float(len(trans[trans_msk]['org'].unique())) / float(len_orgs),
        'institutional_adoption_rate': float(len(trans_src_org[trans_src_org["{}_perc".format(source)]>0.15]['org'].unique().tolist())) / float(len_orgs)
    }
    for threshold in [0., 10., 25., 50., 75., 90.]:
        source_data[source]['forms_gt_{}'.format(threshold)] = len(trans_src_form[trans_src_form["{}_perc".format(source)]>threshold])
        source_data[source]['orgs_gt_{}'.format(threshold)] = len(trans_src_org[trans_src_org["{}_perc".format(source)]>threshold])
        
# adding store purchases
trans['is_purchase'] = trans['purchases_count']>0

purch_forms = trans.groupby(['form', 'is_purchase'])['id'].count().reset_index().pivot(index='form', columns='is_purchase', values='id').reset_index().fillna(0)
purch_forms['perc'] = (purch_forms[True] / (purch_forms[True] + purch_forms[False])) * 100.
purch_orgs = trans.groupby(['org', 'is_purchase'])['id'].count().reset_index().pivot(index='org', columns='is_purchase', values='id').reset_index().fillna(0)
purch_orgs['perc'] = (purch_orgs[True] / (purch_orgs[True] + purch_orgs[False])) * 100.

source_data['store_purchases'] = {
    'average_percentage_per_form': purch_forms['perc'].mean(),
    'average_count_per_form': purch_forms[True].mean(),
    'average_percentage_per_org': purch_orgs['perc'].mean(),
    'average_count_per_org': purch_orgs[True].mean(),
    'mean_transaction_value': trans[trans['purchases_count']>0]['purchases_amt'].mean(),
    'bidirectional_adoption_rate': float(len(purch_orgs[purch_orgs[True]>0.]['org'].unique())) / float(len_orgs),
    'institutional_adoption_rate': float(len(purch_orgs[purch_orgs['perc']>0.15]['org'].unique().tolist())) / float(len_orgs)
}
for threshold in [0., 10., 25., 50., 75., 90.]:
    source_data['store_purchases']['forms_gt_{}'.format(threshold)] = len(purch_forms[purch_forms['perc']>threshold])
    source_data['store_purchases']['orgs_gt_{}'.format(threshold)] = len(purch_orgs[purch_orgs['perc']>threshold])
    
# adding recurring
trans['is_recurring'] = trans['recurring']!=0

rec_forms = trans.groupby(['form', 'is_recurring'])['id'].count().reset_index().pivot(index='form', columns='is_recurring', values='id').reset_index().fillna(0)
rec_forms['perc'] = (rec_forms[True] / (rec_forms[True] + rec_forms[False])) * 100.
rec_orgs = trans.groupby(['org', 'is_recurring'])['id'].count().reset_index().pivot(index='org', columns='is_recurring', values='id').reset_index().fillna(0)
rec_orgs['perc'] = (rec_orgs[True] / rec_orgs[True] + rec_orgs[False]) * 100.

source_data['recurring'] = {
    'average_percentage_per_form': rec_forms['perc'].mean(),
    'average_count_per_form': rec_forms[True].mean(),
    'average_percentage_per_org': rec_orgs['perc'].mean(),
    'average_count_per_org': rec_orgs[True].mean(),
    'mean_transaction_value': trans[trans['is_recurring'].fillna(False)]['amount'].mean(),
    'bidirectional_adoption_rate': float(len(rec_orgs[rec_orgs[True]>0.]['org'].unique())) / float(len_orgs),
    'institutional_adoption_rate': float(len(rec_orgs[rec_orgs['perc']>0.15]['org'].unique().tolist())) / float(len_orgs)
}
for threshold in [0., 10., 25., 50., 75., 90.]:
    source_data['recurring']['forms_gt_{}'.format(threshold)] = len(rec_forms[rec_forms['perc']>threshold])
    source_data['recurring']['orgs_gt_{}'.format(threshold)] = len(rec_orgs[rec_orgs['perc']>threshold])
    
# adding P2P registrations
trans['is_registration'] = trans['registrations_count']>0

reg_forms = trans.groupby(['form', 'is_registration'])['id'].count().reset_index().pivot(index='form', columns='is_registration', values='id').reset_index().fillna(0)
reg_forms['perc'] = (reg_forms[True] / (reg_forms[True] + reg_forms[False])) * 100.
reg_orgs = trans.groupby(['org', 'is_registration'])['id'].count().reset_index().pivot(index='org', columns='is_registration', values='id').reset_index().fillna(0)
reg_orgs['perc'] = (reg_orgs[True] / (reg_orgs[True] + reg_orgs[False])) * 100.

source_data['p2p_registrations'] = {
    'average_percentage_per_form': reg_forms['perc'].mean(),
    'average_count_per_form': reg_forms[True].mean(),
    'average_percentage_per_org': reg_orgs['perc'].mean(),
    'average_count_per_org': reg_orgs[True].mean(),
    'mean_transaction_value': trans[trans['registrations_count']>0]['registrations_amt'].mean(),
    'bidirectional_adoption_rate': float(len(reg_orgs[reg_orgs[True]>0.]['org'].unique())) / float(len_orgs),
    'institutional_adoption_rate': float(len(reg_orgs[reg_orgs['perc']>0.15]['org'].unique().tolist())) / float(len_orgs)
}
for threshold in [0., 10., 25., 50., 75., 90.]:
    source_data['p2p_registrations']['forms_gt_{}'.format(threshold)] = len(reg_forms[reg_forms['perc']>threshold])
    source_data['p2p_registrations']['orgs_gt_{}'.format(threshold)] = len(reg_orgs[reg_orgs['perc']>threshold])
    
    
'''
INTEGRATE TABLE DATA INTO ADOPTION EXPORT DATA
'''
# load table data
table_agg_files = list_files("qgiv-stats-data", search_key=".agg.", print_output=False)

table_data = {}
for f in table_agg_files:
    table_data[f.replace(".agg.csv", "")] = get_dataframe_from_file("qgiv-stats-data", f)
    
refined_table_data = {}
for e in table_data.keys():
    cols = table_data[e].columns
    data = {
        'adoption_rate': 0,
        'meta': {}
    }
    
    if 'org' in cols and 'form' in cols:
        # org & form available
        data['meta']['average_count_per_org'] = table_data[e].groupby('org')['count'].sum().mean()
        data['meta']['average_count_per_form'] = table_data[e]['count'].mean()
        data['meta']['count_forms'] = len(table_data[e])
        data['meta']['count_orgs'] = len(table_data[e]['org'].unique())
        data['meta']['adoption_rate_forms'] = float(data['meta']['count_forms']) / float(len(forms))
        
        data['adoption_rate'] = float(data['meta']['count_orgs']) / float(len(orgs))
    elif 'org' in cols:
        # only org level available
        data['meta']['average_count_per_org'] = table_data[e]['count'].mean()
        data['meta']['count_orgs'] = len(table_data[e])
        
        data['adoption_rate'] = float(data['meta']['count_orgs']) / float(len(orgs))
    elif 'form' in cols:
        # only form level available
        data['meta']['average_count_per_form'] = table_data[e]['count'].mean()
        data['meta']['count_forms'] = len(table_data[e])
        
        data['adoption_rate'] = float(data['meta']['count_forms']) / float(len(forms))
        
    refined_table_data[e] = data
    
for table_key in refined_table_data.keys():
    normalized_agg_data['implementation_data'][table_key] = refined_table_data[table_key]
    
'''
INTEGRATE TRANSACTION DATA
'''
for source_key in source_data.keys():
    bidirectional_adoption_rate = source_data[source_key]['bidirectional_adoption_rate']
    institutional_adoption_rate = source_data[source_key]['institutional_adoption_rate']

    del(source_data[source_key]['institutional_adoption_rate'])
    del(source_data[source_key]['bidirectional_adoption_rate'])

    normalized_agg_data['bidirectional_adoption_data'][source_key] = {
        'adoption_rate': bidirectional_adoption_rate,
        'meta': source_data[source_key]
    }
    normalized_agg_data['institutional_adoption_data'][source_key] = {
        'adoption_rate': institutional_adoption_rate
    }

normalized_agg_data['meta'] = {
    'len_forms': len_forms,
    'len_orgs': len_orgs
}

pkl.dump(normalized_agg_data, open("adoption_data.pkl", "wb"))

'''
RESTRUCTURING
'''