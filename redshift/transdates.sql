/* create table */
create table transdates (
    id        int       not null,
    date    timestamp null
);

/* ingest from S3 */
copy transdates
from 's3://trans-records/trans-dates.csv'
iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
emptyasnull
blanksasnull
fillrecord
delimiter ','
ignoreheader 1
region 'us-east-1';

/* copy from transdates to transactions */
update transactions_tag set date = transdates.date
from transdates where transactions_tag.id=transdates.id;

-- check update
select count(id) from transactions_tag where date=null;

/* clean up */
drop table transdates;