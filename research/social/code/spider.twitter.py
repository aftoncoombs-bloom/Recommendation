'''
Twitter limits free API access results to past 7 days and 100,000 requests per day and 180 requests per 15 minutes for search requests. (https://developer.twitter.com/ja/docs/basics/rate-limits)

Workflow:
1. pull forms data in order to build dataset of URL's to search for
    - account for qgiv vs p2p; how to deal with widgets?
    - should we search for org website shares?
2. paced iteration through all form URL's to retrieve shares from social media
3. store shares to redshift 

- get widget embed URL for widgets
'''
import time, tweepy, sys
import pandas as pd
sys.path.insert(1, '../../../scripts/')
from s3_support import *

CONSUMER_KEY = "aqB8jd0zgfMs4N9XNn6BA"
CONSUMER_SECRET = "LsitOJMTvsksgYHlwlW3PQSPlMBh2WyS0vmS1PnGs"


# load form data
# @TODO update production.form table & associated export with Form.type
# @TODO can we build reliable URL's from path alone?
forms = redshift_query_read("select id, org, type, path from form where status=1", schema="production")

seconds_delay = max(float(len(forms)) / float(100000), 1.0)
# 180 requests per 15 minutes
seconds_delay = 5.0
counter = 0

print("TWITTER SPIDER: crawling {} forms with a {} second delay between requests".format(len(forms), seconds_delay))
days_to_complete = (((len(forms) * seconds_delay) / 60.) / 60.) / 24.
print("\tapproximately {:.2f} days".format(days_to_complete))

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

data = []
counter = 0

for _, form in forms.iterrows():
    # build form URL to search for
    if form['type'] == 3:
        # p2p2 formatting
        form_url = "url:secure.qgiv.com/event/{}".format(form['path'])
    else:
        # qgiv formatting
        form_url = "url:secure.qgiv.com/for/{}".format(form['path'])

    if form_url is not None and form_url != "":
        for e in tweepy.Cursor(api.search, q=form_url).items():
            data.append({
                'tweet_id': e.id,
                'twitter_user_id': e.user.id,
                'org': form['org'],
                'form': form['id'],
                'url': form_url,
                'date_created': e.created_at,
                'content': e.text,
                'retweet_count': e.retweet_count,
                'like_count': e.favorite_count,
                'hashtags': ";".join([t['text'] for t in e.entities['hashtags']])
            })

        # delay until next iteration
        time.sleep(seconds_delay)
    
    counter += 1
    if counter % 2500 == 0 and counter > 0 and len(data) > 0:
        print("\tTWITTER SPIDER: done with {} forms".format(counter))
        save_dataframe_to_file("qgiv-stats-data", "social.twitter.csv", pd.DataFrame(data))
        
print("TWITTER SPIDER: complete, clearing duplicates & loading to redshift")
twitter_shares = redshift_query_read("select * from social_shares_twitter")
twitter_shares = twitter_shares.append(pd.DataFrame(data)).drop_duplicates(subset=['id', 'created'], keep='last')
save_dataframe_to_file("qgiv-stats-data", "social.twitter.csv", twitter_shares)

# wipe current data
q = "truncate social_shares_twitter"
redshift_query_write(q, schema="public")
# load to redshift table
q = '''copy social_shares_twitter
        from 's3://qgiv-stats-data/social.twitter.csv'
        iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
        emptyasnull
        blanksasnull
        fillrecord
        delimiter ','
        ignoreheader 1
        region 'us-east-1';'''
redshift_query_write(q, schema="public")