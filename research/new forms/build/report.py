import sys, datetime
sys.path.append("../../scripts/")
from s3_support import *

import pandas as pd
import numpy as np


# mercy ships: 436247
TARGET_ORG = None
START_DATE = '2020-09-01'
xtra_logs = None
xtra_traffic = None

if TARGET_ORG is not None:
    # hacking target form data
    xtra_logs.append({
        'form': 972972,
        'created': '2021-05-15'
    })
    TRAFFIC_LOAD_PATH = "../../scripts/export google analytics/update/ihruxh.csv"
    xtra_traffic = pd.read_csv(TRAFFIC_LOAD_PATH)
    xtra_traffic['pageviews'] = xtra_traffic['views']
    xtra_traffic.drop('views', axis=1, inplace=True)
    
    START_DATE = '2021-03-15'


if TARGET_ORG is not None:
    print("-"*40)
    print("New forms report for organization {}".format(TARGET_ORG))
    print("-"*40)
    
print("LOAD DATA")

'''
LOADING LOGS DATA FOR FORM CONVERSIONS
'''
print("\tlogs - form template upgrades")
if TARGET_ORG is not None:
    q = "select * from syslog_logs where message like '%Qgiv Form Template Upgraded%' and org={}".format(TARGET_ORG)
else:
    q = "select * from syslog_logs where message like '%Qgiv Form Template Upgraded%'"
df = redshift_query_read(q, schema="production")
df = df[df['message']=='Qgiv Form Template Upgraded']

print("\t\tdone ({} rows, {} - {})".format(len(df), df['created'].min(), df['created'].max()))

converted_forms_dates = df[['form', 'created']].copy()
print("\t\t{} converted form dates, {} converted forms".format(len(converted_forms_dates), len(converted_forms_dates['form'].unique())))

converted_forms_dates.drop_duplicates('form', keep='first', inplace=True)
if xtra_logs is not None:
    if len(converted_forms_dates) == 0:
        converted_forms_dates = xtra_logs
    else:
        converted_forms_dates = converted_forms_dates.append(xtra_logs)
converted_forms_dates.to_csv("converted_forms_dates.csv", index=False)


'''
LOADING RECURRING FREQUENCIES
'''
print("\trecurring frequencies")
q = '''select 
            form,
            date,
            recurring,
            amount
        from transactions 
        where 
            status='A' and
            (source='frontend' or source='mobile') and
            recurring!=0 and
            date_part('year', date)>=2017'''

if TARGET_ORG is not None:
    q = q + " and org={}".format(TARGET_ORG)
    
rec = redshift_query_read(q, schema="public")
rec['date'] = pd.to_datetime(rec['date'])
rec.sort_values('date', ascending=True, inplace=True)

date_diff_data = []
for r in rec['recurring'].unique().tolist():
    _this_rec = rec[rec['recurring']==r]
    date_diff_data.append({
        'recurring': r,
        'form': _this_rec['form'].iloc[0],
        'frequency': _this_rec['date'].diff().mean(),
        'created': _this_rec['date'].min()
    })
    
rec_frequencies = pd.DataFrame(date_diff_data)

converted_forms_list = converted_forms_dates['form'].unique().tolist()
def is_recurring_new_form(r):
    if r['form'] in converted_forms_list:
        if r['created'] >= converted_forms_dates[converted_forms_dates['form']==r['form']]['created'].iloc[0]:
            return True
    return False

rec_frequencies['created'] = pd.to_datetime(rec_frequencies['created'])
rec_frequencies['frequency'] = pd.to_timedelta(rec_frequencies['frequency'])
rec_frequencies['new template'] = rec_frequencies.apply(is_recurring_new_form, axis=1)
rec_frequencies.to_csv("recurring_frequencies.csv", index=False)

'''
LOADING DEVICE CATEGORY CONVERSIONS
'''
print("\tdevice category conversions - transactions")
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
            date >= '{}' '''.format(START_DATE)
if TARGET_ORG is not None:
    q = q + "and org={} ".format(TARGET_ORG)
q = q + "order by date asc"

rec = redshift_query_read(q, schema='public')
rec = rec.groupby('recurring').first().reset_index()
rec['useragent'].fillna('', inplace=True)
rec['is_recurring'] = True

q = '''select 
            org,
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
if TARGET_ORG is not None:
    q = q + " and org={}".format(TARGET_ORG)
    
trans = redshift_query_read(q, schema='public')
trans['useragent'].fillna('', inplace=True)
trans['is_recurring'] = False

