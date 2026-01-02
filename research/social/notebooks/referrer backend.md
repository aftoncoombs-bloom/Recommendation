# GA Referrer Backend

- date (datetime)
- org (int)
- form (int)
- views (int)
- path (string)
- source (string)
- qgiv_frontend (bool)
- p2p_frontend (bool)


```
drop table googleanalytics_referrer;
create table googleanalytics_referrer (
    date datetime null,
    org int null,
    form int null,
    views int not null default 0,
    path varchar(256) not null,
    source varchar(256) not null,
    qgiv_frontend boolean default false,
    p2p_frontend boolean default false
);
```


