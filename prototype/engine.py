import datetime, pickle, json
import numpy as np
import pandas as pd
from collections import OrderedDict
from engine_validation import mean_variance_validation, cross_validation

from flask import Flask, jsonify, request
app = Flask(__name__)


def load_model(model):
    '''
    Opens a json-formatted model file specified by filename without extension. File is expected to be located within the currently active directory.
    '''
    with open(model+'.json') as model_data_file: 
        model__meta_data = OrderedDict(json.load(model_data_file))
        model = model_meta_data
    with open(model+'.pickle', 'rb') as model_pickle_file:
        mdl = pickle.load(model_pickle_file)
        model['model'] = mdl

    return model


def load_training_data(use_csv=True):
    '''
    Loads data from hardcoded CSV files and returns a merged dataframe.
    '''
    if use_csv:
        # load from csv
        analytic_base = pd.read_csv('~/Repositories/datasets/analytic_base.csv')
        analytic_qgiv = pd.read_csv('~/Repositories/datasets/analytic_qgiv_stats.csv')

        ab = analytic_base[['id', 'org', 'form', 'timestamp', 'visits', 'mobile_visits', 'don_form_trans_count', 'don_form_trans_vol']]
        aq = analytic_qgiv[['id', 'base', 'org', 'total_visits', 'opt_fields', 'req_fields', 'donation_active', 'amounts_system', 'multirestriction_system', 'restrictions', 'pledges_count', 'pledge_active', 'permit_anonymous', 'permit_mobile', 'permit_other_amount', 'enable_donorlogins', 'collect_captcha']]
        d = pd.merge(ab, aq, left_on="id", right_on="base")
    else:
        # load from database
        d = pd.dataframe()

    return d


def train_model(model, data=None):
    '''
    Trains a given model with stored data, returning the calculated weights
    '''
    # localize data
    model_obj = load_model(model)

    features = model_obj['features']
    calculated_features = model_obj['calculated_features']
    target = model_obj['target']
    fit = model_obj['fit']

    # load training data
    if data is None:
        data = load_training_data()

    # add the complication terms
    for term in calculated_features:
        if term[-1] in ['2','3','4','5']:
            exponent = int(term[-1])
            original_term = term[:-1]
            data[term] = data[original_term] ** exponent
        elif 'X' in term:
            original_terms = term.split('X')
            data[term] = data[original_terms[0] * original_term[1]]
        elif '+' in term:
            original_terms = term.split('X')
            input[term] = input[original_terms[0] + original_term[1]]
        else:
            raise Exception('engine::73')

    data_target = data[target]
    del data[target]

    fit.fit(data, data_target)

    return fit


def validate_model(model, fit, target=None):
    '''
    Validates the supplied model by the validation method specified in the model definition.
    '''
    # load testing data
    data = load_testing_data()
    model_obj = load_model(model)

    # run validation function
    if model_obj['validation'] == 'mean_variance':
        err = mean_variance_validation(fit, target)
    elif model_obj['validation'] == 'cross_validation':
        err = cross_validation(fit, data)

    return err


def update_model(model, weights=None):
    '''
    Retrains a stored model, calculating updated weights via train_model() or new weights passed, then writing them to the json file.
    '''
    # load the json-stored model data from file
    model_data = load_model(model)

    if weights is None:
        # update weights by re-training the model
        updated_model = train_model(model_data)

    # validate models to store old model if new model performs worse
    new_mdl_error = validate_model(updated_model)
    if new_mdl_error > model_data['validation_error']:
        # new model performs worse so we want to archive the old model
        with open(model+'.'+str(datetime.datetime.now())+'.json', 'w') as model_data_file:
            json.dump(model_data, model_data_file)
    model_data['validation_error'] = new_mdl_error
    
    # write changes to model file
    with open(model+'.json', 'w') as model_data_file:
        json.dump(model_data, model_data_file)
    with open(model+'.pickle', 'wb') as model_pickle_file:
        pickle.dump(updated_model, model_pickle_file)
    
    return jsonify({"success":"True"})


def predict(model, direct_inputs=None):
    '''
    Executes a prediction of the supplied model using the supplied input values.
    '''
    # localize model weights from database
    model_obj = load_model(model)
    coefs = model_obj['features']

    # check if we need to rebuild engineered features
    if sorted(coefs) != sorted(direct_inputs.keys()):
        # build out complication terms for input
        something_changed = True
        while something_changed:
            something_changed = False
            for term in coefs.keys():
                if term not in direct_inputs.keys():
                    try:
                        if term[-1] in ['2','3','4','5']:
                            exponent = int(term[-1])
                            original_term = term[:-1]
                            direct_inputs[term] = direct_inputs[original_term] ** exponent
                            something_changed = True
                        elif 'X' in term:
                            original_terms = term.split('X')
                            direct_inputs[term] = direct_inputs[original_terms[0]] * direct_inputs[original_terms[1]]
                            something_changed = True
                        elif '+' in term:
                            original_terms = term.split('+')
                            direct_inputs[term] = direct_inputs[original_terms[0]] + direct_inputs[original_terms[1]]
                            something_changed = True
                    except KeyError:
                        pass
    
    # calculate prediction from input
    prediction = model_obj['fit'].predict(direct_inputs)
    
    return jsonify(prediction)


def system_recommendations(direct_inputs=None):
    # load system recommendations
    best_practices = load_model("best_practices")
    msgs = []

    for i in input:
        # iterate through system settings and check for anything that could be optimized
        if i in best_practices:
            # if input value isn't already the best practice choice...
            if input[i] != best_practices[i]['value']:
                msgs.append(best_practices[i]['message'])

    return jsonify(msgs)


def update_all_models():
    import os
    models = []
    for f in os.listdir('.'):
        if '.pickle' in f:
            models.append(f.replace('.pickle',''))
    for m in models:
        update_model(m)


@app.route('/predict/<model>/')
def predict_url(model, direct_inputs=None):
    if direct_inputs is None:
        input = request.form
    else:
        input = direct_inputs
        
    return predict(model, input)


@app.route('/bestpractices/')
def system_recommendations_url(direct_inputs=None):
    if direct_inputs is None:
        input = request.form
    else:
        input = direct_inputs

    return system_recommendations(input)


if __name__ == "__main__":
	app.run()