trans = trans.append(rec)
trans['is_mobile'] = (trans['useragent'].str.contains('iPhone').fillna(False))|(trans['useragent'].str.contains('iPad').fillna(False))|(trans['useragent'].str.contains('Android').fillna(False))
trans['is_desktop'] = (trans['useragent'].str.contains('Macintosh').fillna(False))|(trans['useragent'].str.contains('Windows').fillna(False))|(trans['useragent'].str.contains('CrOS').fillna(False))

trans_assigned = trans[trans['is_mobile']|trans['is_desktop']].copy()
trans_unassigned = trans[~trans['is_mobile']&~trans['is_desktop']].copy()
trans_unassigned['is_mobile'] = trans_unassigned['source']=='mobile'
trans_unassigned['is_desktop'] = trans_unassigned['source']=='don_form'
trans = trans_assigned.append(trans_unassigned)

trans_src = trans.groupby(['form', 'date', 'is_mobile', 'is_desktop', 'is_recurring']).agg({
    'useragent': 'count',
    'amount': 'sum'
})
trans_src = trans_src.reset_index()
trans_src['trans_count'] = trans_src['useragent']
trans_src['trans_vol'] = trans_src['amount']
trans_src['source'] = trans_src[['is_mobile', 'is_desktop']].apply(lambda x: 'mobile' if x['is_mobile'] else 'desktop', axis=1)
trans_src.drop(['useragent', 'amount', 'is_mobile', 'is_desktop'], axis=1, inplace=True)

trans_src['desktop_trans_count'] = trans_src[['source', 'trans_count']].apply(lambda x: x['trans_count'] if x['source']=='desktop' else 0, axis=1)
trans_src['desktop_trans_vol'] = trans_src[['source', 'trans_vol']].apply(lambda x: x['trans_vol'] if x['source']=='desktop' else 0, axis=1)

trans_src['mobile_trans_count'] = trans_src[['source', 'trans_count']].apply(lambda x: x['trans_count'] if x['source']=='mobile' else 0, axis=1)
trans_src['mobile_trans_vol'] = trans_src[['source', 'trans_vol']].apply(lambda x: x['trans_vol'] if x['source']=='mobile' else 0, axis=1)

trans_src['onetime_desktop'] = trans_src[['is_recurring', 'desktop_trans_count']].apply(lambda x: x['desktop_trans_count'] if not x['is_recurring'] else 0, axis=1)
trans_src['onetime_mobile'] = trans_src[['is_recurring', 'mobile_trans_count']].apply(lambda x: x['mobile_trans_count'] if not x['is_recurring'] else 0, axis=1)
trans_src['recurring_desktop'] = trans_src[['is_recurring', 'desktop_trans_count']].apply(lambda x: x['desktop_trans_count'] if x['is_recurring'] else 0, axis=1)
trans_src['recurring_mobile'] = trans_src[['is_recurring', 'mobile_trans_count']].apply(lambda x: x['mobile_trans_count'] if x['is_recurring'] else 0, axis=1)

trans_src['count_onetime'] = trans_src['onetime_desktop'] + trans_src['onetime_mobile']
trans_src['count_recurring'] = trans_src['recurring_desktop'] + trans_src['recurring_mobile']
trans_src['volume_onetime'] = trans_src[['trans_vol', 'is_recurring']].apply(lambda x: x['trans_vol'] if not x['is_recurring'] else 0, axis=1)
trans_src['volume_recurring'] = trans_src[['trans_vol', 'is_recurring']].apply(lambda x: x['trans_vol'] if x['is_recurring'] else 0, axis=1)


print("\tdevice category conversions - traffic")
q = '''select
            date,
            form,
            devicecategory,
            sum(views) as pageviews
        from googleanalytics_traffic
        where 
            qgiv_frontend=1 and
            date >= '{}' '''.format(START_DATE)
if TARGET_ORG is not None:
    q = q + "and org={} ".format(TARGET_ORG)
q = q + "group by date, devicecategory, form"

traffic = redshift_query_read(q, schema='public')

if xtra_traffic is not None:
    if len(traffic) == 0:
        traffic = xtra_traffic
    else:
        traffic = traffic.append(xtra_traffic)

df_dc = traffic.pivot(index=['date', 'form'], columns='devicecategory', values='pageviews').reset_index().fillna(0)
# merging tablet & mobile
df_dc['mobile'] = df_dc['mobile'] + df_dc['tablet']
df_dc['desktop_pageviews'] = df_dc['desktop'].astype(int)
df_dc['mobile_pageviews'] = df_dc['mobile'].astype(int)
df_dc.drop(['tablet', 'desktop', 'mobile'], axis=1, inplace=True)

