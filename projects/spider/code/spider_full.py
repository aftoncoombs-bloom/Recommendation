import requests, datetime
import pandas as pd
import json, os, time
from spider import crawl

import sys
sys.path.insert(1, '../../../scripts/')
from s3_support import *

# fetch org URL's
# id, dateCreated, dateLive, mail_addr_state, mail_addr_country, status, website
DOMAIN = "https://secure.qgiv.com/"
URL = "admin/qgivadmin/statistics/export_tables.php"

post_data = {'key': 'DSQR59VwyFhw21PKDF4K', 'table': 'org'}

print("querying for orgs from secure")
rsp = requests.post(DOMAIN + URL, data=post_data)
org_data = json.loads(rsp.text)
orgs = pd.DataFrame(org_data[0])
print("\tfetched {} entries, storing".format(len(orgs)))

orgs['url'] = orgs['website']
orgs.drop('website', axis=1, inplace=True)

# filter orgs to those that (1) are active and (2) we have a URL
orgs_to_crawl = orgs[(orgs['url']!='')&(orgs['status']==1)].copy()
orgs_to_crawl['url'] = orgs_to_crawl['url'].apply(str)
print("\t{} active orgs with URLs to crawl".format(len(orgs_to_crawl)))

len_orgs_to_crawl = len(orgs_to_crawl)

print("crawling {} org websites".format(len_orgs_to_crawl))
today = datetime.datetime.today().date()
orgs_site_data = None
counter = 0
start_time = time.time()
for _, r in orgs_to_crawl.iterrows():
    if 'qgiv.com' in r['url']:
        continue
    
    # crawl org site
    site_data = crawl(r['url'], suppress_errors=True)
    df_site_data = pd.DataFrame(site_data)
    df_site_data['org'] = r['id']
    df_site_data['date'] = today
    
    counter += 1
    if orgs_site_data is None:
        orgs_site_data = df_site_data
    else:
        orgs_site_data = pd.concat([orgs_site_data, df_site_data])
    
    # report counter
    if counter % 100 == 0:
        expired_time = (time.time() - start_time) / 60.
        print("\t{} of {} orgs complete, {:.1f} minutes".format(counter, len_orgs_to_crawl, expired_time))
        start_time = time.time()
        
        # update S3
        print("\tsending to S3")
        save_dataframe_to_file("qgiv-stats-data", "org_website.csv", orgs_site_data)

        
expired_time = (time.time() - start_time) / 60.
print("\t{} of {} orgs complete, {:.1f} minutes".format(counter, len_orgs_to_crawl, expired_time))
save_dataframe_to_file("qgiv-stats-data", "org_website.csv", orgs_site_data)

print("DONE CRAWLING ORGS")
# clean up potentially large local variables
del(orgs_site_data)
del(org_data)
print("LOADING DATA TO REDSHIFT")

cols = ['org', 'date', 'calls_to_action', 'iframe_source_blackbaud',
         'iframe_source_classy', 'iframe_source_donordrive', 'iframe_source_engagingnetworks',
         'iframe_source_facebook', 'iframe_source_giveeffect', 'iframe_source_givelively',
         'iframe_source_instagram', 'iframe_source_mobilecause', 'iframe_source_networkforgood',
         'iframe_source_onecause', 'iframe_source_paypal', 'iframe_source_qgiv',
         'iframe_source_stripe', 'iframe_source_twitter', 'image_count',
         'internal_links', 'link_target_blackbaud', 'link_target_classy',
         'link_target_donordrive', 'link_target_engagingnetworks', 'link_target_facebook',
         'link_target_giveeffect', 'link_target_givelively', 'link_target_instagram',
         'link_target_mobilecause', 'link_target_networkforgood', 'link_target_onecause',
         'link_target_paypal', 'link_target_qgiv', 'link_target_stripe',
         'link_target_twitter', 'outbound_links', 'script_source_blackbaud',
         'script_source_classy', 'script_source_donordrive', 'script_source_engagingnetworks',
         'script_source_facebook', 'script_source_giveeffect', 'script_source_givelively',
         'script_source_instagram', 'script_source_mobilecause', 'script_source_networkforgood',
         'script_source_onecause', 'script_source_paypal', 'script_source_qgiv',
         'script_source_stripe', 'script_source_twitter', 'url', 'word_count',
         'iframe_source_securegive', 'link_target_securegive', 'script_source_securegive']


df = get_dataframe_from_file("qgiv-stats-data", "org_website_csv")
df['date'] = pd.to_datetime(df['date'].min())

# filter out the redirects to social media pages
df = df[(df['url'].str.startswith('http'))&(~df['url'].str.startswith('https://twitter.com'))&(~df['url'].str.startswith('https://www.facebook.com'))&(~df['url'].str.startswith('https://www.linkedin.com'))&(~df['url'].str.startswith('https://www.google.com'))]

df.drop_duplicates('url', inplace=True)
df = df[~df['org'].isna()]

for c in cols:
    if c != 'date' and c != 'url':
        if c not in df.columns:
            df[c] = 0
        else:
            df[c] = df[c].fillna(0).astype('int')
    elif c == 'url':
        df[c] = df[c].apply(lambda x: x.replace(',', '').replace('\n', '')[:200])
        
# store to S3 & load to redshift
save_dataframe_to_file("qgiv-stats-data", "org_website.csv", df[cols])
redshift_query_write('''copy org_websites
                        from 's3://qgiv-stats-data/org_website.csv'
                        iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
                        emptyasnull
                        blanksasnull
                        fillrecord
                        delimiter ','
                        ignoreheader 1
                        region 'us-east-1'
                        ''', schema='production')

# verify new entries
date_count = redshift_query_read("select date, count(date) as count from org_websites group by date order by date desc limit 2", schema='production')

print(date_count)
print("DONE")