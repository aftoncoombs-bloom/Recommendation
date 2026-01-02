SELECT *
FROM svv_all_schemas

create user segment password 'ty3&WPE$bqS8d';

create user mufaddalsanwari password 'ty3&WPE$bqS8d';
GRANT USAGE ON SCHEMA production TO mufaddalsanwari;
grant select on all tables in schema production to mufaddalsanwari;
GRANT USAGE ON SCHEMA pg_catalog TO mufaddalsanwari;
grant select on all tables in schema pg_catalog to mufaddalsanwari;
GRANT USAGE ON SCHEMA information_schema TO mufaddalsanwari;
grant select on all tables in schema information_schema to mufaddalsanwari;
GRANT USAGE ON SCHEMA public TO mufaddalsanwari;
grant select on all tables in schema public to mufaddalsanwari;
GRANT USAGE ON SCHEMA secure TO mufaddalsanwari;
grant select on all tables in schema secure to mufaddalsanwari;



truncate table public.control_panel_views;
insert into public.control_panel_views (
    select
       org,
       trunc(created) as date,
       replace(regexp_replace(regexp_replace(message, '[0-9]+\-[0-9]+\-[0-9]+', '[DATE]'), '\/[0-9]+\/?', '/[ID]/'), 'Page view: ', '') as url,
       count(date) as views
from production.syslog_logs
where
      message like '%Page view: %'
group by org, date, url);

select
       org, form, userid, entity, entitytype, message
from syslog_logs
where message not like '%Queue%' and message not like '%logged in%'
order by created desc limit 200;

select org, form, userid, entity, entitytype, message from logs where message like '%paused%' limit 100;


select count(t.id) / count(distinct t.org) as stat from transactions as t where t.date>='2022-06-03 12:15:26.802897' and status='A';
select * from organization limit 5;



select
    zip,
    state,
    platform,
    median(amount) as amount,
    count(id) as count,
    case when date_trunc('month', date) = 12 and date_trunc('day', date) = 25
        then True
        else False
    end as is_christmas,
    case when date_trunc('month', date) = 12 and (date_trunc('day', date) = 30 or date_trunc('day', date) = 31)
        then True
        else False
    end as is_newyears
from transactions
where
    status='A' and
    recurring=0 and
    source in ('don_form', 'mobile', 'sms') and
    donations_amt>0
group by zip, state, platform, is_christmas, is_newyears;

select count(id), count(distinct id), max(timestamp), min(timestamp) from matomo_traffic;
/*delete from matomo_traffic where timestamp>'2022-12-15';*/
select max(date) from googleanalytics_traffic;
select * from matomo_traffic order by timestamp desc limit 25;
select count(id), count(distinct id), max(created) from syslog_logs;
select distinct(status) from transactions;
select count(id), count(distinct id), max(date) from transactions;
select count(*) from matomo_traffic;

/* 60,474,094; 60,452,183 */
/* 60,473,856; 60,452,183 */
begin;
drop table if exists message_history_clean;
create table message_history_clean as select distinct * from message_history;
alter table message_history rename to message_history_old;
alter table message_history_clean rename to message_history;
drop table message_history_old;
grant select on all tables in schema production to segment;
commit;
select count(id) from syslog_logs;



select org, form, created, message from syslog_logs where message like '%Smart Amount%';
select min(created), max(created) from syslog_logs where message like '%Smart Amount%';

select distinct(pageviewposition) from matomo_traffic;


/*
 GA UNTAGGED ENTRIES
 */
/* 11-06-2022 GA: 110k */

select
    REPLACE(REGEXP_SUBSTR(path, 'formId=[[:digit:]]+'), 'formId=', '') as formid,
    REPLACE(REGEXP_SUBSTR(path, 'org=[[:digit:]]+'), 'org=', '') as orgid,
    path
from googleanalytics_traffic
where form=0
limit 100;

