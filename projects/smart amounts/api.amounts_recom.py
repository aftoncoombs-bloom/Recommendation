from flask import Flask, jsonify, request, g
import pandas as pd
import os
from s3_support import *


# init flask app
app = Flask(__name__)
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
                'entries': len(df)
            }
    except:
        rsp['message'] = 'DB connect failed'

    # respond
    return jsonify(rsp)

        
@app.route('/amounts_rec_data/', methods=['POST'])
def get_amounts_recommendation_data():
    key = 'tIHLM2vNlBwvlZlqdKy8'
    _input = request.get_json()
    
    if 'key' in _input and _input['key'] != key:
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        try:
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
            
            trans = trans.append(trans_nozip)

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
            
            trans = trans.append(trans_nozipplatform)
            
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

            rsp = {
                'success': '1',
                'data': trans.to_dict(orient='records')
            }
        except Exception as e:
            rsp = {
                'success': '0',
                'errors': str(e)
            }
            
    return jsonify(rsp)

    
    
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8890")