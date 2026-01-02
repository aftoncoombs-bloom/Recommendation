from flask import Flask, jsonify, request, g
import numpy as np
import pandas as pd
import datetime
from s3_support import *


app = Flask(__name__)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

MEDIAN_BIDS = None
MEDIAN_BIDS_UPDATED = None
Q = '''select
            count(b.ticketholder) as bids
       from bidders as b
            left join transauction as ta on b.product=ta.product
       group by ta.product'''


'''
Calculates the performance score of a given auction item based upon the data passed in via POST.

Expected inputs:
- value (float): value of the given item provided by the admin
- bid_increment (float)
- reserve (float)
- bids (int): total number of bids placed on the item
- winning_bid (float): value of the winning bid
'''
@app.route('/auctionitemscore/', methods=['POST'])
def auction_item_score(testing=False):
    try:
        # localize parameters
        post_data = request.form.to_dict()
        post_data['bidincrement_ratio'] = post_data['bidincrement'] / post_data['value']
        post_data['reserve_ratio'] = post_data['reserve'] / post_data['value']
        post_data['price_ratio'] = post_data['winning_bid'] / post_data['value']
    
        # calculate median bids
        week_ago = MEDIAN_BIDS_UPDATED - datetime.timedelta(days=7)
        if MEDIAN_BIDS is None or (MEDIAN_BIDS_UPDATED is not None and MEDIAN_BIDS_UPDATED <= week_ago):
            MEDIAN_BIDS = redshift_query_read(Q, schema='production')['bids'].median()
            MEDIAN_BIDS_UPDATED = datetime.datetime.now()
    
        # calculate score
        item_score = calculate_score(post_data, MEDIAN_BIDS)
        
        rsp = {'status': '1', 'data': item_score}
    except Exception as e:
        rsp = {'status': '0', 'error': str(e)}
    
    # return
    if testing:
        return rsp
    else:
        return jsonify(rsp)
    

def calculate_score(item, bids_median):
    scores = []
    # bidincrement_score
    scores.append(item['bidincrement_ratio']>=0.10)
    # reserve_score
    scores.append(item['reserve_ratio']>=0.25)
    # bids_score
    scores.append(item['bids']>=bids_median)
    # winningbid_score
    scores.append(item['price_ratio']>=1.0)
    
    return np.mean(scores)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8899")