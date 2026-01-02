
copy transactions
from 's3://trans-records/transactions.exp.csv'
iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
emptyasnull
blanksasnull
fillrecord
delimiter ','
ignoreheader 1
region 'us-east-1';

select distinct devicecategory from googleanalytics_traffic;

select * from stl_load_errors order by starttime desc;

select count(id), max(date) from analytics where date>='2022-02-15';

select * from transactions limit 5;
drop table public.org_donors;
select
       org,
       email as donor,
       year,
       count(id) as transactions,
       sum(amount) as vol,
       count(distinct(recurring)) as recurring,
       sum(purchases_quantity) as purchases,
       sum(donations_count) as donations,
       sum(events_count) as events,
       sum(registrations_count) as registrations,
       sum(auctiondonation_count) as auctiondonations,
       sum(auctionpurchase_count) as auctionpurchases,
       sum(gift_assist_count) as giftassist,
       sum(matchinggifts_count) as matchinggifts
into public.donor_retention_orgs
from production.transactions
where status='A'
group by org, email, year;

select
       org,
       form,
       email as donor,
       year,
       count(id) as transactions,
       sum(amount) as vol,
       count(distinct(recurring)) as recurring,
       sum(purchases_quantity) as purchases,
       sum(donations_count) as donations,
       sum(events_count) as events,
       sum(registrations_count) as registrations,
       sum(auctiondonation_count) as auctiondonations,
       sum(auctionpurchase_count) as auctionpurchases,
       sum(gift_assist_count) as giftassist,
       sum(matchinggifts_count) as matchinggifts
into public.donor_retention_forms
from production.transactions
where status='A'
group by org, form, email, year;