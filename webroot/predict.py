from flask import Flask, jsonify, request, g
import numpy as np
import pandas as pd
import os, urlparse, ast
from db import select_rows
from multiprocessing.connection import Client
import time


# init flask app
app = Flask(__name__)
# change working directory to files directory for load_model()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


@app.route('/formhealth/', methods=['POST'])
def formhealth(testing=False, _input=None):
    try:
        _input = request.form.to_dict()
        
        input_features = {}
        input_settings = {}
        form_id = None

        if 'features' in _input:
            input_features = _input['features']
        if 'settings' in _input:
            input_settings = _input['settings']

        for k in _input.keys():
            if k == 'form':
                form_id = _input[k]
            elif 'features[' in k:
                _key = k.replace('features[', '').replace(']', '')
                input_features[_key] = _input[k]
            elif 'settings[' in k:
                _key = k.replace('settings[', '').replace(']', '')
                input_settings[_key] = _input[k]

        if type(input_features) == unicode:
            import ast
            input_features = ast.literal_eval(input_features)
        if type(input_settings) == unicode:
            import ast
            input_settings = ast.literal_eval(input_settings)

        # perform predictions
        X_features = pd.DataFrame([input_features]).apply(pd.to_numeric, errors='ignore')
        rsp = client_predict('form_features', X_features.copy())

        optimal_restrictions = rsp['optimal_restrictions']
        optimal_restrictions_conversion = between_ceil_floor(rsp['optimal_restrictions_conversion'], 0, 0.75)
        optimal_reqfields = rsp['optimal_reqfields']
        optimal_reqfields_conversion = between_ceil_floor(rsp['optimal_reqfields_conversion'], 0, 0.75)

        # hard check to stop suggesting increasing features counts
        if int(optimal_reqfields) >= int(input_features['req_fields']):
            optimal_reqfields = 0
            optimal_reqfields_conversion = 0
        if int(optimal_restrictions) >= int(input_features['restrictions']):
            optimal_restrictions = 0
            optimal_restrictions_conversion = 0

        X_settings = pd.DataFrame([input_settings]).apply(pd.to_numeric, errors='ignore')
        rsp = client_predict('form_settings', X_settings.copy())

        settings_to_change = rsp['settings_to_change']
        settings_optimal_conversion = between_ceil_floor(rsp['settings_optimal_conversion'], 0, 1)

        if settings_optimal_conversion == 0.0:
            settings_to_change = []

        visits, trans_val = get_conversion_diff_values(form_id)

        restrictions_cost = get_conversion_diff_cost(optimal_restrictions_conversion, visits, trans_val)
        req_fields_cost = get_conversion_diff_cost(optimal_reqfields_conversion, visits, trans_val)
        features_cost = get_conversion_diff_cost(np.sum([optimal_reqfields_conversion, optimal_restrictions_conversion]), visits, trans_val)
        settings_cost = get_conversion_diff_cost(settings_optimal_conversion, visits, trans_val)

        # calculate grades
        ease_of_use_grade = calculate_grade(np.mean([optimal_restrictions_conversion, optimal_reqfields_conversion]))
        use_of_features_grade = calculate_grade(settings_optimal_conversion)
        overall_grade = np.mean([ease_of_use_grade, use_of_features_grade])
        
        # adjust conversions for proportionality
        optimal_ease_of_use_conversion = np.mean([optimal_restrictions_conversion, optimal_reqfields_conversion])
        overall_conversion = np.mean([optimal_ease_of_use_conversion, settings_optimal_conversion])
        optimal_ease_of_use_conversion = optimal_ease_of_use_conversion / 2
        settings_optimal_conversion = settings_optimal_conversion / 2

        rsp = {
            "conversion": overall_conversion,
            "overall": overall_grade,
            "savings": features_cost + settings_cost,
            "ease_of_use": {
                "grade": ease_of_use_grade,
                "savings": features_cost,
                "conversion": optimal_ease_of_use_conversion,
                "suggestions": {
                    "restrictions": {
                        "num": optimal_restrictions,  # ideal number
                        "savings": restrictions_cost,  # amount losing for lower than optimal conversion
                        "conversion": optimal_restrictions_conversion
                    },
                    "required_fields": {
                        "num": optimal_reqfields,  # ideal number
                        "savings": req_fields_cost,  # amount losing for lower than optimal conversion
                        "conversion": optimal_reqfields_conversion
                    }
                }
            },
            "use_of_features": {
                "grade": use_of_features_grade,
                "suggestions": settings_to_change,  # list of settings that should be changed
                "savings": settings_cost,  # amount losing for bad settings
                "conversion": settings_optimal_conversion
            },
            "cost_calculation": {
                "visits": visits,
                "trans_val": trans_val
            }
        }
    except:
        # log error
        app.logger.info("FORM HEALTH ERROR: {}".format(request.form))
        # send error response
        rsp = {"status": "0", "error": "Input feature error; could not generate prediction or cast input"}

    if testing:
        return rsp
    else:
        return jsonify(rsp)


