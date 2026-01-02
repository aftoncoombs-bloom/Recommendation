import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *


'''
Pre-requisites:

- updated GA table

Process:

1. create (temp) median amount tables
    - redshift won't allow the mix of median with other aggregate functions so we're creating individual tables for these values
2. update stats table with broad system wide statistics
3. update stats per form
'''

start_date = '2023-10-01'

print("Create platform wide aggregates")
'''
1. create (temp) median amount tables
'''
print("\tremoving temp tables possibly still here from last run; also production.stats")
# drop temp tables in case they are still around
cleanup_queries = [
    '''drop table if exists production.mdn_onetime''',
    '''drop table if exists production.mdn_recurring''',
    '''drop table if exists production.stats'''
]
for q in cleanup_queries:
    redshift_query_write(q, schema='production')

print("\tcreating temp tables for medians")
# median one time
q = '''select
            date_trunc('month', date) as month,
            median(case when recurring=0 then amount else null end) as trans_mdn_onetime
        into production.mdn_onetime
        from production.transactions
        where status='A' and date>='{}'
        group by date_trunc('month', date)'''.format(start_date)
redshift_query_write(q, schema='production')

# median recurring
q = '''select
            date_trunc('month', date) as month,
            median(case when recurring_origin=1 then amount else null end) as trans_mdn_rec
        into production.mdn_recurring
        from production.transactions
        where status='A' and date>='{}'
        group by date_trunc('month', date)'''.format(start_date)
redshift_query_write(q, schema='production')

    
print("\tbuilding aggregate table query")
'''
2. update stats table
'''
# broad base stats
#     we use the agg function max() on median tables to avoid having to group on them, there will be only
#     one value per month so this function does nothing

# base
fields = [
    "date_trunc('month', t.date) as month",
    "count(distinct(t.org)) as orgs",
    "count(distinct(t.form)) as forms",
    "count(distinct(t.email)) as donors",
    "count(distinct(t.id)) as trans_count",
    "sum(t.amount) as trans_vol",
    "count(distinct(case when recurring=0 or recurring_origin=1 then id else null end)) as trans_new_count",
    "sum(case when recurring=0 or recurring_origin=1 then amount else null end) as trans_new_vol",
    "avg(case when recurring=0 or recurring_origin=1 then amount else null end) as trans_avg_amount"
]
# one time vs recurring
fields += [
    "count(distinct(case when recurring=0 then id else null end)) as trans_onetime",
    "avg(case when recurring=0 then amount else null end) as trans_avg_onetime",
    "max(mo.trans_mdn_onetime) as trans_mdn_onetime",
    "count(distinct(case when recurring_origin=1 then id else null end)) as trans_rec_origin",
    "avg(case when recurring_origin=1 then amount else null end) as trans_avg_rec",
    "max(mr.trans_mdn_rec) as trans_mdn_rec"
]
# platform (desktop, mobile, tablet)
fields += [
    "count(distinct(case when (platform='Windows' or platform='Mac') and (recurring=0 or recurring_origin=1) then id else null end)) as trans_count_desktop",
    "count(distinct(case when (platform='iPhone' or platform='Android') and (recurring=0 or recurring_origin=1) then id else null end)) as trans_count_mobile",
    "sum(ga.views) as pageviews",
    "sum(case when ga.devicecategory='desktop' then ga.views else null end) as pageviews_desktop",
    "sum(case when ga.devicecategory='mobile' then ga.views else null end) as pageviews_mobile",
    "sum(case when ga.devicecategory='tablet' then ga.views else null end) as pageviews_tablet"
]
# transaction types (express checkout, gift assist)
fields += [
    "count(distinct(case when t.isexpresscheckout then t.form else null end)) as expressdonate_forms",
    "sum(t.isexpresscheckout::int) as expressdonate_count",
    "sum(case when t.isexpresscheckout then t.amount else null end) as expressdonate_vol",
    "count(distinct(case when t.gift_assist_count then t.form else null end)) as giftassist_forms",
    "sum(t.gift_assist_count) as giftassist_count",
    "sum(t.gift_assist_amt) as giftassist_vol"
]

print("\texecuting aggregate table query")
q = '''select {}
        into production.stats
        from production.transactions as t
            left join production.ga on date_trunc('month', t.date)=date_trunc('month', ga.date)
            left join production.mdn_onetime as mo on date_trunc('month', t.date)=mo.month
            left join production.mdn_recurring as mr on date_trunc('month', t.date)=mr.month
        where
            t.status='A' and t.date>='{}'
        group by date_trunc('month', t.date)'''.format(", ".join(fields), start_date)
redshift_query_write(q, schema='production')


print("\tcleaning up temp tables")
# clean up temp tables
cleanup_queries = [
    '''drop table if exists production.mdn_onetime''',
    '''drop table if exists production.mdn_recurring'''
]
for q in cleanup_queries:
    redshift_query_write(q, schema='production')
    
    

