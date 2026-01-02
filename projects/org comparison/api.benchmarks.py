from flask import Flask, jsonify, request
import os
from s3_support import *


# init flask app
app = Flask(__name__)

app.json.sort_keys = False
app.config['JSON_SORT_KEYS'] = False

# change working directory to files directory for load_model()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


@app.route('/test/', methods=['GET'])
def test():
    rsp = {'success': '0'}

    try:
        # query db
        q = "select id from transactions order by id desc limit 10"
        df = redshift_query_read(q, schema='production')

        if len(df) == 10:
            rsp = {
                'success': '1',
                'message': "{} entries retreived".format(len(df))
            }
    except:
        rsp['message'] = 'DB connect failed'

    # respond
    return jsonify(rsp)
    

@app.route('/benchmarks/', methods=['POST'])
def get_benchmarks():
    key = 'tIHLM2vNlBwvlZlqdKy8'
    _input = request.get_json()

    if 'key' not in _input or _input['key'] != key:
        print("Request with incorrect input: {}".format(_input))
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        try:
            sample_size, data = get_benchmarks_data(_input)

            rsp = {
                'success': '1',
                'message': {
                    'sample_size': sample_size,
                    'data': data
                }
            }
            print("Success")
            print(rsp)
        except Exception as e:
            print("Exception occurred")
            print(e)
            rsp = {
                'success': '0',
                'message': str(e)
            }

    return jsonify(rsp)


