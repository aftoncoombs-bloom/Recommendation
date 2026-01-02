import pandas as pd
import numpy as np
from datetime import timedelta
import time

import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *

delta_week_1 = timedelta(weeks=1)
delta_week_4 = timedelta(weeks=4)
delta_week_12 = timedelta(weeks=12)
delta_week_24 = timedelta(weeks=24)
delta_week_52 = timedelta(weeks=52)

print("Drawing starting week dates from transactions")
trans = get_dataframe_from_file("trans-records", "transactions.csv")
trans = trans[trans['status']=='A']
trans['date'] = pd.to_datetime(trans['date'])
trans.sort_values('date', ascending=True, inplace=True)

print("\tcollecting org week dates")
org_data = []

for o in trans['org'].unique():
    data = {}
    _df = trans[trans['org']==o]
    start_date = _df['date'].min()
    
    data['id'] = o
    data['start_date'] = start_date
    data['wk_1_ex_date'] = start_date + delta_week_1
    data['wk_4_ex_date'] = start_date + delta_week_4
    data['wk_12_ex_date'] = start_date + delta_week_12
    data['wk_24_ex_date'] = start_date + delta_week_24
    data['wk_52_ex_date'] = start_date + delta_week_52
    
    wk_1_trans = _df[_df['date'] <= start_date + delta_week_1]['amount']
    data['wk_1_count'] = len(wk_1_trans)
    data['wk_1_sum'] = np.sum(wk_1_trans)
    
    wk_4_trans = _df[_df['date'] <= start_date + delta_week_4]['amount']
    data['wk_4_count'] = len(wk_4_trans)
    data['wk_4_sum'] = np.sum(wk_4_trans)
    
    wk_12_trans = _df[_df['date'] <= start_date + delta_week_12]['amount']
    data['wk_12_count'] = len(wk_12_trans)
    data['wk_12_sum'] = np.sum(wk_12_trans)
    
    wk_24_trans = _df[_df['date'] <= start_date + delta_week_24]['amount']
    data['wk_24_count'] = len(wk_24_trans)
    data['wk_24_sum'] = np.sum(wk_24_trans)
    
    wk_52_trans = _df[_df['date'] <= start_date + delta_week_52]['amount']
    data['wk_52_count'] = len(wk_52_trans)
    data['wk_52_sum'] = np.sum(wk_52_trans)
    
    org_data.append(data)

del(trans)
df_orgs = pd.DataFrame(org_data)

print("Tagging log data")
print("\tloading log data from S3")
logs = get_dataframe_from_file("qgiv-stats-data", "logs.csv")
logs['created'] = pd.to_datetime(logs['created'])
logs['org'] = logs['org'].fillna(0).astype(int)
logs['entity'] = logs['entity'].fillna(0).astype(int)
logs['entitytype'] = logs['entitytype'].fillna(0).astype(int)
logs['form'] = logs['form'].fillna(0).astype(int)
logs['systemtype'] = logs['systemtype'].fillna(0).astype(int)
logs['userid'] = logs['userid'].fillna(0).astype(int)
#logs['user'] = logs['user'].fillna(0).astype(int)
logs['systemid'] = logs['systemid'].fillna(0).astype(int)

logs['wk_1'] = False
logs['wk_4'] = False
logs['wk_12'] = False
logs['wk_24'] = False
logs['wk_52'] = False

logs_start_date = logs['created'].min()

print("\ttagging weeks in logs")
counter = 0
len_orgs = len(df_orgs)
start_time = time.time()
tagged_logs = None

for _, o in df_orgs[df_orgs['start_date']>logs_start_date].iterrows():
    ex_logs = logs[logs['org']==o['id']].copy()
    
    ex_logs['wk_1'] = ex_logs['created']<=o['wk_1_ex_date']
    ex_logs['wk_4'] = (ex_logs['created']>o['wk_1_ex_date'])&(ex_logs['created']<=o['wk_4_ex_date'])
    ex_logs['wk_12'] = (ex_logs['created']>o['wk_4_ex_date'])&(ex_logs['created']<=o['wk_12_ex_date'])
    ex_logs['wk_24'] = (ex_logs['created']>o['wk_12_ex_date'])&(ex_logs['created']<=o['wk_24_ex_date'])
    ex_logs['wk_52'] = (ex_logs['created']>o['wk_24_ex_date'])&(ex_logs['created']<=o['wk_52_ex_date'])
    
    if tagged_logs is None:
        tagged_logs = ex_logs
    else:
        tagged_logs = tagged_logs.append(ex_logs)
        
    counter += 1
    if counter % 50 == 0:
        print("\tdone with {} of {}, {:.2f} minutes".format(o['id'], counter, len_orgs, (time.time() - start_time) / 60.))
        start_time = time.time()
        tagged_logs.to_csv("org_week_tagged_logs.csv", index=False)

print("done")
tagged_logs.to_csv("org_week_tagged_logs.csv", index=False)