grpd_cols = ['onetime_desktop', 'onetime_mobile', 'recurring_desktop', 'recurring_mobile']
device_conversion = df_dc.merge(trans_src.groupby(['form', 'date'])[grpd_cols].sum().reset_index(), on=['form', 'date'], how='outer').fillna(0)
device_conversion['onetime_desktop_conversion'] = device_conversion['onetime_desktop'] / device_conversion['desktop_pageviews']
device_conversion['onetime_mobile_conversion'] = device_conversion['onetime_mobile'] / device_conversion['mobile_pageviews']
device_conversion['recurring_desktop_conversion'] = device_conversion['recurring_desktop'] / device_conversion['desktop_pageviews']
device_conversion['recurring_mobile_conversion'] = device_conversion['recurring_mobile'] / device_conversion['mobile_pageviews']

onetime_desktop_conv = device_conversion['onetime_desktop_conversion'].replace(np.inf, np.nan).mean()
onetime_mobile_conv = device_conversion['onetime_mobile_conversion'].replace(np.inf, np.nan).mean()
recurring_desktop_conv = device_conversion['recurring_desktop_conversion'].replace(np.inf, np.nan).mean()
recurring_mobile_conv = device_conversion['recurring_mobile_conversion'].replace(np.inf, np.nan).mean()

print()
print("CONVERSION:")

print("One time:")
print("Desktop: {:.2f}%".format(onetime_desktop_conv * 100.))
print("Mobile: {:.2f}%".format(onetime_mobile_conv * 100.))
print()
print("Recurring:")
print("Desktop: {:.2f}%".format(recurring_desktop_conv * 100.))
print("Mobile: {:.2f}%".format(recurring_mobile_conv * 100.))
print()

device_conversion.to_csv("device_conversions.csv", index=False)


print("\ttraffic overall breakdown by device category")
# load traffic
q = '''select
            devicecategory,
            sum(views) as pageviews
        from googleanalytics_traffic
        where 
            qgiv_frontend=1 and
            date >= '{}' '''.format(START_DATE)
if TARGET_ORG is not None:
    q = q + "and org={} ".format(TARGET_ORG)
q = q + "group by devicecategory"

traffic_device = redshift_query_read(q, schema='public')
traffic_device['percentage'] = traffic_device['pageviews'] / traffic_device['pageviews'].sum()

print()
print("Device category traffic (all):")
print(traffic_device)
print()

converted_forms_dates['converted'] = pd.to_datetime(converted_forms_dates['created'])
converted_forms_dates.drop('created', axis=1, inplace=True)

q = '''select
            date,
            form,
            devicecategory,
            sum(views) as pageviews
        from googleanalytics_traffic
        where 
            qgiv_frontend=1 and
            date >= '{}' '''.format(START_DATE)
if TARGET_ORG is not None:
    q = q + "and org={} ".format(TARGET_ORG)
q = q + "group by devicecategory, date, form"

traffic_device = redshift_query_read(q, schema='public')
traffic_device['date'] = pd.to_datetime(traffic_device['date'])

converted_forms = converted_forms_dates['form'].unique().tolist()

def is_form_converted_date(r):
    if r['form'] in converted_forms:
        if r['date'] >= converted_forms_dates[converted_forms_dates['form']==r['form']]['converted'].iloc[0]:
            return True
    return False
    
traffic_device['is_new_form'] = traffic_device[['date', 'form']].apply(is_form_converted_date, axis=1)

print("\t\tdevice category traffic for relevant period")
pvt_device_traffic = traffic_device.groupby(['is_new_form', 'devicecategory'])['pageviews'].sum().reset_index().pivot(index='devicecategory', columns='is_new_form', values='pageviews').reset_index()

if False in pvt_device_traffic:
    pvt_device_traffic['old form'] = pvt_device_traffic[False]
    pvt_device_traffic.drop([False], axis=1, inplace=True)
else:
    pvt_device_traffic['old form'] = 0
if True in pvt_device_traffic:
    pvt_device_traffic['new form'] = pvt_device_traffic[True]
    pvt_device_traffic.drop([True], axis=1, inplace=True)
else:
    pvt_device_traffic['new form'] = 0
    
