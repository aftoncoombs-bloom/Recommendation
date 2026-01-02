from flask import Flask, jsonify, request, g
import pandas as pd
import os, sys, json, datetime


# init flask app
app = Flask(__name__)
# change working directory to files directory for load_model()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


DF_STATE = pd.read_csv("amounts.state.csv")
DF_ZIP = pd.read_csv("amounts.zip.csv")


@app.route('/amounts_recom/', methods=['POST'])
def amounts_recommendation(testing=True, _input=None):
    try:
        if _input is None:
            _input = json.loads(request.get_json())
            
        # prototype input: state, zip, useragent
        # prep useragent input
        _input['platform'] = tag_platform(_input['useragent'])
        
        # prep dates
        today_month = datetime.datetime.now().date().month
        today_date = datetime.datetime.now().date().day
        
        is_christmas = today_month == 12 and today_date == 25
        is_newyears = today_month == 12 and today_date in [30, 31]
        
        # check for sufficient sample size by zip
        sample = DF_AMOUNTS[DF_AMOUNTS['state']==_input['state']]
        
        if sample[sample['zip']==_input['zip']]['count'].sum() > 100:
            sample = sample[sample['zip']==_input['zip']]
        if sample[sample['platform']==_input['platform']]['count'].sum() > 100:
            sample = sample[sample['platform']==_input['platform']]
        if is_christmas and sample[sample['is_christmas']]['count'].sum() > 100:
            sample = sample[sample['is_christmas']]
        if is_newyears and sample[sample['is_newyears']]['count'].sum() > 100:
            sample = sample[sample['is_newyears']]
        
        recommended_amount = sample['median'].mean()
        
        rsp = {
            "status": 1,
            "data": {
                "amount": recommended_amount
            }
        }
        
        return jsonify(json.loads(json.dumps(rsp))), 200
        
    except Exception as e:
        _, _, exc = sys.exc_info()
        line_no = exc.tb_lineno
        
        # send error response
        err_msg = "Input feature error; the most likely cause is malformed or missing input"
        
        if testing:
            return {
                'msg': err_msg,
                'line': line_no
            }
        else:
            return jsonify(json.loads(json.dumps({"response": {"errors": [rsp]}}).replace(':NaN,', ':Null,'))), 500
        
        
@app.route('/amounts_rec_data/', methods=['POST'])
def get_amounts_recommendation_data():
    key = 'tIHLM2vNlBwvlZlqdKy8'
    _input = json.loads(request.get_json())
    
    if _input['key'] != key:
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        try:
            q = '''select
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

            trans['platform'] = trans['useragent'].apply(tag_platform)
            platforms = ['iPhone', 'iPad', 'Android', 'Mac', 'Windows']
            trans = trans[trans['platform'].isin(platforms)]

            trans['is_christmas'] = (trans['date'].dt.month==12)&(trans['date'].dt.day==25)
            trans['is_newyears'] = (trans['date'].dt.month==12)&(trans['date'].dt.day.isin([30, 31]))

            grouping_cols = ['state', 'zip', 'platform', 
                             'is_christmas', 'is_newyears']
            trans_grp_zip = trans.groupby(grouping_cols)['amount'].agg(['count', 'median']).reset_index()

            grouping_cols = ['state', 'platform', 'is_christmas', 'is_newyears']
            trans_grp_state = trans.groupby(grouping_cols)['amount'].agg(['count', 'median']).reset_index()
            trans_grp_state['zip'] = None
            
            grouping_cols = ['state', 'is_christmas', 'is_newyears']
            trans_grp_state_noplat = trans.groupby(grouping_cols)['amount'].agg(['count', 'median']).reset_index()
            trans_grp_state_noplat['zip'] = None
            trans_grp_state_noplat['platform'] = None
            
            trans_grp_merged = trans_grp_zip.append(trans_grp_state)
            trans_grp_merged = trans_grp_merged.append(trans_grp_state_noplat)

            rsp = {
                'success': '1',
                'data': trans_grp_merged.to_dict()
            }
        except Exception as e:
            rsp = {
                'success': '0',
                'errors': e
            }
            
    return jsonify(rsp)


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