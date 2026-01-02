'''
Facebook limits API access to 200 requests per hour.

Workflow:
1. pull forms data in order to build dataset of URL's to search for
    - account for qgiv vs p2p; how to deal with widgets?
    - should we search for org website shares?
2. paced iteration through all form URL's to retrieve shares from social media
3. store shares to redshift 

- get widget embed URL for widgets

Facebook API notes:
- https://developers.facebook.com/docs/graph-api/reference/v8.0/url
'''
import time, facebook, sys
import pandas as pd
sys.path.insert(1, '../../../scripts/')
from s3_support import *

# request new token each time
# app id: 380047073336642
# app secret: 667d0e2781b50e38e38a8cfd1a8284b9
APP_ID = "380047073336642"
APP_SECRET = "667d0e2781b50e38e38a8cfd1a8284b9"

# load form data
# @TODO update production.form table & associated export with Form.type
# @TODO can we build reliable URL's from path alone?
forms = redshift_query_read("select id, org, type, path from form where status=1", schema="production")
facebook_shares = redshift_query_read("select * from social_shares_facebook")

seconds_delay = 20.
counter = 0

print("FACEBOOK SPIDER: crawling {} forms with a {} second delay between requests".format(len(forms), seconds_delay))
days_to_complete = (((len(forms) * seconds_delay) / 60.) / 60.) / 24.
print("\tapproximately {:.2f} days".format(days_to_complete))

api = facebook.GraphAPI(access_token="{}|{}".format(APP_ID, APP_SECRET), version="2.12")
            
for _, form in forms.iterrows():
    # build form URL to search for
    if form['type'] == 3:
        # p2p2 formatting
        form_url = "https://secure.qgiv.com/event/{}".format(form['path'])
    else:
        # qgiv formatting
        form_url = "https://secure.qgiv.com/for/{}".format(form['path'])

    if form_url is not None and form_url != "":
        fb_query = "v9.0?id={}&fields=engagement".format(form_url)

        try:
            # query facebook for search results
            results = api.request(fb_query)

            # process & store results
            if 'engagement' in results:
                # process url info
                data = {
                    'org': form['org'],
                    'form': form['id'],
                    'url': form_url,
                    'reaction_count': results['engagement']['reaction_count'],
                    'comment_count': results['engagement']['comment_count'],
                    'share_count': results['engagement']['share_count']
                }

                # store url info & keep most recent
                facebook_shares = facebook_shares.append(pd.DataFrame([data]), sort=False)
        except Exception as e:
            print("Exception: {}".format(e))
            
        # delay until next iteration
        time.sleep(seconds_delay)

    counter += 1
    if counter % 2500 == 0 and counter > 0:
        print("\t\tFACEBOOK SPIDER: done with {} forms".format(counter))
        # store to csv
        facebook_shares = facebook_shares.drop_duplicates(subset=['url', 'form'], keep='last')
        cols = ['org', 'form', 'url', 'reaction_count', 'comment_count', 'share_count']
        save_dataframe_to_file("qgiv-stats-data", "social.facebook.csv", facebook_shares[cols])
    
cols = ['org', 'form', 'url', 'reaction_count', 'comment_count', 'share_count']
save_dataframe_to_file("qgiv-stats-data", "social.facebook.csv", facebook_shares[cols])
    
print("\tFACEBOOK SPIDER: complete, loading to redshift")
# wipe the current data
q = "truncate social_shares_facebook"
redshift_query_write(q, schema="public")

# load to redshift table
q = '''copy social_shares_facebook
        from 's3://qgiv-stats-data/social.facebook.csv'
        iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
        emptyasnull
        blanksasnull
        fillrecord
        delimiter ','
        ignoreheader 1
        region 'us-east-1';'''
redshift_query_write(q, schema="public")