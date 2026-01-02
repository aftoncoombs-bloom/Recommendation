from multiprocessing.connection import Listener
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import os


# set model variables to None until they're used
fraud_model = None
form_features_model = None
form_settings_model = None
form_embeddings = None


'''
Load function for opening & deserializing the fraud models and 
returning the object
'''
def load_model(model_name):
    if '.' not in model_name:
        model_name = model_name + '.pkl'
    f = open('/var/www/analytics/'+model_name, 'rb')
    mdl = joblib.load(f)
    f.close()
    
    return mdl


def optimize_required_fields(mdl, _input):
    conversions = []
    base_conversion = mdl.predict(_input)[0]

    for i in range(0, 8):
        _input['req_fields'] = i
        _input['req_fields^2'] = i**2
        _input['req_fields^3'] = i**3
        _input['fields'] = i + _input['opt_fields']
        _input['fields^2'] = _input['fields']**2
        _input['fields^3'] = _input['fields']**3
        
        conversions.append(mdl.predict(_input)[0])
    return (conversions.index(max(conversions)) + 1, max(conversions) - base_conversion)


def optimize_optional_fields(mdl, _input):
    conversions = []
    base_conversion = mdl.predict(_input)[0]

    for i in range(0, 8):
        _input['opt_fields'] = i
        _input['opt_fields^2'] = i**2
        _input['opt_fields^3'] = i**3
        _input['fields'] = i + _input['req_fields']
        _input['fields^2'] = _input['fields']**2
        _input['fields^3'] = _input['fields']**3

        conversions.append(mdl.predict(_input)[0])
    return (conversions.index(max(conversions)) + 1, max(conversions) - base_conversion)


def optimize_restrictions(mdl, _input):
    conversions = []
    base_conversion = mdl.predict(_input)[0]

    for i in range(0, 12):
        _input['restrictions'] = i
        _input['restrictions^2'] = i**2
        _input['restrictions^3'] = i**3
        _input['restrictionsXmultirestriction_system'] = _input['restrictions'] * _input['multirestriction_system']
        _input['restrictions^2Xmultirestriction_system'] = _input['restrictions^2'] * _input['multirestriction_system']
        _input['restrictions^3Xmultirestriction_system'] = _input['restrictions^3'] * _input['multirestriction_system']

        conversions.append(mdl.predict(_input)[0])
    return (conversions.index(max(conversions)) + 1, max(conversions) - base_conversion)


def optimize_settings(mdl, _input):
    settings_to_change = []
    base_conversion = mdl.predict(_input)[0]
    new_conversions = []

    for i in _input:
        if i not in ['month', 'day', 'is_payday']:
            if _input[i][0] == 0:
                _input[i] = 1
                new_conversion = mdl.predict(_input)[0]
                if new_conversion > base_conversion:
                    new_conversions.append(new_conversion)
                    settings_to_change.append(i)
                _input[i] = 0

    if len(new_conversions) == 0:
        new_conversions = [0]

    return (settings_to_change, np.mean(new_conversions) - base_conversion)


fraud_model = load_model('fraud')
fraud_model_sm = load_model("fraud_sml")

form_embeddings = None
if os.path.exists("form_embeddings.csv"):
    form_embeddings = pd.read_csv("form_embeddings.csv")

# loop the listener waiting for input
while True:
    # setup for thread listener
    address = ('localhost', 6000)
    listener = Listener(address, authkey='secret password')
    conn = listener.accept()

    print('connection accepted from {}'.format(listener.last_accepted))

    msg = conn.recv()
    rsp = {'status': 0, 'errors': []}

    # received input, verify & run
    if 'model' not in msg:
        rsp['errors'].append('Model not specified')
    elif 'params' not in msg:
        rsp['errors'].append('Parameters not provided')
    else:
        try:
            if msg['model'] not in ['fraud', 'form_features', 'form_settings']:
                rsp['errors'].append('Invalid model specified ({})'.format(msg['model']))
            else:
                # verify model is loaded and localize the fit
                if msg['model'] == 'fraud':
                    print("DEBUG received fraud input parameters: {}".format(", ".join(msg['params'].columns)))

                    fraud_model = load_model("fraud")
                    ftrs = fraud_model['features']
                    
                    # remove inputs that are not model features
                    rm = []
                    for c in msg['params']:
                        if c not in ftrs:
                            rm.append(c)
                    if len(rm) > 0:
                        msg['params'].drop(rm, axis=1, inplace=True)

                    # execute prediction
                    y_pred = fraud_model['fit'].predict(msg['params'])[0]

                    rsp['status'] = 1
                    rsp['is_fraud'] = y_pred
                elif msg['model'] == 'form_features':
                    if form_features_model is None:
                        form_features_model = load_model('form_features')
                    if os.path.exists("form_embeddings.csv") and form_embeddings is None:
                        form_embeddings = pd.read_csv("form_embeddings.csv")
                    
                    # load the form embedding and add to input features
                    if os.path.exists("form_embeddings.csv"):
                        form_id = int(msg['params']['form'])
                        del(msg['params']['form'])
                        embedding = form_embeddings[form_embeddings.form==form_id].iloc[0]
                        for c in embedding.columns:
                            msg['params'][c] = embedding[c]

                    # optimization predictions
                    optimal_restrictions, optimal_restrictions_conversion = optimize_restrictions(form_features_model['fit'], msg['params'])
                    optimal_reqfields, optimal_reqfields_conversion = optimize_required_fields(form_features_model['fit'], msg['params'])

                    rsp['status'] = 1
                    rsp['optimal_restrictions'] = optimal_restrictions
                    rsp['optimal_restrictions_conversion'] = optimal_restrictions_conversion
                    rsp['optimal_reqfields'] = optimal_reqfields
                    rsp['optimal_reqfields_conversion'] = optimal_reqfields_conversion
                elif msg['model'] == 'form_settings':
                    if form_settings_model is None:
                        form_settings_model = load_model('form_settings')
                    if os.path.exists("form_embeddings.csv") and form_embeddings is None:
                        form_embeddings = pd.read_csv("form_embeddings.csv")
                    
                    if os.path.exists("form_embeddings.csv"):
                        # load the form embedding and add to input features
                        form_id = int(msg['params']['form'])
                        del(msg['params']['form'])
                        embedding = form_embeddings[form_embeddings.form==form_id].iloc[0]
                        for c in embedding.columns:
                            msg['params'][c] = embedding[c]
                    
                    # optimization predictions
                    settings_to_change, settings_optimal_conversion = optimize_settings(form_settings_model['fit'], msg['params'])

                    rsp['status'] = 1
                    rsp['settings_to_change'] = settings_to_change
                    rsp['settings_optimal_conversion'] = settings_optimal_conversion

        except Exception as e:
            rsp['errors'].append("Error occurred loading or executing the model; {}".format(e.strerror))
    
    conn.send(rsp)
    conn.close()

    listener.close()

listener.close()