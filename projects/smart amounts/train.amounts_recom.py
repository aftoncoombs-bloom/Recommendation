import pandas as pd

import sys
sys.path.insert(1, '../webroot/')
#sys.path.insert(1, '../../scripts/')
from s3_support import *

print("Localizing transaction data")
q = '''select
            id,
            date,
            zip,
            state,
            amount,
            useragent
        from transactions
        where
            status='A' and
            recurring=0 and
            source in ('don_form', 'mobile', 'sms') and
            donations_amt>0'''
trans = redshift_query_read(q, schema='production')

print("Data prep")
print("\tstate cleanup")
us_states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 
    'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 
    'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 
    'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 
    'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

def state_fix(s):
    state_truncs = {'geor': 'GA', 'ohio': 'OH', 'cali': 'CA', 'fla': 'FL',
                    'flor': 'FL', 'hawa': 'HI', 'virg': 'VA', 'texa': 'TX',
                    'newy': 'NY', 'mich': 'MI', 'arka': 'AR', 'mass': 'MA',
                    'okla': 'OK', 'idah': 'ID', 'loui': 'LA', 'illi': 'IL',
                    'conn': 'CT', 'alas': 'AK', 'colo': 'CO', 'iowa': 'IA',
                    'kans': 'KS', 'wyom': 'WY', 'wisc': 'WI', 'wash': 'WA',
                    'verm': 'VT', 'utah': 'UT', 'tenn': 'TN', 'rhod': 'RI',
                    'oreg': 'OR', 'neva': 'NV', 'nebr': 'NE', 'indi': 'IN',
                    'mont': 'MT', 'alab': 'AL', 'miss': 'MS', 'penn': 'PA',
                    'dela': 'DE'}
    if str(s).lower() in state_truncs.keys():
        return state_truncs[str(s).lower()]
    
    return str(s).upper()

trans['state'] = trans['state'].apply(state_fix)
trans = trans[trans['state'].isin(us_states)]

print("\tuseragent cleanup")
def tag_platform(u):
    u = str(u)
    if 'iPhone' in u:
        return 'iPhone'
    elif 'iPad' in u:
        return 'iPad'
    elif 'Android' in u:
        return 'Android'
    elif 'IntelMacOSX' in u:
        return 'Mac'
    elif 'Windows' in u:
        return 'Windows'
    else:
        return u

trans['platform'] = trans['useragent'].apply(tag_platform)
trans = trans[trans['platform'].isin(['iPhone', 'iPad', 'Android', 'Mac', 'Windows'])]

print("\tflag dates")
trans['is_christmas'] = (trans['date'].dt.month==12)&(trans['date'].dt.day==25)
trans['is_newyears'] = (trans['date'].dt.month==12)&(trans['date'].dt.day.isin([30, 31]))

print("Building training data")
print("\tgrouping data")
grouping_cols = ['state', 'zip', 'platform', 
                 'is_christmas', 'is_newyears']
trans_grp_zip = trans.groupby(grouping_cols)['amount'].agg(['count', 'median']).reset_index()

grouping_cols = ['state', 'platform', 'is_christmas', 'is_newyears']
trans_grp_state = trans.groupby(grouping_cols)['amount'].agg(['count', 'median']).reset_index()
trans_grp_state['zip'] = None

grouping_cols = ['state', 'is_christmas', 'is_newyears']
trans_grp_state_noplat = trans.groupby(grouping_cols)['amount'].agg(['count', 'media']).reset_index()
trans_grp_state_noplat['zip'] = None
trans_grp_state_noplat['platform'] = None

print("\tmerging groups")
trans_grp_merged = trans_grp_zip.append(trans_grp_state)
trans_grp_merged = trans_grp_merged.append(trans_grp_state_noplat)

print("\t{:,} rows in merged data set".format(len(trans_grp_merged)))

print("\tsaving to CSV")
trans_grp_merged.to_csv("amounts.csv", index=False)

print("DONE")