def get_benchmarks_data(_input):
    print("Request input:")
    print(_input)

    where_clause = []
    params = []
    joins = []
    data = {'sample_size': 0, 'data': None}
    group_on = None

    comparison_org = _input.get('comparison_org', None)

    if comparison_org in _input:
        data['comparison_org'] = _input['comparison_org']

    filters = _input.get('filters', [])
    if len(filters) > 0:
        for f in filters:
            k = list(f.keys())[0]
            v = f[k]
            if k == 'org':
                where_clause.append('t.org={}')
                params.append(int(v))
            elif k == 'state':
                where_clause.append("o.state='{}'")
                params.append(v)
                joins.append('production.organization as o on t.org=o.id')
            elif k == 'volume':
                # org size
                # what buckets will we use here?
                pass
            elif k == 'date_min':
                where_clause.append("t.date>='{}'")
                params.append(v)
            elif k == 'date_max':
                where_clause.append("t.date<='{}'")
                params.append(v)
            elif k == 'trailing':
                # trailing30, trailing180, trailing365, etc.
                where_clause.append("t.date>='{}'")
                params.append("current_day - interval '{} day'".foramt(v))
            elif k == 'ntee':
                where_clause.append("o.ntee LIKE '%{}%'")
                params.append(v)
                joins.append('production.organization as o on t.org=o.id')
            elif k == 'tag':
                where_clause.append("o.tags LIKE '%{}%'")
                params.append(v)
                joins.append('production.organization as o on t.org=o.id')
            elif k == 'source':
                if v == 'don_form':
                    where_clause.append("t.source='{}'")
                    params.append('don_form')
                elif v == 'mobile':
                    where_clause.append("t.source='{}'")
                    params.append('mobile')
                elif v == 'p2p':
                    where_clause.append("t.source='{}'")
                    params.append('p2p')
            elif k == 'formtype':
                joins.append('production.form as f on f.id=t.form')

                if v == 'p2p':
                    where_clause.append("f.type={}")
                    params.append(3)
                elif v == 'yearround':
                    # qgiv
                    where_clause.append("f.type={}")
                    params.append(1)
                elif v == 'auction':
                    where_clause.append("f.type={}")
                    params.append(5)

    '''
    Insights:
    amount left to be raised, 
    at-risk donors, donor lifetime value, lapsed donors, new donors, 
    new vs repeat donors, retention rate, churn rate, 

    attendees bidding, attendees checked-in, auction constituents, 
    auction overview, average auction item sale price, average bid,
    average number of bids, bid activity over time, bids by increment amount,
    bids by source, higest bid, item performance, 

    contributions by associated info, contributions by date, 
    recent transactions, contributions by amount segment, contributions by form, 
    contributions by restriction, 
    contributions by text campaign,

    packages sold, contributions by event, days left to event, 
    p2p constituents, p2p overview, 
    '''
    if _input['insight'] == 'form_type':  # contributions by form type
        # build query
        q = '''select 
                    t.org as org,
                    f.type as type,
                    sum(t.amount) as volume,
                    count(distinct(t.id)) as count
                from production.transactions as t'''
        joins.append("production.form as f on t.form=f.id")
        group_on = 'f.type, t.org'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)
        
        # prep data for response
        def interpret_form_type(form_type):
            if form_type == 1:
                return 'qgiv'
            elif form_type == 2:
                return 'barnstorm'
            elif form_type == 3:
                return 'p2p'
            elif form_type == 5:
                return 'auction'
        
        df['type'] = df['type'].apply(interpret_form_type)
        df = df[~df['type'].isna()]
        df_pivot = df.pivot(index='org', columns='type', values='volume').reset_index().fillna(0)

        type_cols = [c for c in df_pivot.columns if c!='org']
        for c in df_pivot.columns:
            if c != 'org':
                df_pivot['{}_percentage'.format(c)] = df_pivot[c] / df_pivot[type_cols].sum(axis=1)

        # build response object
        data = {
            'sample_size': len(df_pivot),
            'data': df_pivot[[c for c in df_pivot.columns if c!='org']].agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df_pivot[df_pivot['org']==comparison_org][[c for c in df_pivot.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df_pivot[df_pivot[k]<this_org_data[k]]) / len(df_pivot[df_pivot[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] == 'payment_method':  # contributions by payment method
        # build query
        q = '''select 
                    t.org as org,
                    t.payment_type as payment_type,
                    sum(t.amount) as volume,
                    count(distinct(t.id)) as count
                from production.transactions as t'''
        group_on = 't.org, t.payment_type'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)
        
        # prep data for response
        df = df[~df['payment_type'].isna()]
        df_pivot = df.pivot(index='org', columns='payment_type', values='volume').reset_index().fillna(0)

        type_cols = [c for c in df_pivot.columns if c!='org']
        for c in df_pivot.columns:
            if c != 'org':
                df_pivot['{}_percentage'.format(c)] = df_pivot[c] / df_pivot[type_cols].sum(axis=1)

        # build response object
        data = {
            'sample_size': len(df_pivot),
            'data': df_pivot[[c for c in df_pivot.columns if c!='org']].agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df_pivot[df_pivot['org']==comparison_org][[c for c in df_pivot.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df_pivot[df_pivot[k]<this_org_data[k]]) / len(df_pivot[df_pivot[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] == 'contribution_source':  # contributions by source
        # build query
        q = '''select 
                    t.org as org,
                    t.source as source,
                    sum(t.amount) as volume,
                    count(distinct(t.id)) as count
                from production.transactions as t'''
        group_on = 't.org, t.source'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)
        
        # prep data for response
        df_pivot = df.pivot(index='org', columns='source', values='volume').reset_index().fillna(0)

        type_cols = [c for c in df_pivot.columns if c!='org']
        for c in df_pivot.columns:
            df_pivot['{}_percentage'.format(c)] = df_pivot[c] / df_pivot[type_cols].sum(axis=1)

        # build response object
        data = {
            'sample_size': len(df_pivot),
            'data': df_pivot[[c for c in df_pivot.columns if c!='org']].agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df_pivot[df_pivot['org']==comparison_org][[c for c in df_pivot.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df_pivot[df_pivot[k]<this_org_data[k]]) / len(df_pivot[df_pivot[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] in ['trans_count', 'trans_average', 'trans_sum']:
        # contribution count, average contribution amount, amount raised
        # build query
        q = '''select 
                    t.org as org,
                    median(t.amount) as trans_median,
                    count(t.id) as trans_count,
                    sum(t.amount) as trans_volume
                from production.transactions as t'''
        group_on = 't.org'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)
        
        # prep data
        df['trans_mean'] = df['trans_volume'] / df['trans_count']

        # build response object
        data = {
            'sample_size': len(df),
            'data': df[[c for c in df.columns if c!='org']].agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org][[c for c in df.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df[df[k]<this_org_data[k]]) / len(df[df[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] == 'oentime_v_recurring':  # contributions by type (one time v recurring)
        # build query
        q = '''select
                    t.org as org,
                    sum(case when t.recurring=0 then 1 else 0 end) as onetime_count,
                    sum(case when t.recurring=0 then amount else 0 end) as onetime_volume,
                    sum(case when t.recurring_origin!=0 then 1 else 0 end) as recurring_count,
                    sum(case when t.recurring_origin!=0 then amount else 0 end) as recurring_volume
                from production.transactions as t'''
        group_on = 't.org'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)

        # prep data for response
        df['total_count'] = df['onetime_count'] + df['recurring_count']
        df['total_volume'] = df['onetime_volume'] + df['recurring_volume']
        df['onetime_count_percentage'] = df['onetime_count'] / df['total_count']
        df['recurring_count_percentage'] = df['recurring_count'] / df['total_count']
        df['onetime_volume_percentage'] = df['onetime_volume'] / df['total_count']
        df['recurring_volume_percentage'] = df['recurring_volume'] / df['total_count']
        df.drop(['total_count', 'total_volume'], axis=1, inplace=True)

        # build response object
        data = {
            'sample_size': len(df),
            'data': df[[c for c in df.columns if c!='org']].agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org][[c for c in df.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df[df[k]<this_org_data[k]]) / len(df[df[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] in ['donation_count', 'registration_count']:
        # donation count, registration count
        # build query
        q = '''select
                    t.org as org,
                    sum(t.donations_count) as donations_count,
                    sum(t.donations_amt) as donations_volume,
                    sum(t.registrations_count) as registrations_count,
                    sum(t.registrations_amt) as registrations_volume
                from production.transactions as t'''
        group_on = 't.org'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)

        # prep data for response
        df['total_count'] = df['donations_count'] + df['registrations_count']
        df['total_volume'] = df['donations_volume'] + df['registrations_volume']
        df['donations_count_percentage'] = df['donations_count'] / df['total_count']
        df['registrations_count_percentage'] = df['registrations_count'] / df['total_count']
        df['donations_volume_percentage'] = df['donations_volume'] / df['total_count']
        df['registrations_volume_percentage'] = df['registrations_volume'] / df['total_count']
        df.drop(['total_count', 'total_volume'], axis=1, inplace=True)

        # build response object
        data = {
            'sample_size': len(df),
            'data': df[[c for c in df.columns if c!='org']].agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org][[c for c in df.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df[df[k]<this_org_data[k]]) / len(df[df[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] == 'giftassist':
        # total gift assist, gift assist success rate
        # build query
        q = '''select
                    t.org as org,
                    count(distinct(t.id)) as trans_count,
                    sum(t.gift_assist_count) as giftassist_count,
                    sum(t.amount) as volume,
                    sum(t.gift_assist_amt) as giftassist_volume
                from production.transactions as t'''
        group_on = 't.org'

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)

        # prep data for response
        df['success_rate'] = df['giftassist_count'] / df['trans_count']
        df.drop(['org', 'trans_count'], axis=1, inplace=True)

        # build response object
        data = {
            'sample_size': len(df),
            'data': df.agg(['mean', 'median']).to_dict()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org][[c for c in df.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df[df[k]<this_org_data[k]]) / len(df[df[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] == 'form_conversion':
        # build query
        q = '''select
                    fa.form as form,
                    sum(fa.pageviews) as pageviews,
                    sum(fa.trans_onetime_count) + sum(fa.trans_rec_count) as transactions
                from production.transactions as t
                    left join public.form_aggregates as fa on t.form=fa.form'''
        group_on = 'fa.form'
        for i in range(0, len(where_clause)):
            if 't.date' in where_clause[i]:
                where_clause[i] = where_clause[i].replace('t.', 'fa.')

        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)
        
        # prep data for response
        df = df[df['pageviews']>0]
        df['conversion'] = df['transactions'] / df['pageviews']
        df = df[df['conversion']<1.]

        # build response object
        data = {
            'sample_size': len(df),
            'data': {
                'mean': df['conversion'].mean(),
                'median': df['conversion'].median()
            }
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org][[c for c in df.columns if c!='org']].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df[df[k]<this_org_data[k]]) / len(df[df[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] == 'donor_liftetime_value':
        # public.donors_orgs, volume
        # build query
        q = '''select
                    d.org as org,
                    avg(d.volume) as average_lifetime_value
                from public.donors_orgs as d'''
        if len(where_clause) > 0:
            joins.append('production.transactions as t on t.form=d.form')
        group_on = 'd.org'
        
        # pull data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins, group_on=group_on)

        # prep for response
        e = df.iloc[0]

        # build response object
        data = {
            'sample_size': len(df),
            'data': df['average_lifetime_value'].mean()
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org].iloc[0].to_dict()

            comparison_data = {
                'average_lifetime_value': len(df[df['average_lifetime_value']<this_org_data['average_lifetime_value']]) / len(df[df['average_lifetime_value']>0])
            }

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }
    elif _input['insight'] in ['churn', 'retention', 'new_donors']:
        # public.org_retention
        # org, retention, churn, new_donors
        q = '''select
                    r.org as org,
                    r.retention as retention,
                    r.churn as churn,
                    r.new_donors as new_donors
                from public.org_retention as r'''
        if len(where_clause) > 0:
            joins.append('production.transactions as t on t.form=r.form')

        # query data
        df = build_and_execute_query(q, where_clause=where_clause, parameters=params, joins=joins)

        # build response        
        data = {
            'sample_size': len(df),
            'data': {
                'retention': df['retention'].mean(),
                'churn': df['churn'].mean(),
                'new_donors': df['new_donors'].mean()
            }
        }

        # add comparison stats if comparison_org provided...
        if comparison_org is not None:
            this_org_data = df[df['org']==comparison_org].iloc[0].to_dict()

            comparison_data = {}
            for k in this_org_data.keys():
                comparison_data[k] = len(df[df[k]<this_org_data[k]]) / len(df[df[k]>0])

            data['comparison_org'] = {
                'data': this_org_data,
                'better_than': comparison_data
            }

    '''
    restructure for donor_liftetime_value, churn, retention, 
    new_donors
    (1) need to adjust where clause application for dates to match agg
    tables rather than transactions
    (2) need to block certain filters for lack of support? (payment method,
    source)
    '''
    
    return data['sample_size'], data['data']


def build_and_execute_query(q, where_clause=[], parameters=[], joins=[], group_on=None):
    if len(joins) > 0:
        q += ' left join ' + ' left join '.join(joins)

    if len(where_clause) > 0:
        q += ' where ' + ' and '.join(where_clause)
    
    if group_on is not None:
        q += ' group by {}'.format(group_on)

    df = redshift_query_read(q.format(*parameters), schema='production')

    return df


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)