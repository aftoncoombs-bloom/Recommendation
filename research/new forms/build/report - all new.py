import sys, datetime
sys.path.append("../../scripts/")
from s3_support import *

import pandas as pd
import numpy as np


compare_sets = []
START_DATE = '2019-10-01'


print("loading data")
print("\ttraffic")
q = '''select
            date,
            form,
            devicecategory,
            views as pageviews,
            bounces
        from googleanalytics_traffic
        where 
            qgiv_frontend=1 and
            date >= '{}' '''.format(START_DATE)
traffic = redshift_query_read(q, schema='public')

traffic['form'] = traffic['form'].astype(int)

print("\ttransactions")
q = '''select 
            form,
            date,
            amount,
            source,
            useragent
        from transactions
        where
            status='A' and
            (source='don_form' or source='mobile') and
            recurring=0 and
            date >= '{}'
        '''.format(START_DATE)
trans = redshift_query_read(q, schema='public')
trans['useragent'].fillna('', inplace=True)
trans['is_recurring'] = False

q = '''select 
            form,
            date,
            recurring,
            amount,
            source,
            useragent
        from transactions
        where
            status='A' and
            (source='don_form' or source='mobile') and
            recurring!=0 and
            date >= '{}'
        order by date asc
        '''.format(START_DATE)
rec = redshift_query_read(q, schema='public')
rec = rec.groupby('recurring').first().reset_index()
rec['useragent'].fillna('', inplace=True)
rec['is_recurring'] = True

trans = trans.append(rec)

# flagging mobile & desktop
trans['is_mobile'] = (trans['useragent'].str.contains('iPhone').fillna(False))|(trans['useragent'].str.contains('iPad').fillna(False))|(trans['useragent'].str.contains('Android').fillna(False))
trans['is_desktop'] = (trans['useragent'].str.contains('Macintosh').fillna(False))|(trans['useragent'].str.contains('Windows').fillna(False))|(trans['useragent'].str.contains('CrOS').fillna(False))

# defaulting to source for ambiguous/missing useragent
trans_assigned = trans[trans['is_mobile']|trans['is_desktop']].copy()
trans_unassigned = trans[~trans['is_mobile']&~trans['is_desktop']].copy()
trans_unassigned['is_mobile'] = trans_unassigned['source']=='mobile'
trans_unassigned['is_desktop'] = trans_unassigned['source']=='don_form'
trans = trans_assigned.append(trans_unassigned)

trans = trans[trans['form'].isin(traffic['form'].unique().tolist())]

print("\tprocess and merge traffic & transactions")
# calculate conversions
daily_trans = trans.groupby(['form', 'date', 'is_recurring'])['amount'].agg({'count', 'sum'}).reset_index()
daily_trans['trans_count'] = daily_trans['count']
daily_trans['trans_vol'] = daily_trans['sum']
daily_trans.drop(['count', 'sum'], axis=1, inplace=True)

daily_trans_pvt = daily_trans.pivot(index=['form', 'date'], columns='is_recurring', values=['trans_count', 'trans_vol']).reset_index()
daily_trans_pvt.columns = ['form', 'date', 'trans_count_onetime', 'trans_count_recurring', 'trans_vol_onetime', 'trans_vol_recurring']
daily_trans_pvt.fillna(0, inplace=True)

dailies = daily_trans_pvt.merge(traffic.groupby(['date', 'form'])[['pageviews', 'bounces']].sum().reset_index(), on=['date', 'form'], how='outer')
dailies.fillna(0, inplace=True)

dailies['conversion'] = (dailies['trans_count_onetime'] + dailies['trans_count_recurring']) / dailies['pageviews']
dailies['conversion_onetime'] = dailies['trans_count_onetime'] / dailies['pageviews']
dailies['conversion_recurring'] = dailies['trans_count_recurring'] / dailies['pageviews']

print("isolating data sets")
bucket = "qgiv-stats-data"
new_form_template_list = "form_download new template.csv"
new_forms = get_dataframe_from_file(bucket, new_form_template_list)
new_forms_ids = new_forms[new_forms['Status']=='active']['Form ID'].unique().tolist()
compare_sets = [
    {
        'title': 'All',
        'data': dailies
    },
    {
        'title': 'New Forms',
        'data': dailies[dailies['form'].isin(new_forms_ids)]
    },
    {
        'title': 'Old Forms',
        'data': dailies[~dailies['form'].isin(new_forms_ids)]
    }
]

print("report")
print("-"*40)
print()

def report(df):
    # recurring frequency?
    df.replace(np.inf, np.nan, inplace=True)
    return {
        'form sample size': len(df['form'].unique().tolist()),
        'transactions': df['trans_count_onetime'].sum() + df['trans_count_recurring'].sum(),
        'conversion': df['conversion'].mean(),
        'conversion onetime': df['conversion_onetime'].mean(),
        'conversion recurring': df['conversion_recurring'].mean(),
        'mean transaction onetime': df['trans_vol_onetime'].sum() / df['trans_count_onetime'].sum(),
        'mean transaction recurring': df['trans_vol_recurring'].sum() / df['trans_count_recurring'].sum(),
        'onetime/recurring': df['trans_count_onetime'].sum() / df['trans_count_recurring'].sum(),
        'pageviews': df['pageviews'].sum(),
        'bounce rate': df['bounces'].sum() / df['pageviews'].sum()
    }


