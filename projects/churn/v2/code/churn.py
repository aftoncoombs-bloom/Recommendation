import pandas as pd
import numpy as np
import sys, datetime
sys.path.insert(1, '../../../../scripts/')
from s3_support import *


def get_orgs_logged_in_last_3_months():    
    q = '''select
                distinct(org) as org
            from users
            where
                lastlogin >= add_months(current_date, -3);'''
    return redshift_query_read(q, schema="production")


def get_diff_mean_growth_churned(churned_orgs_ids):
    q = '''select
                org,
                count(distinct form) as forms,
                date_trunc('month', date) as month,
                count(id) as count,
                sum(amount) as volume
            from transactions
                where status='A'
                group by org, date_trunc('month', date)
                order by date_trunc('month', date) desc;'''
    df_trans_agg = redshift_query_read(q)
    df_trans_agg['month'] = pd.to_datetime(df_trans_agg['month'])
    df_trans_agg.sort_values('month', ascending=True, inplace=True)

    org_growth_data = []

    for org in df_trans_agg['org'].unique():
        this_df = df_trans_agg[df_trans_agg['org']==org].copy()
        if len(this_df) <= 1:
            continue
        this_df['growth'] = this_df['volume'].diff() / this_df['volume'].shift(1)

        org_growth_data.append({
            'org': org,
            'growth': this_df['growth'].replace([np.inf, -np.inf], np.nan).dropna().mean()
        })

    growth_df = pd.DataFrame(org_growth_data)
    growth_df['churned'] = growth_df['org'].isin(churned_orgs_ids)
    
    mean_churned_growth_rate = growth_df[growth_df['churned']]['growth'].mean()
    
    growth_df['mean_diff_growth_churned'] = growth_df['growth'] - mean_churned_growth_rate
    
    return growth_df[['org', 'mean_diff_growth_churned']]


def get_orgs_created_users_in_last_3_months():
    q = '''select
                org,
                count(id) as user_count
            from users
            where createddate >= add_months(current_date, -3)
            group by org'''
    return redshift_query_read(q, schema="production")


print("load orgs, integrations, transactions, recent logins, growth trend")
df_orgs = get_dataframe_from_file("qgiv-stats-data", "organizations.names.csv")
df_integrations = get_dataframe_from_file("qgiv-stats-data", 'integrations.csv')
df_trans = redshift_query_read("select * from transactions where status='A' and date>=DATEADD('month', -6, CURRENT_DATE)")
logged_in_3_months = get_orgs_logged_in_last_3_months()
created_users = get_orgs_created_users_in_last_3_months()

zd = get_dataframe_from_file("qgiv-stats-data", "zendesk.mrgd.csv")
zd = zd[['external_id', 'created_at', 'updated_at']]
zd = zd[zd['external_id'].apply(lambda x: str(x).isnumeric())]
zd['org'] = zd['external_id'].astype(int, errors='ignore')
zd.drop('external_id', axis=1, inplace=True)
zd['created_at'] = pd.to_datetime(zd['created_at'])


print("prep data")
orgs_trans_counts = df_trans.groupby('org')['id'].count().reset_index()
inactive_orgs = df_orgs[(df_orgs['status']=='active')&(~df_orgs['id'].isin(orgs_trans_counts['org'].tolist()))]['id'].tolist()
orgs_never_viable = orgs_trans_counts[orgs_trans_counts['id']<100]['org'].tolist() + inactive_orgs

df_orgs['churned'] = ~df_orgs['date_closed'].isnull()

orgs_growth = get_diff_mean_growth_churned(df_orgs[df_orgs['churned']]['id'].tolist())
df_orgs = df_orgs.merge(orgs_growth, right_on="org", left_on="id")

df_orgs['integrations'] = df_orgs['id'].isin(df_integrations['org'].tolist())
df_orgs['recent_logins'] = df_orgs['id'].isin(logged_in_3_months['org'].tolist())
df_orgs['recent_created_users'] = df_orgs['id'].isin(created_users['org'].tolist())
df_orgs['zendesk_active'] = df_orgs['id'].isin(zd['org'].tolist())
df_orgs['feature_sum'] = df_orgs[['zendesk_active', 'integrations', 'recent_logins', 'recent_created_users']].sum(axis=1)
df_orgs['never_viable'] = df_orgs['id'].isin(orgs_never_viable)

cols = ['id', 'org_name', 'status', 'churned', 'mean_diff_growth_churned', 
        'integrations', 'recent_logins', 'recent_created_users', 'zendesk_active',
        'never_viable', 'feature_sum']
df_orgs = df_orgs[cols]
# omit never viable orgs
df_orgs = df_orgs[~df_orgs['never_viable']]


print("filtering prior preds w/in 6 months")
six_months_ago = datetime.datetime.today() - datetime.timedelta(6*365/12)
tdy = datetime.datetime.today()
try:
    df_priorpreds = get_dataframe_from_file("qgiv-stats-data", "preds.churn.csv")
    df_priorpreds['Date'] = pd.to_datetime(df_priorpreds['Date'])
    df_priorpreds = df_priorpreds[df_priorpreds['Date']>six_months_ago]
    print("\t{} prior preds found".format(len(df_priorpreds)))
except Exception as e:
    df_priorpreds = pd.DataFrame(columns=['ID', 'Date', 'Org Name'])
    print("\tno prior preds found")
    print(e)
    
df_orgs = df_orgs[(df_orgs['status']=='active')&(~df_orgs['id'].isin(df_priorpreds['ID'].tolist()))]
potential_churns = df_orgs[df_orgs['feature_sum']<=2]

print("sorting for churn predictions")
potential_churns['mean_diff_growth_churned_diff'] = np.abs(potential_churns['mean_diff_growth_churned'].abs() - df_orgs[df_orgs['churned']]['mean_diff_growth_churned'].mean())

y_preds = potential_churns.sort_values(['mean_diff_growth_churned_diff', 'feature_sum'], ascending=True).head(10)

print("storing y preds")
y_preds_lst = pd.DataFrame([{'ID': o, 'Date': tdy, 'Org Name': ''} for o in y_preds['id'].tolist()])
df_priorpreds = df_priorpreds.append(y_preds_lst, sort=True)
df_priorpreds['ID'] = df_priorpreds['ID'].astype(int)
save_dataframe_to_file("qgiv-stats-data", "preds.churn.csv", df_priorpreds)

print("report:")
print("-"*40)

labels = ['integrations', 'recent_logins', 'recent_created_users', 
          'mean_diff_growth_churned', 'zendesk_active']
for _, o in y_preds.iterrows():
    print("{} ({})".format(o['org_name'], int(o['id'])))
    print("; ".join(["{}: {}".format(l, o[l]) for l in labels]))