pvt_device_traffic['old form perc'] = pvt_device_traffic['old form'] / pvt_device_traffic['old form'].sum()
pvt_device_traffic['new form perc'] = pvt_device_traffic['new form'] / pvt_device_traffic['new form'].sum()

print()
print("New vs.old form device category traffic breakdown")
print(pvt_device_traffic)
print()


print("\t\ttransactions again")
# query onetime
q = '''select 
            form, 
            org, 
            sum(amount) as volume_onetime, 
            count(id) as count_onetime, 
            date 
        from transactions 
        where 
            status='A' and
            creatingtransactionfor=0 and
            recurring=0'''
if TARGET_ORG is not None:
    q = q + " and org={}".format(TARGET_ORG)
q = q + "group by form, org, date"

trans_onetime = redshift_query_read(q, schema="public")
trans_onetime['date'] = pd.to_datetime(trans_onetime['date'])

# query recurring
q = '''select 
            form, 
            org, 
            amount, 
            id, 
            date 
        from transactions 
        where 
            status='A' and
            recurring!=0'''
if TARGET_ORG is not None:
    q = q + " and org={}".format(TARGET_ORG)
q = q + " order by date asc"

trans_rec = redshift_query_read(q, schema="public")
trans_rec['date'] = pd.to_datetime(trans_rec['date'])
trans_rec.drop_duplicates(subset=['id'], keep='first', inplace=True)

# aggregate recurring
trans_rec = trans_rec.groupby(['form', 'org', 'date']).agg({'amount': 'sum', 'id': 'count'}).reset_index()
trans_rec['count_recurring'] = trans_rec['id']
trans_rec['volume_recurring'] = trans_rec['amount']
trans_rec.drop(['id', 'amount'], axis=1, inplace=True)

# merge one time & recurring
trans = trans_onetime.merge(trans_rec, on=['form', 'org', 'date'])


print("\t\ttraffic")
q = '''select
            date, 
            org,
            form,
            sum(views) as pageviews
        from googleanalytics_traffic
        where qgiv_frontend=1 and date>='{}' '''.format(START_DATE)
if TARGET_ORG is not None:
    q = q + "and org={} ".format(TARGET_ORG)
q = q + "group by date, org, form"

traffic = redshift_query_read(q, schema="public")
traffic['date'] = pd.to_datetime(traffic['date'])

q = "select id, type from form where status=1"
forms = redshift_query_read(q, schema="production")
active_qgiv_forms = forms[forms['type']==1]['id'].tolist()

trans = trans[trans['form'].isin(active_qgiv_forms)]
trans = trans[trans['date']>=traffic['date'].min()]
forms_conversions = trans.merge(traffic, on=['form', 'date'], how='outer')
forms_conversions.fillna(0, inplace=True)
forms_conversions['conversion_onetime'] = forms_conversions['count_onetime'] / forms_conversions['pageviews']
forms_conversions['conversion_recurring'] = forms_conversions['count_recurring'] / forms_conversions['pageviews']
forms_conversions.to_csv("forms_conversion.csv", index=False)

print("\t\tconversions by device category")
q = '''select
            date, 
            org,
            form,
            devicecategory,
            sum(views) as pageviews
        from googleanalytics_traffic
        where qgiv_frontend=1'''
if TARGET_ORG is not None:
    q = q + " and org={}".format(TARGET_ORG)
q = q + " group by date, org, form, devicecategory"
traffic_device = redshift_query_read(q, schema="public")
traffic_device['date'] = pd.to_datetime(traffic_device['date'])

device_conversions = trans.merge(traffic_device, on=['form', 'date'], how='outer')
device_conversions['conversion_onetime'] = device_conversions['count_onetime'] / device_conversions['pageviews']
device_conversions['conversion_recurring'] = device_conversions['count_recurring'] / device_conversions['pageviews']
device_conversions = device_conversions[device_conversions['pageviews']>0]
device_conversions.to_csv("forms_device_conversion.csv", index=False)

'''
PRINTING REPORT OUTPUT
'''

template_upgrades = pd.read_csv("converted_forms_dates.csv", low_memory=False)
template_upgrades['created'] = pd.to_datetime(template_upgrades['created'])

daily_conversions = pd.read_csv("forms_conversion.csv", low_memory=False)

daily_conversions['date'] = pd.to_datetime(daily_conversions['date'])
daily_conversions['avg_onetime'] = daily_conversions['volume_onetime'] / daily_conversions['count_onetime']
daily_conversions['avg_recurring'] = daily_conversions['volume_recurring'] / daily_conversions['count_recurring']
daily_conversions['onetime / recurring'] = daily_conversions['count_onetime'] / daily_conversions['count_recurring']

