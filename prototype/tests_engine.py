import sys
from engine import *
import pandas
from random import randint


def test_load_model(model_file=None):
    print bcolors.BOLD+"Running tests on load_model()..."+bcolors.ENDC

    if model_file is None:
        model_file = 'req_fields'
        print bcolors.WARNING+"-\ttesting with default model file: req_fields"+bcolors.ENDC
    else:
        print "-\ttesting with custom model file: "+model_file

    # test loading existing file
    try:
        legit_mdl = load_model(model_file)
        print u'\u2611'+"\tload_model() successfully loaded existing model file"
    except IOError as err:
        print u'\u2612'+"\tload_model() raised unexpected IOError for model file that should exist"
        return
    except Exception as err:
        print u'\u2612'+"\tload_model() raised unexpected exception: "+repr(error)
        return

    # test loading nonexistent file
    try:
        fake_mdl = load_model('im_not_here')
    except IOError as err:
        print u'\u2611'+"\tload_model() raised appropriate exception for nonexistent model file"
    except Exception as err:
        print u'\u2612'+"\tload_model() raised unexpected exception: "+repr(err)
        return

    # verify loaded model file is a dict and has the expected attributes
    try:
        if not isinstance(legit_mdl, dict):
            raise TypeError("loaded model is not a dict")
        
        if len(legit_mdl) == 0:
            raise TypeError("loaded model has no attributes")

        keys = legit_mdl.keys()
        expected_keys = [u'features', u'calculated_features', u'target', u'last_trained', u'validation_error', u'validation_type', u'output_type']
        intersecting_keys = [i for i in expected_keys if i in keys]
        if len(expected_keys) != len(intersecting_keys):
            raise TypeError("loaded model does not contain the expected keys")

        print u'\u2611'+"\tloaded model has the expected type & attributes"
    except TypeError as err:
        print u'\u2612'+bcolors.FAIL+"\tError in loaded model structure: "+repr(err)+bcolors.ENDC
        return
    except Exception as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected exception raised when validating loaded model structure: "+repr(err)+bcolors.ENDC
        return

    print u'\u2714'+bcolors.OKGREEN+"\t... completed load_model() tests successfully"+bcolors.ENDC


def test_load_training_data():
    print bcolors.BOLD+"Running tests on load_training_data()..."+bcolors.ENDC
    print bcolors.WARNING+"-\tstarting with loading data from CSVs"+bcolors.ENDC

    try:
        d = load_training_data()

        if not isinstance(d, pandas.core.frame.DataFrame):
            raise TypeError("type of return value is not a dataframe")

        expected_columns = ['id_x', 'org_x', 'form', 'timestamp', 'visits', 'mobile_visits', 'don_form_trans_count', 'don_form_trans_vol', 'id_y', 'base', 'org_y', 'total_visits', 'opt_fields', 'req_fields', 'donation_active', 'amounts_system', 'multirestriction_system', 'restrictions', 'pledges_count', 'pledge_active', 'permit_anonymous', 'permit_mobile', 'permit_other_amount', 'enable_donorlogins', 'collect_captcha']
        if (expected_columns == d.columns.values) is False:
            raise TypeError("loaded dataframe does not contain the expected columns")
        
        if len(d) < 100:
            raise TypeError("loaded dataframe contains an unexpectedly low number of observations ("+len(d)+")")

        print u'\u2611'+"\tloaded model has the expected type & attributes"
    except IOError as err:
        print u'\u2612'+bcolors.FAIL+"\tPandas could not find the specified file: "+repr(err)+bcolors.ENDC
    except TypeError as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected type error: "+repr(err)+bcolors.ENDC
        return
    except Exception as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected exception raised when calling load_training_data() with no params: "+repr(err)+bcolors.ENDC
        return

    print u'\u2714'+bcolors.OKGREEN+"\t... completed load_training_data() tests successfully"+bcolors.ENDC


def test_predict(model=None, input_values=None):
    print bcolors.BOLD+"Running tests on predict()..."+bcolors.ENDC

    if model is None:
        print bcolors.WARNING+"-\ttesting with default model file: req_fields"+bcolors.ENDC
        model = 'req_fields'
    else:
        print bcolors.WARNING+"-\ttesting with model file: "+str(model)+bcolors.ENDC
        model = model
        
    if input_values is None:
        print bcolors.WARNING+"-\ttesting with default input values"+bcolors.ENDC
        input_values = {
            "opt_fields": 1,
            "req_fields": 1,
            "donation_active": 1,
            "multirestriction_system": 0,
            "restrictions": 5,
            "pledges_count": 0,
            "pledge_active": 0,
            "permit_anonymous": 1,
            "permit_mobile": 1,
            "permit_other_amount": 1,
            "enable_donorlogins": 1,
            "collect_captcha": 0,
            "day": 12,
            "month": 2
        }

    try:
        response = predict(model, input_values)
    except Exception as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected exception raised when calling predict(): "+repr(err)+bcolors.ENDC
        return

    print u'\u2714'+bcolors.OKGREEN+"\t... completed predict() tests successfully"+bcolors.ENDC


