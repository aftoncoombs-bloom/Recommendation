import pandas as pd
import datetime, os

import sys, os, requests, json
sys.path.insert(1, '../../../scripts/')
from s3_support import *

import warnings
warnings.filterwarnings('ignore')

'''
Data points needed:
    - Orgs with only P2P forms and no year round forms
    - Orgs relying upon SMS for the majority of their transactin volume
    - Orgs relying upon events for the majority of their transaction volume
    - Orgs not using recurring
    - Orgs not using donor logins

All data points can be derived from transactions history and Qgiv settings so we need 2 datasets.

@TODO
    - limit filters to pay attention to the last 3 months (?) to make target organizations more relevant
'''

tips = [
    "Organizations with P2P forms raise more than 25 times more when they also use year round forms than those only using P2P",
    "Of organizations utilizing SMS, those which do not rely upon SMS for the majority of their fundraising raise more than 172 times more than those that do rely upon SMS for the majority of their fundraising",
    "Organizations that rely upon events for less than 50% of their funds raised will generate about 50% more in funds than those that rely upon events for more than 50% of their funds raised",
    "Donors give 2.4 times the amount in recurring donations than one time",
    "Donor logins can lead to up to 4 times the donations (by count, not volume) per donor",
    "Organizations active in CMS grow 25% faster on average in volume and 45% faster on average in transaction counts than those that are not",
    "Organizations with widgets grow 21.5% faster on average in volume and 153% faster on average in transaction counts than those without",
    "Organizations with logins within the last 3 months grow 7.5% faster on average in volume and 48.7% faster on average in transaction counts than those without"
]

print("Load data")
q = '''select
            org,
            source,
            date_trunc('month', date) as month,
            sum(amount) as amount,
            sum(donations_amt) as donations_amt,
            sum(events_amt) as events_amt,
            sum(purchases_amt) as purchases_amt,
            sum(registrations_amt) as registrations_amt,
            sum(case when recurring!=0 then amount else 0 end) as recurring_amt
        from transactions
            where status='A'
            group by org, date_trunc('month', date), source'''
df_trans = redshift_query_read(q)

print("\tprepping analytics features - getting donor logins activation setting")
df_dl_trans = get_dataframe_from_file("qgiv-stats-data", "dl_transactions.csv")
org_dl_count = df_dl_trans.groupby('org')['count'].sum().reset_index()

print("\tprepping segment features")
print("\t\trecent logins")
q = '''select
            distinct(org) as org
        from users
        where
            lastlogin >= add_months(current_date, -3);'''
org_logins = redshift_query_read(q, schema="production")
print("\t\twith widgets")
q = '''select distinct entity as org from embed'''
org_widgets = redshift_query_read(q, schema='production')['org'].tolist()

print("\t\tactive in CMS")
print("\t\t\t- IGNORE DATA POINT, STILL NEEDS UPDATING")
q = '''select
            distinct(users.org) as org
        from saved_page
            left join users on saved_page.uuid=users.uuid'''
org_cms_saves = redshift_query_read(q, schema='secure')['org'].tolist()

print("\tprepping trans features")
print("\t\tdate handling")
df_trans['date'] = pd.to_datetime(df_trans['month'])

print("\t\tcalculating transaction source & type percentages")
trans_types = ['amount', 'donations_amt', 'events_amt', 'purchases_amt', 'registrations_amt', 'recurring_amt']
trans_type_agg = df_trans.groupby(['org', 'month'])[trans_types].sum().reset_index()
for col in trans_types:
    if col != "amount":
        trans_type_agg["{}_perc".format(col)] = trans_type_agg[col] / trans_type_agg['amount']

trans_source_agg = df_trans[['org', 'source', 'amount']].groupby(['org', 'source'])['amount'].sum().reset_index().pivot(index='org', columns='source', values='amount').reset_index().fillna(0.)
sources = ['don_form', 'fb', 'givi', 'kiosk', 'mobile', 'mobilevt', 'p2p', 'sms', 'vt']
trans_source_agg['total'] = trans_source_agg[sources].sum(axis=1)
for s in sources:
    trans_source_agg[s+'_perc'] = trans_source_agg[s] / trans_source_agg['total']