daily_conversions = daily_conversions[daily_conversions['pageviews']>0]
daily_conversions['conversion_onetime'] = daily_conversions['count_onetime'] / daily_conversions['pageviews']
daily_conversions['conversion_recurring'] = daily_conversions['count_recurring'] / daily_conversions['pageviews']

device_conversions = pd.read_csv("forms_device_conversion.csv")
device_conversions['date'] = pd.to_datetime(device_conversions['date'])
device_conversions['avg_onetime'] = device_conversions['volume_onetime'] / device_conversions['count_onetime']
device_conversions['avg_recurring'] = device_conversions['volume_recurring'] / device_conversions['count_recurring']
device_conversions['onetime / recurring'] = device_conversions['count_onetime'] / device_conversions['count_recurring']

# isolate list of form IDs that have been converted
converted_forms = template_upgrades['form'].unique().tolist()

# get active forms percentage of converted forms
q = "select id, status from form"
forms = redshift_query_read(q, schema="production")
forms_statuses_conv = forms[forms['id'].isin(converted_forms)]
active_converted_forms_count = forms_statuses_conv['status'].value_counts()[1]
active_converted_forms_perc = forms_statuses_conv['status'].value_counts(normalize=True)[1]

# recurring frequencies
rec_frequencies = pd.read_csv("recurring_frequencies.csv", low_memory=False)
rec_frequencies['created'] = pd.to_datetime(rec_frequencies['created'])
rec_frequencies['frequency'] = pd.to_timedelta(rec_frequencies['frequency'])

# device conversions
device_conversions = pd.read_csv("device_conversions.csv", low_memory=False)
device_conversions['date'] = pd.to_datetime(device_conversions['date'])

def get_template_type(r):
    if r['form'] in template_upgrades['form'].tolist():
        if r['date']>=template_upgrades[template_upgrades['form']==r['form']]['created'].iloc[0]:
            return True
    return False

device_conversions['new template'] = device_conversions.apply(get_template_type, axis=1)

def was_converted(r):
    if r['form'] in template_upgrades['form'].tolist():
        if r['date'] >= template_upgrades[template_upgrades['form']==r['form']]['created'].iloc[0]:
            return True
    
    return False

daily_conversions['new template'] = daily_conversions.apply(was_converted, axis=1)
device_conversions['new template'] = device_conversions.apply(was_converted, axis=1)

converted_daily_entries = daily_conversions[daily_conversions['form'].isin(template_upgrades['form'].unique().tolist())]
converted_trans_sum = converted_daily_entries['count_onetime'].sum() + converted_daily_entries['count_recurring'].sum()
converted_trans_perc = (converted_trans_sum / (daily_conversions['count_onetime'].sum() + daily_conversions['count_recurring'].sum())) * 100.

print("converted forms: {:,}".format(len(converted_forms)))
print("converted forms w/ active status: {:.2f}%".format(active_converted_forms_perc * 100.))
print("converted forms w/ transactions: {:,}".format(len(converted_daily_entries['form'].unique())))
print("total transactions of converted forms: {:,} ({:.2f}%)".format(converted_trans_sum, converted_trans_perc))

print("Device category traffic overall:")
traffic_grpd = traffic_device.groupby('devicecategory')['pageviews'].sum().reset_index()
traffic_grpd['percentage'] = (traffic_grpd['pageviews'] / traffic_grpd['pageviews'].sum()) * 100.
traffic_grpd['percentage'] = traffic_grpd['percentage'].apply(lambda x: "{:.2f}%".format(x))
traffic_grpd['pageviews'] = traffic_grpd['pageviews'].apply(lambda x: "{:,}".format(x))
print(traffic_grpd)
print()

print()
min_year = daily_conversions['date'].min().year

# one time
conv_mean = daily_conversions['conversion_onetime'].mean()
conv_median = daily_conversions['conversion_onetime'].median()

print("All forms ({}+) - one time:".format(min_year))
print("-"*40)
print("Conversion:")
print("\tMean: {:.2f}%".format(conv_mean * 100.))
print("\tMedian: {:.2f}%".format(conv_median * 100.))
print("Per transaction:")
print("\tMean: ${:,.2f}".format(daily_conversions['avg_onetime'].mean()))
print("\tMedian: ${:,.2f}".format(daily_conversions['avg_onetime'].median()))