print("Create form aggregates")
'''
3. update stats per form
'''
print("\tremoving temp tables possibly still here from last run; also production.stats_forms")
# drop temp tables in case they are still around
cleanup_queries = [
    '''drop table if exists production.mdn_onetime_forms''',
    '''drop table if exists production.mdn_recurring_forms''',
    '''drop table if exists production.stats_forms'''
]
for q in cleanup_queries:
    redshift_query_write(q, schema='production')

print("\tcreating temp tables for medians")
# median one time
q = '''select
            form,
            date_trunc('month', date) as month,
            median(case when recurring=0 then amount else null end) as trans_mdn_onetime
        into production.mdn_onetime_forms
        from production.transactions
        where status='A' and date>='{}'
        group by form, date_trunc('month', date)'''.format(start_date)
redshift_query_write(q, schema='production')

# median recurring
q = '''select
            form,
            date_trunc('month', date) as month,
            median(case when recurring_origin=1 then amount else null end) as trans_mdn_rec
        into production.mdn_recurring_forms
        from production.transactions
        where status='A' and date>='{}'
        group by form, date_trunc('month', date)'''.format(start_date)
redshift_query_write(q, schema='production')


print("\tcreating aggregate table query")
# create agg table
# base
fields = [
    "t.form",
    "f.type as product",
    "f.template as frontend_template",
    "date_trunc('month', t.date) as month"
]
# base processing
fields += [
    "count(distinct(t.id)) as trans_count",
    "sum(t.amount) as trans_vol",
    "count(distinct(case when t.recurring=0 or t.recurring_origin=1 then t.id else null end)) as trans_new_count",
    "sum(case when t.recurring=0 or t.recurring_origin=1 then amount else null end) as trans_new_vol",
    "avg(case when t.recurring=0 or t.recurring_origin=1 then t.amount else null end) as trans_avg_amount"
]
# onetime vs recurring
fields += [
    "count(distinct(case when t.recurring=0 then t.id else null end)) as trans_onetime",
    "avg(case when t.recurring=0 then t.amount else null end) as trans_avg_onetime",
    "mot.trans_mdn_onetime as trans_mdn_onetime",
    "count(distinct(case when t.recurring_origin=1 then t.id else null end)) as trans_rec_origin",
    "avg(case when t.recurring_origin=1 then t.amount else null end) as trans_avg_rec",
    "mor.trans_mdn_rec as trans_mdn_rec"
]
# platform (desktop, mobile, tablet)
fields += [
    "count(distinct(case when (t.platform='Windows' or t.platform='Mac') and (recurring=0 or recurring_origin=1) then t.id else null end)) as trans_count_desktop",
    "count(distinct(case when (t.platform='iPhone' or t.platform='Android') and (t.recurring=0 or t.recurring_origin=1) then t.id else null end)) as trans_count_mobile",
    "sum(ga.views) as pageviews",
    "sum(case when ga.devicecategory='desktop' then ga.views else null end) as pageviews_desktop",
    "sum(case when ga.devicecategory='mobile' then ga.views else null end) as pageviews_mobile"
]
# transaction types (gift assist, express donate)
fields += [
    "sum(t.isexpresscheckout::int) as expressdonate_count",
    "count(distinct(case when t.isexpresscheckout and (t.recurring=0 or t.recurring_origin=1) then t.id else null end)) as expressdonate_new_count",
    "sum(t.amount) as expressdonate_vol",
    "sum(case when t.isexpresscheckout and (t.recurring=0 or t.recurring_origin=1) then t.amount else null end) as expressdonate_new_vol",
    "sum(t.gift_assist_count) as giftassist_count",
    "sum(t.gift_assist_amt) as giftassist_vol"
]

print("\texecuting aggregate table query")
fields += ['rep_forms=0']
q = '''select {}
        into production.stats_forms
        from production.transactions as t
            left join production.ga on t.form=ga.form and date_trunc('month', t.date)=date_trunc('month', ga.date)
            left join production.mdn_onetime_forms as mot on date_trunc('month', t.date)=mot.month and t.form=mot.form
            left join production.mdn_recurring_forms as mor on date_trunc('month', t.date)=mor.month and t.form=mor.form
            left join production.form as f on t.form=f.id
        where
            t.status='A' and t.date>='{}'
        group by t.form, date_trunc('month', t.date)'''.format(", ".join(fields), start_date)
redshift_query_write(q, schema='production')


print("\tcleaning up temp tables")
# clean up temp tables
cleanup_queries = [
    '''drop table if exists production.mdn_onetime_forms''',
    '''drop table if exists production.mdn_recurring_forms'''
]
for q in cleanup_queries:
    redshift_query_write(q, schema='production')
    

# adding representative form tag value
print("\ttagging representative forms")
q = '''update stats_forms set rep_forms=1 where form in (select form from representative_forms)'''
#redshift_query_write(q, schema='production')


print("DONE")