select date, path, views, REPLACE(REPLACE(REGEXP_SUBSTR(path, 'for/[[:alnum:]]+/?'), 'for/', ''), '/', '')
from googleanalytics_traffic
where form=0 and path not like '%account/%' and path not like '%event/%'
order by date desc limit 100;


select
    count(date) entries,
    sum(case when form=0 then 1 else 0 end) as untagged,
    untagged::float / entries::float as untagged_perc
from googleanalytics_traffic

select * from form where path='flightpaths'

/*
 55,089,949
 6,900,798; after regex formId: 4,960,587; after regex key=: 4,951,048
 1,940,211

 2,631,730 have key= or event/ in path
 9,539 have ?key=
 */

/* udpate queries */
update ga4_traffic
set form=REPLACE(REGEXP_SUBSTR(path, 'formId=[[:digit:]]+'), 'formId=', '')::int
where form=0 and path like '%formId=%' and REPLACE(REGEXP_SUBSTR(path, 'formId=[[:digit:]]+'), 'formId=', '')!='';
update ga4_traffic
set org=REPLACE(REGEXP_SUBSTR(path, 'org=[[:digit:]]+'), 'org=', '')::int
where org=0 and path like '%org=%';
update ga4_traffic
    set form=f.id
from form as f join ga4_traffic as ga on f.path=REPLACE(REGEXP_SUBSTR(ga.path, 'for/\\?key=[[:alnum:]]+'), 'for/?key=', '')
where ga.path like '%key=%' and ga.form=0;
update ga4_traffic
    set form=f.id
from form as f join ga4_traffic as ga on f.path=REPLACE(REPLACE(REGEXP_SUBSTR(ga.path, 'for/[[:alnum:]]+/?'), 'for/', ''), '/', '')
where ga.path like '%/for/%' and ga.form=0;




update matomo_traffic
set form=REPLACE(REGEXP_SUBSTR(url, 'formId=[[:digit:]]+'), 'formId=', '')::int
where form=0 and url like '%formId=%';
update matomo_traffic
set form=REPLACE(REGEXP_SUBSTR(url, '&form=[[:digit:]]+'), '&form=', '')::int
where form=0 and url like '%&form=%';
update matomo_traffic
set org=REPLACE(REGEXP_SUBSTR(url, 'org=[[:digit:]]+'), 'org=', '')::int
where org=0 and url like '%org=%';
update matomo_traffic
    set form=f.id
from form as f join matomo_traffic as ga on f.path=REPLACE(REGEXP_SUBSTR(ga.url, 'for/\\?key=[[:alnum:]-]+'), 'for/?key=', '')
where ga.url like '%key=%' and ga.form=0;
update matomo_traffic
    set form=f.id
from form as f join matomo_traffic as ga on f.path=REPLACE(REPLACE(REGEXP_SUBSTR(ga.url, 'for/[[:alnum:]-]+/?'), 'for/', ''), '/', '')
where ga.url like '%/for/%' and ga.form=0;


select id, path, REGEXP_SUBSTR(path, '[[:alnum:]-]+')
from production.form
where id=994529

select *
from production.matomo_traffic
where
    timestamp>='2022-10-18 11:00' and
    timestamp<'2022-10-18 11:56' and
    url like '%twgt%';



select
    date_trunc('month', date) as month,
    is_new_form,
    count(distinct(form)) as forms,
    count(distinct(id)) as trans_count_all,
    sum(amount) as trans_vol_all,
    count(distinct(case when recurring=0 then id else null end)) as trans_count_onetime,
    sum(case when recurring=0 then amount else null end) as trans_vol_onetime,
    avg(case when recurring=0 then amount else null end) as trans_mean_onetime,
    count(distinct(case when recurring!=0 and recurring_origin then id else null end)) as trans_count_recurring,
    sum(case when recurring=0 then amount else null end) as trans_vol_recurring,
    avg(case when recurring=0 then amount else null end) as trans_mean_recurring
from transactions
where
    status='A' and
    date>'2019-11-01'
group by date_trunc('month', date), is_new_form

