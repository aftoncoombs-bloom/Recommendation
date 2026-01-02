
import pandas as pd

#import sys
#sys.path.insert(1, '../../scripts/')
from s3_support import *


print("building donor_orgs data")

print("drop old values")
q = '''drop table if exists donors_orgs'''
redshift_query_write(q, schema='public')

print("calculate data")
q = '''select
            org,
            email as donor,
            max(extract('epoch' from date))::int - min(extract('epoch' from date))::int as activity_duration,
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
        into public.donors_orgs
        from production.transactions
        where
            status='A'
        group by org, email'''
redshift_query_write(q, schema='production')

print("DONE")