print("Find designated groups")
print("\tlow donor logins")
orgs_low_dl = org_dl_count[org_dl_count['count']<10]['org'].tolist()

print("\tlow transaction source rates")
# recurring
orgs_low_recurring = trans_type_agg[trans_type_agg["recurring_amt_perc"]<.1]['org'].tolist()
# events
orgs_high_events = trans_type_agg[trans_type_agg["events_amt_perc"]>.5]['org'].tolist()
# sms
orgs_high_sms = trans_source_agg[trans_source_agg['sms_perc']>.5]['org'].tolist()
# p2p
orgs_only_p2p = trans_source_agg[trans_source_agg['p2p_perc']>.9]['org'].tolist()

print("Output list of orgs with groups")
unique_orgs = list(set(orgs_low_recurring + orgs_high_events + orgs_high_sms + orgs_only_p2p + orgs_low_dl))
org_list = pd.DataFrame(unique_orgs, columns=['org'])
org_list['low_recurring'] = org_list['org'].apply(lambda x: True if x in orgs_low_recurring else False)
org_list['high_events'] = org_list['org'].apply(lambda x: True if x in orgs_high_events else False)
org_list['high_sms'] = org_list['org'].apply(lambda x: True if x in orgs_high_sms else False)
org_list['only_p2p'] = org_list['org'].apply(lambda x: True if x in orgs_only_p2p else False)
org_list['low_dl'] = org_list['org'].apply(lambda x: True if x in orgs_low_dl else False)
org_list['total'] = org_list[['low_recurring', 'low_dl', 'high_events', 'high_sms', 'only_p2p']].sum(axis=1)

# segment data points
org_list['not_cms_active'] = ~org_list['org'].isin(org_cms_saves)
org_list['not_using_widgets'] = ~org_list['org'].isin(org_widgets)
org_list['no_recent_logins'] = ~org_list['org'].isin(org_logins)

org_list.sort_values('total', ascending=False, inplace=True)

# remove previously recommended orgs
try:
    df_prior_preds = get_dataframe_from_file("qgiv-stats-data", "preds.growth.csv")
    
    df_prior_preds['org'] = df_prior_preds['org'].astype(int)
    df_prior_preds['date'] = pd.to_datetime(df_prior_preds['date'])
    six_months_ago = datetime.datetime.today() - datetime.timedelta(6*365/12)
    
    prior_preds = df_prior_preds[df_prior_preds['date']>=six_months_ago]['org'].tolist()
    print("\t{} prior preds found".format(len(prior_preds)))
except Exception as e:
    print("\tprior preds not found")
    print(e)
    df_prior_preds = None
    prior_preds = []

orgs = redshift_query_read("select id, status from organization", schema="production")
active_orgs = orgs[orgs['status']==1]['id'].tolist()
org_names = get_dataframe_from_file("qgiv-stats-data", "organizations.names.csv")
org_names['id'] = org_names['id'].fillna(0).astype(int)

# filter prior preds & not active orgs from preds
these_preds = org_list[(~org_list['org'].astype(int).isin(prior_preds))&(org_list['org'].isin(active_orgs))].head(20).copy()
these_preds['date'] = datetime.datetime.today()

# store to prior preds
if df_prior_preds is not None:
    save_dataframe_to_file("qgiv-stats-data", "preds.growth.csv", df_prior_preds.append(these_preds))
else:
    save_dataframe_to_file("qgiv-stats-data", "preds.growth.csv", these_preds)

# print report
these_preds.drop('date', axis=1, inplace=True)
these_preds['name'] = these_preds['org'].apply(lambda x: org_names[org_names['id']==int(x)]['org_name'].iloc[0] if len(org_names[org_names['id']==x]) > 0 else None)

pd.set_option('display.max_columns', 50)

print("-"*40)
print("\tIGNORE CMS RECOMMENDATIONS")
print("-"*40)

print(these_preds)