select * from ga4_traffic order by date desc limit 25;
select min(date), max(date) from googleanalytics_traffic where form!=0;


select message from syslog_logs where message ilike '%express donate%'


/* merge GA tables */
drop table if exists production.ga;
drop table if exists production.ga_merged;
select
    date, org, form, path, devicecategory, qgiv_frontend, p2p_frontend, views::int, sessions, sessionduration, bounces
into production.ga_merged
from production.googleanalytics_traffic;
insert into production.ga_merged
    select date, org, form, path, devicecategory, qgiv_frontend, p2p_frontend, views::int, sessions, sessionduration, bounces
    from production.ga4_traffic;
select
    date, org, form, path, devicecategory, qgiv_frontend, p2p_frontend, max(views) as views,
    max(sessions) as sessions, max(sessionduration) as sessionduration, max(bounces) as bounces
into production.ga
from production.ga_merged
group by date, org, form, path, devicecategory, qgiv_frontend, p2p_frontend;
drop table production.ga_merged;
select count(*), max(date), min(date) from production.ga;

insert into production.ga (select
                    date, org, form, path, devicecategory, qgiv_frontend::int,
                    p2p_frontend::int, views::int, sessions, sessionduration, bounces
                from production.ga4_traffic as ga4
                where ga4.date>(select max(date) from production.ga));
select max(date) from production.ga;

/* donor retention */
insert into public.donor_retention_orgs_trailing
(
select
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
from production.transactions
where
    status='A' and
    date>=dateadd(month, -24, current_date)
group by org, email, date
)





drop table if exists public.form_aggregates;
select
    t.form as form,
    t.date as date,
    count(distinct(t.id)) as trans_count,
    count(distinct(case when t.recurring=0 then t.id else null end)) as trans_onetime_count,
    count(distinct(case when t.recurring_origin=1 then t.id else null end)) as trans_rec_count,
    sum(distinct(case when t.recurring=0 then t.amount else null end)) as trans_onetime_vol,
    sum(distinct(case when t.recurring_origin=1 then t.amount else null end)) as trans_rec_vol,
    sum(ga.views) as pageviews
into public.form_aggregates
from production.transactions as t
    left join production.ga as ga on t.form=ga.form and t.date=ga.date
where
    t.status='A'
group by t.form, t.date;

select count(*), min(date), max(date) from public.form_aggregates




select
    t.form,
    date_trunc('month', t.date) as month,
    count(distinct(t.id)) as trans_count,
    sum(t.amount) as trans_vol,
    count(distinct(case when recurring=0 or recurring_origin=1 then id else null end)) as trans_new_count,
    sum(case when recurring=0 or recurring_origin=1 then amount else null end) as trans_new_vol,
    avg(case when recurring=0 or recurring_origin=1 then amount else null end) as trans_avg_amount,
    count(distinct(case when recurring=0 then id else null end)) as trans_onetime,
    count(distinct(case when recurring_origin=1 then id else null end)) as trans_rec_origin,
    count(distinct(case when platform='desktop' and (recurring=0 or recurring_origin=1) then id else null end)) as trans_count_desktop,
    count(distinct(case when (platform='iPhone' or platform='Android') and (recurring=0 or recurring_origin=1) then id else null end)) as trans_count_mobile,
    sum(ga.views) as pageviews,
    sum(case when ga.devicecategory='desktop' then ga.views else null end) as pageviews_desktop,
    sum(case when ga.devicecategory='mobile' then ga.views else null end) as pageviews_mobile
from transactions as t
left join ga on t.form=ga.form and date_trunc('month', t.date)=date_trunc('month', ga.date)
where
    status='A'
group by t.form, date_trunc('month', t.date)




select user_id, session_id, start_time, query_text
from sys_query_history
where status='running'

cancel 1073815929


select
    date as month,
    avg(events_count) as events_yearround,
    count(distinct(case when conditional_fields>0 then form else null end)) as conditional_fields_forms,
    count(distinct(case when cta_before=1 then form else null end)) as cta_before_forms,
    count(distinct(case when cta_after=1 then form else null end)) as cta_after_forms