print()
onetime_cols = ['onetime_desktop_conversion', 'onetime_mobile_conversion']
print(device_conversions[onetime_cols].replace([np.inf, -np.inf], np.nan).dropna().mean())

# recurring
conv_mean = daily_conversions['conversion_recurring'].mean()
conv_median = daily_conversions['conversion_recurring'].median()

print()
print("All forms ({}+) - recurring:".format(min_year))
print("-"*40)
print("Conversion:")
print("\tMean: {:.2f}%".format(conv_mean * 100.))
print("\tMedian: {:.2f}%".format(conv_median * 100.))
print("Per transaction:")
print("\tMean: ${:,.2f}".format(daily_conversions['avg_recurring'].mean()))
print("\tMedian: ${:,.2f}".format(daily_conversions['avg_recurring'].median()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(rec_frequencies['frequency'].mean()))
print("\tMedian: {}".format(rec_frequencies['frequency'].median()))

print()
print("One time / Recurring: {:.2f}".format(daily_conversions['onetime / recurring'].mean()))


print()

print("Isolated time frame to approximately when processing begins with new forms ({}+), all forms:".format(START_DATE))
print()

date_iso = daily_conversions[daily_conversions['date']>=START_DATE]
len_all_forms = len(date_iso['form'].unique())
len_all_trans = date_iso['count_onetime'].sum() + date_iso['count_recurring'].sum()
device_date_iso = device_conversions[device_conversions['date']>=START_DATE]

nuform_device = device_date_iso[device_date_iso['new template']]
nuform_rec_frequency = rec_frequencies[(rec_frequencies['new template'])&(rec_frequencies['created']>=START_DATE)]

nuform = date_iso[date_iso['new template']]
len_nuform_forms = len(nuform['form'].unique())
len_nuform_trans = nuform['count_onetime'].sum() + nuform['count_recurring'].sum()

print("New form:")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_nuform_forms, (len_nuform_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_nuform_trans, (len_nuform_trans / len_all_trans) * 100.))