@app.route('/fraud/', methods=['POST'])
def is_fraud():
    '''
    provided:
        'five_or_less', 'fifteen_or_less', 'from_frontend',
        'is_recurring', 'fifty_or_less', 'donations_count',
    computed:
        'form_mean_fraud', 'form_perc_five_or_less',
        'form_perc_fifteen_or_less', 'form_dayofweek_diff'
    '''
    try:
        # build the model features from the input
        X = build_fraud_features({
            'form': request.form['form'], 
            'amount': request.form['amount'], 
            'day': request.form['day'],
            'from_frontend': request.form.get('from_frontend', False),
            'is_recurring': request.form.get('is_recurring', False),
            'donations_count': request.form.get('donations_count', 0)
        })

        print("DEBUG predicting fraud")

        rsp = client_predict('fraud', X)
        if 'status' not in rsp or rsp['status'] != 1:
            rsp['error'] = "Fraud prediction returned with error"
    except:
        # log error
        app.logger.info("FRAUD ERROR: {}".format(request.form))
        # send error response
        rsp = {"status": "0", "is_fraud": "0", "error": "Input feature error; could not generate prediction or cast input"}
    
    for k in rsp:
            rsp[k] = str(rsp[k])

    return jsonify(rsp)


@app.before_request
def before_request():
    g.start = time.time()


@app.after_request
def after_request(response):
    execution_time = time.time() - g.start

    app.logger.info("REQUEST: {} execution time; input - {}; response - {}".format(execution_time, request.form, response.data))

    return response


