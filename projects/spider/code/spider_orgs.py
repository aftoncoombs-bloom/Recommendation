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
orgs['status'] = orgs['status'].astype(int)

# filter orgs to those that (1) are active and (2) we have a URL
orgs_to_crawl = orgs[(orgs['url']!='')&(orgs['status']==1)].copy()
orgs_to_crawl['url'] = orgs_to_crawl['url'].apply(str)
print("\t{} active orgs with URLs to crawl".format(len(orgs_to_crawl)))

len_orgs_to_crawl = len(orgs_to_crawl)

print("crawling {} org websites".format(len_orgs_to_crawl))
orgs_site_data = None
counter = 0
start_time = time.time()
for _, r in orgs_to_crawl.iterrows():
    if 'qgiv.com' in r['url']:
        continue
    elif ' or ' in r['url']:
        this_url = r['url'].split(' or ')
        r['url'] = this_url[0]
    
    # crawl org site
    site_data = crawl(r['url'], suppress_errors=True)
    df_site_data = pd.DataFrame(site_data)
    df_site_data['org'] = r['id']
    df_site_data['date'] = datetime.datetime.today().date()
    
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

print("DONE")


'''
print("Post:")
print("checking for orgs with new links to competitors or have dropped links to us")
# cleanup 
del(df_site_data)
del(orgs_to_crawl)

df = pd.read_csv(ORG_WEBSITE_DATA_PATH)

link_cols = [c for c in df.columns if 'link_target_' in c]
script_cols = [c for c in df.columns if 'script_source_' in c]

df_agg = df.groupby(['org', 'date'])[link_cols + script_cols].sum().reset_index().sort_values('date', ascending=False)

target_diffs = []
for o in df_agg['org'].unique():
    org_df = df_agg[df_agg['org']==o]
    for c in link_cols + script_cols:
        if org_df[c].iloc[0] != org_df[c].iloc[1]:
            target_diffs.append({'org': o, 'col_diff': c})
            
print("Done")
print("Target diffs:")
print(target_diffs)
'''