import datetime, requests, json, time
import pandas as pd

import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *

from export_matomo import extract_entry

PRODUCTION_DOMAIN = 'https://main.matomo.qgiv.com'

URL = '/?module=API&method=Live.getLastVisitsDetails&idSite=1'
URL += '&period=day&date={}&format=json&'
URL += 'token_auth={}&filter_limit={}&filter_offset={}'

AUTH_TOKEN = '20e9d5eeece2562bb882cb1e39f76828'


def store_matomo_file(data, filename):
    df = pd.DataFrame(data)
    df = df.drop_duplicates()
    print("\t\tstoring {:,} entries, {} - {}".format(len(df), df['timestamp'].min(), df['timestamp'].max()))
    
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
        save_dataframe_to_file("ingest-records", filename, df[cols], print_output=False)
    else:
        print("\tno data to store in S3")


def backfill_month(month=None, year=None, limit=2500):
    if month is None or year is None:
        raise Exception("Bad input: month or year")
        
    current_date = datetime.datetime(year=year, month=month, day=6)
    while current_date.month == month:
        page_views = []
        date_param = "{:%Y-%m-%d}".format(current_date)
        offset = 0
        
        print("starting to export {}".format(date_param))
        counter = 1
        file_counter = 1
        while True:
            url = URL.format(date_param, AUTH_TOKEN, limit, offset)
            rsp = requests.get(PRODUCTION_DOMAIN + url)
            data = json.loads(rsp.text)
            
            if 'result' in data and data['result'] == 'error':
                # likely memory issue, sleep for 5 seconds and try again
                time.sleep(5)
                continue
                
            for visitor in data:
                try:
                    page_views += extract_entry(visitor)
                except Exception as e:
                    print("\t\t{}: {}".format(e, visitor[:10]))
                    return data
            
            print("\titeration {} complete, {:,} entries".format(counter, len(page_views)))
            
            if len(data) < limit:
                # end of day's data
                break
            else:
                if counter % 10 == 0:
                    filename = "matomo_update.{}.{}.csv".format(date_param, file_counter)
                    store_matomo_file(page_views, filename)
                    file_counter += 1
                    page_views = []
                
                offset += limit
                counter += 1  
        
        # store days data
        if len(page_views) > 0:
            print("\tstoring {:,} visitor logs".format(len(page_views)))
            
            filename = "matomo_update.{}.csv".format(date_param)
            store_matomo_file(page_views, filename)
        else:
            print("\tERROR: no visitor logs on {}".format(date_param))
        
        # increment date
        current_date += datetime.timedelta(days=1)
    
    print("DONE")
    
    
error_entry = backfill_month(month=12, year=2022)