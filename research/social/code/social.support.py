import requests


def get_token_facebook(app_id, app_secret):
    '''
    url = "https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&grant_type={}"
    perm_grants = ""
    
    rsp = requests.get(url.format(app_id, app_secret, perm_grants))
    '''
    
    return "{}|{}".format(app_id, app_secret)