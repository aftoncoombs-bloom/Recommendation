import requests, json
import pandas as pd
import numpy as np
import pickle as pkl

# LOAD DATA
URL = "https://secure.qgiv.com/admin/qgivadmin/utilities/export_product_adoption.php"
KEY = "DSQR59VwyFhw21PKDF4K"

rsp = requests.post(URL, data={'key': KEY})
data = json.loads(rsp.text)

# FORMATTING
## get org & form counts
len_orgs = len([])
len_forms = len([])

imp_data = data['implementation_data']
bid_data = data['bidirectional_data']

def get_org_data(data_set):
    count_key = [e for e in data_set[0].keys() if 'count' in e][0]
    avg_value = "{:.2f}".format(np.mean([int(e[count_key]) for e in data_set]))
    
    percentage_text = "{:.2f}%".format((float(len(data_set)) / float(len_orgs)) * 100)
    note_text = "{} orgs; {} per org".format(len(data_set), avg_value)
    
    return {'value': percentage_text, 'note': note_text}


def get_form_data(data_set):
    count_key = [e for e in data_set[0].keys() if 'count' in e][0]
    avg_value = "{:.2f}".format(np.mean([int(e[count_key]) for e in data_set]))
    
    percentage_text = "{:.2f}%".format((float(len(data_set)) / float(len_forms)) * 100)
    note_text = "{} forms; {} per form".format(len(data_set), avg_value)
    
    return {'value': percentage_text, 'note': note_text}

adoption_data = {}
all_keys = list(set(list(imp_data.keys()) + list(bid_data.keys())))

for k in all_keys:
    imp_entry = {}
    bid_entry = {}
    inst_entry = {}
    
    if k in imp_data and imp_data[k] is not None:
        if type(imp_data[k]) == str:
            imp_entry = {'count': imp_data[k]}
        elif type(imp_data[k][0]) == str:
            imp_entry = {'count': len(imp_data[k])}
        elif 'org' in imp_data[k][0].keys():
            imp_entry = get_org_data(imp_data[k])
        elif 'form' in imp_data[k][0].keys():
            imp_entry = get_form_data(imp_data[k])
    if k in bid_data and bid_data[k] is not None:
        if 'org' in bid_data[k][0].keys():
            bid_entry = get_org_data(bid_data[k])
        elif 'form' in bid_data[k][0].keys():
            bid_entry = get_form_data(bid_data[k])
            
        
    adoption_data[k] = {
        'implemented': imp_entry,
        'bidirectional': bid_entry,
        'institutional': inst_entry
    }
    
pkl.dump(adoption_data, open("adoption_data.pkl", "wb"))