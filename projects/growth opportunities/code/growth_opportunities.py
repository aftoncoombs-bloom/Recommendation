import pandas as pd
import datetime, os

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

PATH_TRANS = "../transactions/transactions.csv"
PATH_QGIVANALYTICS = "analytic_qgiv_stats.csv"
PATH_PRIOR_PREDS = "growth_preds.csv"
PATH_ORGS = "organizations.clean.csv"

tips = [
    "Organizations with P2P forms raise more than 25 times more when they also use year round forms than those only using P2P",
    "Of organizations utilizing SMS, those which do not rely upon SMS for the majority of their fundraising raise more than 172 times more than those that do rely upon SMS for the majority of their fundraising",
    "Organizations that rely upon events for less than 50% of their funds raised will generate about 50% more in funds than those that rely upon events for more than 50% of their funds raised",
    "Donors give 2.4 times the amount in recurring donations than one time",
    "Donor logins can lead to up to 4 times the donations (by count, not volume) per donor"
]

print("Load data")
df_trans = pd.read_csv(PATH_TRANS, low_memory=False)

print("\tprepping analytics features - getting donor logins activation setting")
org_dl_count_bld = None
for _df in pd.read_csv(PATH_QGIVANALYTICS, engine='python', encoding='utf-8', error_bad_lines=False, chunksize=10000):
    if org_dl_count_bld is None:
        org_dl_count_bld = _df.groupby('org')['dl_trans_count'].sum().reset_index()
    else:
        org_dl_count_bld = org_dl_count_bld.append(_df.groupby('org')['dl_trans_count'].sum().reset_index())
org_dl_count = org_dl_count_bld.groupby('org')['dl_trans_count'].sum().reset_index()

print("\tprepping trans features")
print("\t\tdate handling")
df_trans['date'] = pd.to_datetime(df_trans['date'])
df_trans['year'] = df_trans['date'].dt.year
df_trans['month'] = df_trans['date'].dt.month
df_trans['year_month'] = df_trans[['year', 'month']].apply(lambda x: str(x['year']) + "/" + str(x['month']), axis=1)

print("\t\tprepping columns for recurring transactions")
df_trans['recurring_amt'] = df_trans[['amount', 'is_recurring']].apply(lambda x: x['amount'] if x['is_recurring'] else 0., axis=1)

print("\t\taggregating")
sum_cols = ['amount', 'donations_amt', 'events_amt', 'purchases_amt', 'registrations_amt', 'recurring_amt']
ix_cols = ['org', 'form', 'year_month']
df_agg = df_trans[ix_cols + sum_cols].groupby(ix_cols)[sum_cols].sum().reset_index()
for col in sum_cols:
    if col != "amount":
        df_agg["{}_perc".format(col)] = df_agg[col] / df_agg['amount']

df_source_agg = df_trans[['org', 'source', 'amount']].groupby(['org', 'source'])['amount'].sum().reset_index().pivot(index='org', columns='source', values='amount').reset_index().fillna(0.)
sources = ['don_form', 'fb', 'givi', 'kiosk', 'mobile', 'mobilevt', 'p2p', 'sms', 'vt']
df_source_agg['total'] = df_source_agg[sources].sum(axis=1)
for s in sources:
    df_source_agg[s+'_perc'] = df_source_agg[s] / df_source_agg['total']

print("Find designated groups")
print("\tlow donor logins")
orgs_low_dl = org_dl_count[org_dl_count['dl_trans_count']<10]['org'].tolist()

print("\tlow transaction source rates")
# recurring
# @TODO is 10% threshold right here?
orgs_low_recurring = df_agg[df_agg["recurring_amt_perc"]<.1]['org'].tolist()
# events
orgs_high_events = df_agg[df_agg["events_amt_perc"]>.5]['org'].tolist()
# sms
orgs_high_sms = df_source_agg[df_source_agg['sms_perc']>.5]['org'].tolist()
# p2p
orgs_only_p2p = df_source_agg[df_source_agg['p2p_perc']>.9]['org'].tolist()

print("Output list of orgs with groups")
unique_orgs = list(set(orgs_low_recurring + orgs_high_events + orgs_high_sms + orgs_only_p2p + orgs_low_dl))
org_list = pd.DataFrame(unique_orgs, columns=['org'])
org_list['low_recurring'] = org_list['org'].apply(lambda x: True if x in orgs_low_recurring else False)
org_list['high_events'] = org_list['org'].apply(lambda x: True if x in orgs_high_events else False)
org_list['high_sms'] = org_list['org'].apply(lambda x: True if x in orgs_high_sms else False)
org_list['only_p2p'] = org_list['org'].apply(lambda x: True if x in orgs_only_p2p else False)
org_list['low_dl'] = org_list['org'].apply(lambda x: True if x in orgs_low_dl else False)
org_list['total'] = org_list[['low_recurring', 'low_dl', 'high_events', 'high_sms', 'only_p2p']].sum(axis=1)
org_list.sort_values('total', ascending=False, inplace=True)

# remove previously recommended orgs
prior_preds = []
if os.path.exists(PATH_PRIOR_PREDS):
    prior_preds = pd.read_csv(PATH_PRIOR_PREDS)['org'].tolist()

orgs = pd.read_csv(PATH_ORGS)
active_orgs = orgs[orgs['status']==1]['id'].tolist()

# report 
these_preds = org_list[(~org_list['org'].isin(prior_preds))&(org_list['org'].isin(active_orgs))].head(10).copy()
these_preds['date'] = datetime.datetime.today()

if os.path.exists(PATH_PRIOR_PREDS):
    pd.read_csv(PATH_PRIOR_PREDS).append(pd.DataFrame(these_preds)).to_csv(PATH_PRIOR_PREDS, index=False)
else:
    pd.DataFrame(these_preds).to_csv(PATH_PRIOR_PREDS, index=False)

print(these_preds.drop('date', axis=1))
