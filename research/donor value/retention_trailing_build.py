
import pandas as pd

#import sys
#sys.path.insert(1, '../../scripts/')
from s3_support import *


print("building donor_orgs_trailing data")

print("\tdrop old values")
q = '''drop table if exists donors_orgs_trailing'''
redshift_query_write(q, schema='public')

print("\tcalculate 12 to 24 months")
q = '''select
            org,
            email as donor,
            (case
                when date>=dateadd(month, -12, current_date) then 1
                when date>=dateadd(month, -24, current_date) and date<dateadd(month, -12, current_date) then 2
                else null
            end) as past_twelve,
            count(id) as transactions,
            sum(amount) as volume,
            count(distinct(case when recurring!=0 then recurring else null end)) as recurring,
            sum(purchases_quantity) as purchases,
            sum(donations_count) as donations,
            sum(events_count) as events,
            sum(registrations_count) as registrations,
            sum(auctiondonation_count) as auctiondonations,
            sum(auctionpurchase_count) as auctionpurchases,
            sum(gift_assist_count) as giftassist,
            sum(matchinggifts_count) as matchinggifts
        into public.donors_orgs_trailing
        from production.transactions
        where
            status='A' and
            date>=dateadd(month, -24, current_date)
        group by org, email, date'''
redshift_query_write(q, schema='production')

q = '''select * from donor_orgs_trailing'''
df = redshift_query_read(q, schema='public')
print("\tdonor_orgs_trailing done, {:,} rows".format(len(df)))

print("building orgs_retention_trailing data")

print("\tdrop old values")
q = '''truncate table org_retention'''
redshift_query_write(q, schema='public')

print("\titerating through orgs to calculate 12, 12 to 24")
org_data = []
for org in df['org'].unique():
    _df = df[df['org']==org]
    rolling_12 = _df[_df['past_twelve']==1]
    rolling_12_24 = _df[_df['past_twelve']==2]
    
    if len(rolling_12_24) == 0 or len(rolling_12) == 0:
        # skip orgs with insufficient activity
        continue
    
    retained_donors = len(rolling_12[rolling_12['donor'].isin(rolling_12_24['donor'])])
    churned_donors = len(rolling_12_24[~rolling_12_24['donor'].isin(rolling_12['donor'])])
    new_donors = len(rolling_12[~rolling_12['donor'].isin(rolling_12_24['donor'])])
    if rolling_12_24['volume'].mean() == 0:
        mean_value = 0
    else:
        mean_value = (rolling_12['volume'].mean() - rolling_12_24['volume'].mean()) / rolling_12_24['volume'].mean()
    if rolling_12_24['volume'].median() == 0:
        median_value = 0
    else:
        median_value = (rolling_12['volume'].median() - rolling_12_24['volume'].median()) / rolling_12_24['volume'].median()
    
    org_data.append({
        'org': org,
        'retention': retained_donors / len(rolling_12_24),
        'churn': churned_donors / len(rolling_12_24),
        'new_donors': new_donors / len(rolling_12),
        'mean_value_change': mean_value,
        'median_value_change': median_value
    })
    

orgs_retention = pd.DataFrame(org_data)
print("\torg retention values compiled; {:,} orgs, {:,} rows".format(len(orgs_retention['org'].unique()), len(orgs_retention)))

print("\tstoring to redshift")
save_dataframe_to_file('qgiv-stats-data', 'org_retention.csv', orgs_retention)

q = '''copy org_retention
        from 's3://qgiv-stats-data/{}'
        iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
        emptyasnull
        blanksasnull
        fillrecord
        delimiter ','
        ignoreheader 1
        region 'us-east-1';'''.format('org_retention.csv')

redshift_query_write(q, schema='public')

print("DONE")