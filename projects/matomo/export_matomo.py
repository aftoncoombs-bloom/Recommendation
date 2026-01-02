import requests, json, sys, time
from datetime import datetime, timedelta
import pandas as pd

# sys.path.append() for testing
sys.path.append('../../scripts/')
from s3_support import *


PRODUCTION_DOMAIN = 'https://main.matomo.qgiv.com'
STAGING_DOMAIN = 'https://main.matomo.qgiv.com:8443'

URL = '/?module=API&method=Live.getLastVisitsDetails&idSite=1'
URL += '&period=day&date={}&format=json&'
URL += 'token_auth={}&filter_limit={}&filter_offset={}'

AUTH_TOKEN = '20e9d5eeece2562bb882cb1e39f76828'


def pull_matomo_data(limit=10000, print_messages=False, testing=False, testing_entry_limit=None):
    data_to_return = None
    offset = 0
    if print_messages:
        print("starting data pull")
        
    # query to get last stored entry
    try:
        q = "select max(timestamp) as last_date from matomo_traffic"
        last_date = "{:%Y-%m-%d}".format(pd.to_datetime(redshift_query_read(q, schema='production')['last_date']).dt.date.iloc[0])
        
        if pd.isnull(last_date):
            last_date = '2022-09-01'
    except:
        # matomo start date
        last_date = '2022-09-01'
    
    file_counter = 0
    while True:
        if print_messages:
            print("\tlast date: {}; offset: {:,}".format(last_date, offset))

        # API call to localize [limit] entries
        visitors = matomo_api_call(last_date, limit, offset)
        
        if 'result' in visitors and visitors['result'] == 'error':
            print("Error:")
            print(visitors['message'])

            # likely memory issue, sleep for 30 seconds and try again
            time.sleep(30)
            continue

        if print_messages:
            print("\treceived {:,} visitor entries".format(len(visitors)))

        # extract page view entries from visitors logs
        page_views = []
        for visitor in visitors:
            page_views += extract_entry(visitor)

        if print_messages:
            print("\tprocessed visitor entries; storing {:,} page view entries".format(len(page_views)))

        # store page view entries
        if len(page_views) > 0:
            if not testing:
                # store to CSV
                new_filename = "matomo_update.{}-{}.csv".format(datetime.now().date(), file_counter)
                file_counter += 1
                df = pd.DataFrame(page_views)
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                df['form'] = pd.to_numeric(df['form'], errors='coerce').fillna(0).astype(int)
                df['org'] = pd.to_numeric(df['org'], errors='coerce').fillna(0).astype(int)
                df['url'] = df['url'].str.replace(',', '')
                df['url'] = df['url'].str.replace('"', '')
                df['url'] = df['url'].str.slice(0, 290)
                df['referrerName'] = df['referrerName'].str.replace(',', '')
                cols = ['id', 'ip', 'visitorId', 'visitDuration',
                        'actions', 'referrerType', 'referrerName',
                        'deviceType', 'deviceBrand', 'deviceModel',
                        'operatingSystemName', 'browser', 'url',
                        'timeSpent', 'pageviewPosition', 
                        'timestamp', 'org', 'form']
                if len(df) > 0:
                    save_dataframe_to_file("matomo-records", new_filename, df[cols], print_output=False)
                else:
                    print("\tno data to store in S3")
            else:
                if data_to_return is None:
                    data_to_return = page_views
                else:
                    data_to_return = data_to_return.append(page_views)
        
        # if we received fewer visitors than request limit...
        if len(visitors) < limit:
            if print_messages:
                print("\tDONE w {}".format(last_date))
            
            # increment date
            last_date_dt = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
            last_date = "{:%Y-%m-%d}".format(last_date_dt.date())
            
            # if last date is today...
            if datetime.strptime(last_date, "%Y-%m-%d").date() == datetime.today().date():
                # if not testing, data_to_return will be None
                return data_to_return
            else:
                # iterating to next day, clear offset
                offset = 0
        elif testing and testing_entry_limit is not None and len(data_to_return) >= testing_entry_limit:
            # testing, return processed page view data
            return data_to_return
        else:
            # continuing iterations for current date...
            offset += limit
    

def extract_entry(e):
    page_views = []
    
    universal_fields = ['idVisit', 'visitIp', 'visitorId', 
                        'visitDuration', 'actions', 'referrerType', 
                        'referrerName', 'deviceType', 'deviceBrand',
                        'deviceModel', 'operatingSystemName', 
                        'browser']
    # dimensions (form & org) in universal or action details?
    action_fields = ['url', 'timeSpent', 'pageviewPosition', 
                     'timestamp', "dimension1", "dimension2"]
    
    for e_action in e['actionDetails']:
        if e_action['type'] == 'action' and e_action['url'] is not None:
            page_view = {}
            for field in universal_fields:
                page_view[field] = e[field]
            try:
                for field in action_fields:
                    page_view[field] = e_action[field]
            except:
                print("ERROR")
                print(e_action)
                raise Exception()
            
            # redshift field prep
            page_view['url'] = page_view['url'].replace('\\', '')
            page_view['referrerName'] = page_view['referrerName'][:100]
            page_view['referrerType'] = page_view['referrerType'][:24]
            page_view['deviceType'] = page_view['deviceType'][:50]
            page_view['deviceBrand'] = page_view['deviceBrand'][:50]
            page_view['deviceModel'] = page_view['deviceModel'][:100]
            page_view['operatingSystemName'] = page_view['operatingSystemName'][:50]
            page_view['browser'] = page_view['browser'][:100]
            page_view['url'] = page_view['url'][:300]
            
            try:
                page_view['org'] = int(page_view['dimension1'])
            except:
                page_view['org'] = 0
            try:
                page_view['form'] = int(page_view['dimension2'])
            except:
                page_view['form'] = 0
                
            page_view['id'] = page_view['idVisit']
            page_view['ip'] = page_view['visitIp']
            del(page_view['dimension1'], page_view['dimension2'], page_view['idVisit'], page_view['visitIp'])
            page_views.append(page_view)
        
    return page_views


def matomo_api_call(last_date, limit, offset):
    # returns in reverse chronological order
    url = URL.format(last_date, AUTH_TOKEN, limit, offset)
    
    full_url = PRODUCTION_DOMAIN + url
    
    try:
        rsp = requests.get(full_url, verify=False)
    except:
        print("Error:")
        print(full_url)
        raise Exception()
    
    try:
        data = json.loads(rsp.text)
    except:
        print("Error:")
        print(full_url)
        raise Exception()
    
    return data