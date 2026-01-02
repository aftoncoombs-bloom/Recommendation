import pandas as pd
from s3_support import *


def cache_recommended_amounts():
    # one time
    trans = get_onetime_amounts()

    # recurring
    rec = get_recurring_amounts()

    # merge one time and recurring
    trans = trans.merge(rec, on=['zip', 'state', 'platform', 'is_christmas', 
    'is_newyears']).drop_duplicates()

    # store to S3
    print("storing to S3 ({:,} entries)".format(len(trans)))
    bucket = 'qgiv-stats-data'
    filename = 'recommended_amounts.cache.csv'
    save_dataframe_to_file(bucket, filename, trans, print_output=False)

    print("DONE")


def get_onetime_amounts():
    print("get_onetime_amounts()")
    # query zip, state, platform, xmas & new years
    q = '''select
                zip,
                state,
                platform,
                median(amount) as amount,
                count(id) as count,
                case 
                    when date_part('month', date) = 12 and date_part('day', date) = 25
                        then True
                        else False
                end as is_christmas,
                case 
                    when date_part('month', date) = 12 and (date_part('day', date) = 30 or date_part('day', date) = 31)
                        then True
                        else False
                end as is_newyears
            from transactions
            where
                status='A' and
                recurring=0 and
                source in ('don_form', 'mobile', 'sms') and
                donations_amt>0
            group by zip, state, platform, is_christmas, is_newyears;'''
    trans = redshift_query_read(q, schema='production')

    # query for state, platform, xmas & new years
    q = '''select
                state,
                platform,
                median(amount) as amount,
                count(id) as count,
                case 
                    when date_part('month', date) = 12 and date_part('day', date) = 25
                        then True
                        else False
                end as is_christmas,
                case 
                    when date_part('month', date) = 12 and (date_part('day', date) = 30 or date_part('day', date) = 31)
                        then True
                        else False
                end as is_newyears
            from transactions
            where
                status='A' and
                recurring=0 and
                source in ('don_form', 'mobile', 'sms') and
                donations_amt>0
            group by state, platform, is_christmas, is_newyears;'''
    trans_nozip = redshift_query_read(q, schema='production')
    trans_nozip['zip'] = None
    
    trans = pd.concat([trans, trans_nozip])

    platforms = ['iPhone', 'iPad', 'Android', 'Mac', 'Windows']
    trans = trans[trans['platform'].isin(platforms)]
    
    # query for state, xmas & new years
    q = '''select
                state,
                median(amount) as amount,
                count(id) as count,
                case 
                    when date_part('month', date) = 12 and date_part('day', date) = 25
                        then True
                        else False
                end as is_christmas,
                case 
                    when date_part('month', date) = 12 and (date_part('day', date) = 30 or date_part('day', date) = 31)
                        then True
                        else False
                end as is_newyears
            from transactions
            where
                status='A' and
                recurring=0 and
                source in ('don_form', 'mobile', 'sms') and
                donations_amt>0
            group by state, is_christmas, is_newyears;'''
    trans_nozipplatform = redshift_query_read(q, schema='production')
    trans_nozipplatform['zip'] = None
    trans_nozipplatform['platform'] = None
    
    trans = pd.concat([trans, trans_nozipplatform])
    
    us_states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 
        'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
        'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
        'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 
        'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 
        'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 
        'WV', 'WI', 'WY'
    ]

    trans['state'] = trans['state'].apply(state_fix)
    trans = trans[trans['state'].isin(us_states)]
    
    # de-duping from malformed state names
    grp = ['zip', 'state', 'platform', 'is_christmas', 
            'is_newyears']
    trans = trans.groupby(grp)[['count', 'amount']].max().reset_index()
    trans['onetime'] = trans['amount']
    trans.drop('amount', axis=1, inplace=True)

    return trans


def get_recurring_amounts():
    print("get_recurring_amounts()")
    # localize recurring transactions
    q = '''select
            recurring,
            id,
            date,
            amount,
            zip,
            state,
            platform
        from transactions
        where
            status='A' and
            recurring!=0 and
            source in ('don_form', 'mobile', 'sms')'''
    rec = redshift_query_read(q, schema='production')

    # get counts per recurring ID
    rec_counts = rec.groupby('recurring')['id'].count().reset_index()
    rec_counts.columns = ['recurring', 'count']

    # iterate through recurring to calculate mean difference between dates
    rec_data = []
    for r in rec_counts[rec_counts['count']>1]['recurring'].tolist():
        this_rec = rec[rec['recurring']==r].sort_values('date', ascending=True)
        
        date_diff = this_rec['date'].diff().mean()

        rec_data.append({
            'recurring': r,
            'date_diff': date_diff
        })

    freq_df = pd.DataFrame(rec_data)
    # merge frequency data to get amount, zip, state & platform
    rec = freq_df.merge(rec[['recurring', 'amount', 'zip', 'state', 'platform']], on='recurring').drop_duplicates('recurring', keep='last')

    # normalize frequency & state
    rec['frequency'] = rec['date_diff'].apply(get_frequency)
    rec['state'] = rec['state'].apply(state_fix)

    us_states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DC', 
        'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
        'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
        'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 
        'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 
        'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 
        'WV', 'WI', 'WY'
    ]
    rec = rec[rec['state'].isin(us_states)]

    # zip, state, platform, frequency
    grp = ['zip', 'state', 'platform', 'frequency']
    rec_grp = rec.groupby(grp)['amount'].median().reset_index()
    zip_state_platform = rec_grp.pivot(index=['zip', 'state', 'platform'], columns='frequency', values='amount').reset_index()

    # state, platform, frequency
    grp = ['state', 'platform', 'frequency']
    rec_grp = rec.groupby(grp)['amount'].median().reset_index()
    rec_grp['zip'] = None
    state_platform = rec_grp.pivot(index=['zip', 'state', 'platform'], columns='frequency', values='amount').reset_index()

    # platform
    grp = ['platform', 'frequency']
    rec_grp = rec.groupby(grp)['amount'].median().reset_index()
    rec_grp['state'] = None
    rec_grp['zip'] = None
    platform = rec_grp.pivot(index=['zip', 'state', 'platform'], columns='frequency', values='amount').reset_index()

    rec_all = pd.concat([zip_state_platform, state_platform, platform])

    rec_all['is_christmas'] = False 
    rec_all['is_newyears'] = False

    return rec_all


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


def get_frequency(date_diff):
    if date_diff != pd.Timedelta(0, 'd'):
        if date_diff - pd.Timedelta(7, "d") < pd.Timedelta(1, "d"):
            return 'week'
        elif date_diff - pd.Timedelta(14, "d") < pd.Timedelta(1, "d"):
            return 'bimonth'
        elif date_diff - pd.Timedelta(30, "d") < pd.Timedelta(2, "d"):
            return 'month'
        elif date_diff - pd.Timedelta(90, "d") < pd.Timedelta(3, "d"):
            return 'quarter'
        elif date_diff - pd.Timedelta(180, "d") < pd.Timedelta(4, "d"):
            return 'biannual'
        elif date_diff - pd.Timedelta(365, "d") < pd.Timedelta(5, "d"):
            return 'annual'
    
    return None


cache_recommended_amounts()