print("conversion:")
print("\tOne time mean: {:.2f}%".format(nuform['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(nuform['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(nuform['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(nuform['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(nuform['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(nuform['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(nuform['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(nuform['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(nuform['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(nuform_rec_frequency['frequency'].mean()))
print("\tMedian: {}".format(nuform_rec_frequency['frequency'].median()))

print()

oldform_rec_frequency = rec_frequencies[(~rec_frequencies['new template'])&(rec_frequencies['created']>=START_DATE)]
oldform_device = device_date_iso[~device_date_iso['new template']]
oldform = date_iso[~date_iso['new template']]
len_oldform_forms = len(oldform['form'].unique())
len_oldform_trans = oldform['count_onetime'].sum() + oldform['count_recurring'].sum()

print("Old form:")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_oldform_forms, (len_oldform_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_oldform_trans, (len_oldform_trans / len_all_trans) * 100.))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(oldform['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(oldform['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(oldform['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(oldform['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(oldform['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(oldform['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(oldform['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(oldform['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(oldform['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(oldform_rec_frequency['frequency'].mean()))
print("\tMedian: {}".format(oldform_rec_frequency['frequency'].median()))

print()

print()

overall_conv = nuform[['form', 'date', 'count_recurring', 'count_onetime', 'pageviews']].copy()
overall_conv['conversion'] = (overall_conv['count_recurring'] + overall_conv['count_onetime']) / overall_conv['pageviews']
print("New form conversion: {:.2f}%".format(overall_conv['conversion'].mean() * 100.))

overall_conv = oldform[['form', 'date', 'count_recurring', 'count_onetime', 'pageviews']].copy()
overall_conv['conversion'] = (overall_conv['count_recurring'] + overall_conv['count_onetime']) / overall_conv['pageviews']
print("Old form conversion: {:.2f}%".format(overall_conv['conversion'].mean() * 100.))

print("Forms w/ transactions in new & old, isolated timeframe:")
print()

nuoldform_device = nuform_device[nuform_device['form'].isin(oldform_device['form'].unique().tolist())]
nuoldform_rec_frequency = nuform_rec_frequency[nuform_rec_frequency['form'].isin(oldform_rec_frequency['form'].unique().tolist())]

nuoldform = nuform[nuform['form'].isin(oldform['form'].unique().tolist())]
len_nuoldform_forms = len(nuoldform['form'].unique())
len_nuoldform_trans = nuoldform['count_onetime'].sum() + nuoldform['count_recurring'].sum()

print("Converted form (after conversion):")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_nuoldform_forms, (len_nuoldform_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_nuoldform_trans, (len_nuoldform_trans / len_all_trans) * 100.))
print("Transactions per form: {:.2f}".format(nuoldform.groupby('form')['count_onetime'].sum().mean()))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(nuoldform['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(nuoldform['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(nuoldform['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(nuoldform['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(nuoldform['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(nuoldform['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(nuoldform['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(nuoldform['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(nuoldform['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(nuoldform_rec_frequency['frequency'].mean()))
print("\tMedian: {}".format(nuoldform_rec_frequency['frequency'].median()))


print()

oldconvform_device = oldform_device[oldform_device['form'].isin(nuform_device['form'].tolist())]
oldconvform_rec_frequency = oldform_rec_frequency[oldform_rec_frequency['form'].isin(nuform_rec_frequency['form'].unique().tolist())]

oldconvform = oldform[oldform['form'].isin(nuform['form'].tolist())]
len_oldconvform_forms = len(oldconvform['form'].unique())
len_oldconvform_trans = oldconvform['count_onetime'].sum() + oldconvform['count_recurring'].sum()

print("Converted Old form (prior to conversion):")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_oldconvform_forms, (len_oldconvform_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_oldconvform_trans, (len_oldconvform_trans / len_all_trans) * 100.))
print("Transactions per form: {:.2f}".format(oldconvform.groupby('form')['count_onetime'].sum().mean()))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(oldconvform['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(oldconvform['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(oldconvform['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(oldconvform['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(oldconvform['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(oldconvform['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(oldconvform['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(oldconvform['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(oldconvform['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(oldconvform_rec_frequency['frequency'].mean()))
print("\tMedian: {}".format(oldconvform_rec_frequency['frequency'].median()))

print()

print("Forms w/ transactions in new & old, last 60 days:")
print()

sixty_days_ago = datetime.datetime.now() - pd.to_timedelta("60day")

nuoldform_device = nuform_device[(nuform_device['form'].isin(oldform_device['form'].unique().tolist()))&(nuform_device['date']>=sixty_days_ago)]
nuoldform_rec_frequency = nuform_rec_frequency[(nuform_rec_frequency['form'].isin(oldform_rec_frequency['form'].unique().tolist()))&(nuform_rec_frequency['created']>=sixty_days_ago)]

nuoldform = nuform[(nuform['form'].isin(oldform['form'].unique().tolist()))&(nuform['date']>=sixty_days_ago)]
len_nuoldform_forms = len(nuoldform['form'].unique())
len_nuoldform_trans = nuoldform['count_onetime'].sum() + nuoldform['count_recurring'].sum()

print("Converted form (after conversion):")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_nuoldform_forms, (len_nuoldform_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_nuoldform_trans, (len_nuoldform_trans / len_all_trans) * 100.))
print("Transactions per form: {:.2f}".format(nuoldform.groupby('form')['count_onetime'].sum().mean()))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(nuoldform['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(nuoldform['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(nuoldform['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(nuoldform['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(nuoldform['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(nuoldform['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(nuoldform['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(nuoldform['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(nuoldform['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(nuoldform_rec_frequency['frequency'].mean()))
print("\tMedian: {}".format(nuoldform_rec_frequency['frequency'].median()))


print()

oldconvform_device = oldform_device[(oldform_device['form'].isin(nuform_device['form'].tolist()))&(oldform_device['date']>=sixty_days_ago)]
oldconvform_rec_frequency = oldform_rec_frequency[(oldform_rec_frequency['form'].isin(nuform_rec_frequency['form'].tolist()))&(oldform_rec_frequency['created']>=sixty_days_ago)]

oldconvform = oldform[(oldform['form'].isin(nuform['form'].tolist()))&(oldform['date']>=sixty_days_ago)]
len_oldconvform_forms = len(oldconvform['form'].unique())
len_oldconvform_trans = oldconvform['count_onetime'].sum() + oldconvform['count_recurring'].sum()

print("Converted Old form (prior to conversion):")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_oldconvform_forms, (len_oldconvform_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_oldconvform_trans, (len_oldconvform_trans / len_all_trans) * 100.))
print("Transactions per form: {:.2f}".format(oldconvform.groupby('form')['count_onetime'].sum().mean()))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(oldconvform['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(oldconvform['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(oldconvform['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(oldconvform['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(oldconvform['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(oldconvform['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(oldconvform['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(oldconvform['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(oldconvform['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(oldconvform_rec_frequency['frequency'].mean()))
print("\tMedian: {}".format(oldconvform_rec_frequency['frequency'].median()))

print()

print("Last 30 days, all forms, grouped by new/old")
print()

thirty_days_ago = daily_conversions['date'].max() - pd.to_timedelta("30day")
last_30_days = daily_conversions[daily_conversions['date']>=thirty_days_ago]
last_30_days_device = device_conversions[device_conversions['date']>=thirty_days_ago]
last_30_days_rec_frequency = rec_frequencies[rec_frequencies['created']>=thirty_days_ago]

len_conv_forms = len(last_30_days[last_30_days['new template']]['form'].unique())
len_old_forms = len(last_30_days[~last_30_days['new template']]['form'].unique())
len_all_forms = len(last_30_days['form'].unique())

len_conv_trans = last_30_days[last_30_days['new template']]['count_onetime'].sum() + last_30_days[last_30_days['new template']]['count_recurring'].sum()
len_old_trans = last_30_days[~last_30_days['new template']]['count_onetime'].sum() + last_30_days[~last_30_days['new template']]['count_recurring'].sum()
len_all_trans = last_30_days['count_onetime'].sum() + last_30_days['count_recurring'].sum()

print("New form")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_conv_forms, (len_conv_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_conv_trans, (len_conv_trans / len_all_trans) * 100.))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(last_30_days[last_30_days['new template']]['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(last_30_days[last_30_days['new template']]['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(last_30_days[last_30_days['new template']]['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(last_30_days[last_30_days['new template']]['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(last_30_days[last_30_days['new template']]['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(last_30_days[last_30_days['new template']]['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(last_30_days[last_30_days['new template']]['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(last_30_days[last_30_days['new template']]['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(last_30_days[last_30_days['new template']]['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(last_30_days_rec_frequency[last_30_days_rec_frequency['new template']]['frequency'].mean()))
print("\tMedian: {}".format(last_30_days_rec_frequency[last_30_days_rec_frequency['new template']]['frequency'].median()))


print()

print("Old form")
print("-"*40)
print("Form sample size: {:,} ({:.2f}%)".format(len_old_forms, (len_old_forms / len_all_forms) * 100.))
print("Transaction sample size: {:,} ({:.2f}%)".format(len_old_trans, (len_old_trans / len_all_trans) * 100.))
print("conversion:")
print("\tOne time mean: {:.2f}%".format(last_30_days[~last_30_days['new template']]['conversion_onetime'].mean() * 100.))
print("\tOne time median: {:.2f}%".format(last_30_days[~last_30_days['new template']]['conversion_onetime'].median() * 100.))
print("\tRecurring mean: {:.2f}%".format(last_30_days[~last_30_days['new template']]['conversion_recurring'].mean() * 100.))
print("\tRecurring median: {:.2f}%".format(last_30_days[~last_30_days['new template']]['conversion_recurring'].median() * 100.))
print("per transaction:")
print("\tOne time mean: ${:,.2f}".format(last_30_days[~last_30_days['new template']]['avg_onetime'].mean()))
print("\tOne time median: ${:,.2f}".format(last_30_days[~last_30_days['new template']]['avg_onetime'].median()))
print("\tRecurring mean: ${:,.2f}".format(last_30_days[~last_30_days['new template']]['avg_recurring'].mean()))
print("\tRecurring median: ${:,.2f}".format(last_30_days[~last_30_days['new template']]['avg_recurring'].median()))

print()
print("One time / recurring: {:.2f}".format(last_30_days[~last_30_days['new template']]['onetime / recurring'].mean()))

print()
print("Recurring frequency:")
print("\tMean: {}".format(last_30_days_rec_frequency[~last_30_days_rec_frequency['new template']]['frequency'].mean()))
print("\tMedian: {}".format(last_30_days_rec_frequency[~last_30_days_rec_frequency['new template']]['frequency'].median()))

print()

print("Device categories")
print()

conv_cols = ['onetime_desktop_conversion', 'onetime_mobile_conversion',
            'recurring_desktop_conversion', 'recurring_mobile_conversion']

print("All time")
print("{}+ device conversion means".format(device_conversions['date'].min()))
print(device_conversions.replace(np.inf, np.nan).groupby('new template')[conv_cols].mean().reset_index().transpose())

print()

print("Last 60 days conversion means")
print(device_conversions.replace(np.inf, np.nan)[device_conversions['date']>=sixty_days_ago].groupby('new template')[conv_cols].mean().reset_index().transpose())