def build_fraud_features(_input):
    import datetime
    
    form = int(_input['form'])
    amount = float(_input['amount'])
    day = _input.get('day', None)

    if day is None:
        now = datetime.datetime.now()
        if day is None:
            day = now.day

    flds = ['trans_day_mean as dayofweek_mean',
            'mean_fraud as mean_fraud',
            'perc_fifty_or_less as form_perc_fifty_or_less',
            'perc_fifteen_or_less as form_perc_fifteen_or_less',
            'perc_five_or_less as form_perc_five_or_less']
    cached_form_stats = select_rows('form', fields=flds, where='id={}'.format(form))

    if 'amount' not in cached_form_stats or cached_form_stats['amount'] is None:
        flds = ['avg(amount) as amount', 
                'avg(dayofweek(date)) as dayofweek']
        cached_form_stats = select_rows('transactions', fields=flds, where='form={}'.format(form)).iloc[0]

        len_transactions = select_rows("transactions", fields=['count(id) as count'], where="form={}".format(form)).iloc[0]['count']
        len_less_than_5 = select_rows("transactions", fields=['count(id) as count'], where="form={} and amount>5".format(form)).iloc[0]['count']
        len_less_than_15 = select_rows("transactions", fields=['count(id) as count'], where="form={} and amount>15".format(form)).iloc[0]['count']
        len_less_than_50 = select_rows("transactions", fields=['count(id) as count'], where="form={} and amount>50".format(form)).iloc[0]['count']
        
        if cached_form_stats['amount'] is None:
            flds = ['avg(is_fraud) as mean_fraud', 
                    'avg(dayofweek(date)) as dayofweek']
            cached_form_stats = select_rows('transactions', fields=flds).iloc[0]

            len_transactions = select_rows("transactions", fields=['count(id) as count'], where="form={}".format(form)).iloc[0]['count']
            len_less_than_5 = select_rows("transactions", fields=['count(id) as count'], where="amount>5").iloc[0]['count']
            len_less_than_15 = select_rows("transactions", fields=['count(id) as count'], where="amount>15").iloc[0]['count']
            len_less_than_50 = select_rows("transactions", fields=['count(id) as count'], where="amount>50").iloc[0]['count']

        if float(len_transactions) > 0.:
            cached_form_stats['form_perc_fifty_or_less'] = float(len_less_than_50) / float(len_transactions)
            cached_form_stats['form_perc_fifteen_or_less'] = float(len_less_than_15) / float(len_transactions)
            cached_form_stats['form_perc_five_or_less'] = float(len_less_than_5) / float(len_transactions)

    # if we didn't have perc_[#]_or_less calculated, use precalculated system-wide stats
    if 'form_perc_fifteen_or_less' not in cached_form_stats:
        cached_form_stats['form_perc_fifty_or_less'] = 0.59999
        cached_form_stats['form_perc_fifteen_or_less'] = 0.1522
        cached_form_stats['form_perc_five_or_less'] = 0.0781

    if 'mean_fraud' not in cached_form_stats:
        cached_form_stats['mean_fraud'] = 0.025
        
    print("DEBUG cached_form_stats: {}".format(cached_form_stats))
    
    amount = float(amount)
    cached_mean_dayofweek = float(cached_form_stats['dayofweek'])
    form_dayofweek_diff = cached_mean_dayofweek - float(day)
    
    X = pd.DataFrame([{
        'form_mean_fraud': cached_form_stats['mean_fraud'],  
        'is_recurring': _input['is_recurring'], 
        'five_or_less': amount <= 5., 
        'fifteen_or_less': amount <= 15.,
        'fifty_or_less': amount <= 50., 
        'form_perc_five_or_less': cached_form_stats['form_perc_five_or_less'],
        'form_perc_fifteen_or_less': cached_form_stats['form_perc_fifteen_or_less'], 
        'from_frontend': _input['from_frontend'], 
        'donations_count': _input['donations_count'], 
        'form_dayofweek_diff': form_dayofweek_diff
    }])

    return X


def client_predict(model, X):
    address = ('localhost', 6000)
    try:
        conn = Client(address, authkey='secret password')
    except:
        # restart process & try again
        import os
        os.system("python /var/www/analytics/model_loader.py &")
        conn = Client(address, authkey='secret password')
    
    payload = {'model': model, 'params': X}
    conn.send(payload)
    rsp = conn.recv()
    conn.close()

    print("DEBUG - client sending payload")
    print("DEBUG - server response: {}".format(rsp))

    return rsp


def get_conversion_diff_values(form, avgs=None):
    if avgs is None:
        # load current average transaction value & average visits
        avgs = select_rows('transactions_form_agg', fields=['AVG(visits) AS visits', 'AVG(trans_amount_mean) AS avg_trans_value'], where="form={}".format(form)).dropna()

        # if we don't have data for the given form, go with table averages
        sys_avgs = select_rows('transactions_form_agg', fields=['AVG(visits) AS visits', 'AVG(trans_amount_mean) AS avg_trans_value'])

    if len(avgs) == 0:
        avgs = sys_avgs

    visits = avgs.iloc[0]['visits']
    trans_val = avgs.iloc[0]['avg_trans_value']

    if visits == 0:
        visits = sys_avgs.iloc[0]['visits']
    if trans_val == 0:
        trans_val = sys_avgs.iloc[0]['avg_trans_value']

    return visits, trans_val


def get_conversion_diff_cost(conversion_diff, visits, trans_val):
    return ((visits * (conversion_diff / 100)) * trans_val) * 365.0


def calculate_grade(perc_diff):
    return max(100 - (5 * perc_diff), 0)


def between_ceil_floor(x, floor=0, ceil=1):
    x = max(x, floor)
    x = min(x, ceil)
    return x