def test_train_model():
    print bcolors.BOLD+"Running tests on train_model()..."+bcolors.ENDC
    print bcolors.WARNING+"-\ttesting with dummy model data"+bcolors.ENDC

    try:
        # load model
        mdl = get_dummy_model()
        # get dummy data w/ predictable training pattern
        dummy_data = get_dummy_data()

        # get trained model new weights
        rsp = train_model(mdl, dummy_data)

        # compare weight count
        feature_count = len(mdl['features']) + len(mdl['calculated_features'])
        if (feature_count + 1) != len(rsp.coef_):
            raise TypeError("model feature count & trained model coefficient count do not match")

        # check that weights are realistic?
    except TypeError as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected type error: "+repr(err)+bcolors.ENDC
        return
    except Exception as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected exception raised when calling train_model(): "+repr(err)+bcolors.ENDC
        return

    print u'\u2714'+bcolors.OKGREEN+"\t... completed train_model() tests successfully"+bcolors.ENDC


def test_update_model():
    print bcolors.BOLD+"Running tests on update_model()..."+bcolors.ENDC
    print bcolors.WARNING+"-\ttesting with dummy model data"+bcolors.ENDC

    try:
        # send dummy data to update_model() to update the file
        update_model('dummy')

        # load dummy file to verify changes were written
        ld_dummy_mdl = load_model('dummy')

        # compare model weight counts
        mdl_feature_count = len(dummy_mdl['features']) + len(dummy_mdl['calculated_features'])
        ld_mdl_feature_count = len(ld_dummy_mdl['features']) + len(ld_dummy_mdl['calculated_features'])
        if mdl_feature_count != ld_mdl_feature_count:
            raise TypeError("model feature count & loaded model feature count do not match")
        
        print u'\u2611'+"\tupdated dummy model has the expected number of coefficients"

        # compare values of weights between the dummy model and the loaded dummy model
        for i in dummy_mdl['features']:
            if ld_dummy_mdl['features'][i] == dummy_mdl['features'][i]:
                raise TypeError("model feature value & loaded model feature value do not match for index ("+str(i)+")")
        
        print u'\u2611'+"\tupdated dummy model coefficient values match those of the original dummy model (for features)"

        for i in dummy_mdl['calculated_features']:
            if ld_dummy_mdl['calculated_features'][i] != dummy_mdl['calculated_features'][i]:
                raise TypeError("model complication term value & loaded model complication term value do not match for index ("+str(i)+")")

        print u'\u2611'+"\tupdated dummy model coefficient values match those of the original dummy model (for complication terms)"

    except TypeError as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected type error: "+repr(err)+bcolors.ENDC
        return
    except Exception as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected exception raised when calling update_model(): "+repr(err)+bcolors.ENDC
        return

    print u'\u2714'+bcolors.OKGREEN+"\t... completed update_model() tests successfully"+bcolors.ENDC


def test_system_recommendations():
    print bcolors.BOLD+"Running tests on system_recommendations()..."+bcolors.ENDC
    print bcolors.WARNING+"-\ttesting with best practices file data"+bcolors.ENDC

    try:
        best_practices = load_model("best_practices")
        print bcolors.WARNING+"-\tloaded best practices file to local object"+bcolors.ENDC
        
        for bp in best_practices:
            if best_practices[bp]['value'] == '1':
                best_practices[bp]['value'] = '0'
            elif best_practices[bp]['value'] == '0':
                best_practices[bp]['value'] = '1'

        print bcolors.WARNING+"\tflipped all values in best practices object"+bcolors.ENDC
        
        best_practices_count = len(best_practices)

        best_practices_recommendations = system_recommendations(best_practices)

        if best_practices_count != len(best_practices_recommendations):
            raise TypeError("number of recommendation messages does not match the number of misaligned inputs")
    except TypeError as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected type error: "+repr(err)+bcolors.ENDC
        return
    except Exception as err:
        print u'\u2612'+bcolors.FAIL+"\tUnexpected exception raised when calling system_recommendations(): "+repr(err)+bcolors.ENDC
        return

    print u'\u2714'+bcolors.OKGREEN+"\t... completed system_recommendations() tests successfully"+bcolors.ENDC


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_dummy_model():
    return []


def get_dummy_data():
    return []


# run all the tests
test_load_model()
test_load_training_data()
test_predict()
test_system_recommendations()