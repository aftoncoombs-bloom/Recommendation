import threading
from flask import Flask, jsonify, request
import os, threading, json
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


@app.route('/', methods=['POST'])
def receive_analytics():
    # thread input processing
    rsp = {'success': '1'}

    try:
        t = threading.Thread(target=process_input, args=[request.get_json()])
        t.start()
    except Exception as e:
        rsp['success'] = '0'
        rsp['rsp'] = "Exception threading input: {}".format(e)
    
    # return 200
    return jsonify(rsp)
    
    
def process_input(analytics):
    # need user ID, form ID, and org ID
    fields = ['userIP', 'requestedURL', 'https', 'ssl_tls_sni', 
            'httpHost', 'httpUserAgent', 'httpAccept', 'httpAcceptLanguage',
            'httpAcceptEncoding', 'httpConnection', 'httpReferer',
            'httpCookie', 'httpUpgradeInsecureRequests', 'httpSecFetchDest',
            'httpSecFetchMode', 'httpSecFetchSite', 'path', 'ldLibraryPath',
            'serverSignature', 'serverSoftware', 'serverName', 'serverAddr',
            'serverPort', 'remoteAddr', 'documentRoot', 'requestScheme',
            'contextPrefix', 'contextDocumentRoot', 'serverAdmin',
            'scriptFilename', 'remotePort', 'redirectURL', 
            'redirectQueryString', 'gatewayInterface', 'serverProtocol',
            'requestMethod', 'queryString', 'requestURI', 'scriptName',
            'phpSelf', 'requestTimeFloat', 'requestTime', 'formID', 'orgID']
    
    # process input
    subject = 'Page view'
    message = {}
    for field in fields:
        if field in analytics:
            message[field.lower()] = analytics[field]
    
    # send analytics to SNS
    return publish_sns(SNS_ANALYTICS_TOPIC, subject, json.dumps({'default': json.dumps(message)}), message_is_json=True)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=80)

