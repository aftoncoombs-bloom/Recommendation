import json, requests
from datetime import datetime


def handler(event, context):
    # localize message
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # push message to matomo
    rsp = publish_to_matomo(message)

    print("Request status: {}".format(rsp))
    return rsp==200


def publish_to_matomo(pageview):
    matomo_url = 'https://matomo.qgiv.com/matomo.php'

    pageview_time = datetime.fromtimestamp(pageview['requesttime'])

    params = {
        'idsite': '1',
        'rec': '1',
        'action_name': 'Backend pageview',
        'apiv': '1',
        'token_auth': '20e9d5eeece2562bb882cb1e39f76828',
        'cdt': pageview['requesttime'],
        'cip': pageview['userip'],
        'url': pageview['requestedurl'],
        'urlref': pageview['httpreferer'],
        'h': pageview_time.hour,
        'm': pageview_time.minute,
        's': pageview_time.second,
        'ua': pageview['httpuseragent'],
        'dimension[1]': pageview.get('formid', None),
        'dimension[0]': pageview.get('orgid', None)
    }

    request_str = matomo_url + '?' + '&'.join(['{}={}'.format(c, params[c]) for c in params])

    rsp = requests.get(request_str)

    return rsp.status_code