from public.analyticsqgiv_monthly
where date>='2022-11-01'
group by date

select distinct(cta_before) from public.analyticsqgiv_monthly
select date, form, cta_before, cta_after from public.analyticsqgiv_monthly limit 10;

select date as month, count(distinct(form))
from public.analyticsqgiv_monthly
where cta_before=1 and date>='2022-11-01'
group by date



select * from production.ga4_traffic_daily_device limit 5;
select * from production.ga4_traffic_daily_device where org!=0 limit 5;
select count(date) as rows, count(distinct(org)) as orgs, min(date), max(date) from production.ga4_traffic_daily_device;
select min(week) as min_date, max(week) as max_date from production.ga4_traffic_weekly; /* 23/7 > */
select min(week) as min_date, max(week) as max_date from production.ga4_traffic_weekly_device; /* 23/7 > */
select * from production.ga4_traffic_weekly_device where org!= 0 limit 5;

select
    date_trunc('day', date),
    count(case when recurring_origin=1 then id else null end) as recurring,
    count(case when recurring=0 then id else null end) as onetime
from production.transactions
where
    status='A'
group by date
order by date desc
limit 180


select
    date,
    count(distinct(org)) as orgs,
    count(distinct(form)) as forms,
    count(id) as trans_count,
    sum(amount) as trans_vol,
    sum(case when (recurring=0 or recurring_origin=1) then amount else null end) as trans_new_vol
from production.transactions
where status='A'
group by date order by date desc limit 30



select
    org,
    date_trunc(date, 'month') as month,
    count(distinct(id)) as trans_count,
    sum(amount) as trans_vol
from production.transactions
where
    status='A' and
    date>=dateadd(month,-2,current_date) and
    org in (452052, 445602, 451975, 446372, 446710, 447295, 448248, 445684, 445622, 449159, 446487, 449202, 450988, 446347, 450720, 449410, 447085, 446439, 448798, 445766, 445785, 446787, 447176, 448218, 449490, 446161, 445749, 451407, 445649, 446233, 449922, 447231, 447410, 450975, 447022, 446704, 447802, 445659, 446580, 445438, 446124, 447456, 446202, 445856, 446474, 447078, 446636, 447008)
group by org, date_trunc(date, 'month')


/**
  UPDATE FORM AGGREGATES TABLE (BENCHMARKS API)
 */
select count(org) as rows, max(date) from public.form_aggregates;
drop table if exists public.form_aggregates;
select
    t.org as org,
    t.form as form,
    t.date as date,
    count(distinct(t.id)) as trans_count,
    count(distinct(case when t.recurring=0 then t.id else null end)) as trans_onetime_count,
    count(distinct(case when t.recurring_origin=1 then t.id else null end)) as trans_rec_count,
    sum(distinct(case when t.recurring=0 then t.amount else null end)) as trans_onetime_vol,
    sum(distinct(case when t.recurring_origin=1 then t.amount else null end)) as trans_rec_vol,
    sum(ga.views) as pageviews
into public.form_aggregates
from production.transactions as t
    left join production.ga as ga on t.form=ga.form and t.date=ga.date
where
    t.status='A'
group by t.org, t.form, t.date;
select count(org) as rows, max(date) from public.form_aggregates;


select * from production.auctionitem
select count(date) from production.auctionbids

select count(distinct(id)) from production.auctionitem
select * from production.auctionitem limit 4

select * from production.analyticsauction limit 5;
select
    ab.form,
    max(aa.items_auction) as max_items_auction,
    max(aa.bids) as max_bids,
    sum(aa.bids) as sum_bids,
    max(aa.items_bid_on) as max_items_bid_on,
    sum(aa.items_bid_on) as sum_items_bid_on
from production.analyticsauction as aa
    left join production.analytics as ab on aa.id_hash=ab.id_hash
group by ab.form;

