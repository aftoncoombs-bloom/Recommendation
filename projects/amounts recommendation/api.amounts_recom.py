from flask import Flask, jsonify, request, g
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
                'message': "{} entries retreived".format(len(df))
            }
    except:
        rsp['message'] = 'DB connect failed'

    # respond
    return jsonify(rsp)

        
@app.route('/amounts_rec_data/', methods=['POST'])
def get_amounts_recommendation_data():
    print("get_amounts_recommendation_data()")
    key = 'tIHLM2vNlBwvlZlqdKy8'
    _input = request.get_json()
    
    if 'key' not in _input or _input['key'] != key:
        print("Request with incorrect input: {}".format(_input))
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        print("Request with correct input received")
        try:
            # return S3 url
            bucket = 'qgiv-stats-data'
            filename = 'recommended_amounts.cache.csv'
            df = get_dataframe_from_file(bucket, filename)

            # replace NaN with 'null' for json
            df.fillna('null', inplace=True)

            rsp = {
                'success': '1',
                'data': df.to_dict(orient='records')
            }
        except Exception as e:
            print("Exception occurred")
            print(e)
            rsp = {
                'success': '0',
                'errors': str(e)
            }
            
    return jsonify(rsp)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)