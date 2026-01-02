from datetime import datetime
from analytics import load_analytics as load_ga_analytics
import pandas as pd
import numpy as np
from db import update_rows, insert_rows, select_rows, select_to_dataframe, execute_query
import requests, json


def run_updates(debug=False):
    if debug:
        print("PRODUCTION ANALYTICS UPDATE")

    # load ID of last analytics entry
    last_analytics_entry = select_rows('analytics_base', order_by="-id", limit=1)

    if debug:
        print("\tlast analytics entry ID: {}".format(last_analytics_entry['id'].iloc[0]))
    
    # pull analytics copy from production & delete source
    last_analytics_entry_id = last_analytics_entry['id'].iloc[0]
    analytics_log = load_analytics_chain(last_id=last_analytics_entry_id, debug=debug)
    analytics_log.append({'last_id': last_analytics_entry_id})
    
    if debug:
        print("PRODUCTION TRANSACTIONS UPDATE")

    # update transaction data, set is_returning_donor & fraud flags
    last_transaction_entry = select_rows('transactions', order_by="-id", limit=1)
    
    if debug:
        # print("\tlast transaction entry: {}".format(last_transaction_entry))
        print("\tlast transaction entry ID: {}".format(last_transaction_entry['id'].iloc[0]))

    last_transaction_entry_id = last_transaction_entry['id'].iloc[0]
    transaction_log = load_transactions(last_id=last_transaction_entry_id, debug=debug)
    transaction_log.append({'last_id': last_transaction_entry_id})

    if debug:
        print("GOOGLE ANALYTICS ANALYTICS UPDATE & PROCESSING")

    # pull GA data since last date entered
    last_ga_entry = select_rows('ga_form', fields=['date'], order_by="-date", limit=1)

    if debug:
        print("\tlast GA entry: {}".format(last_ga_entry['date'].iloc[0]))

    # get days since last entry... +1 to account for time since midnight
    date_format = "%Y-%m-%d"
    days_to_pull = (datetime.now() - datetime.strptime(str(last_ga_entry['date'].iloc[0]), date_format)).days + 1
    days_to_pull = min(days_to_pull, 5)

    ga_analytics_log = {'days_to_pull': days_to_pull}

    if debug:
        print("\tGA days to pull: {}".format(ga_analytics_log))
        print("\tpulling GA form analytics")
    # pull GA analytics
    ga_entries = load_ga_analytics(days_to_pull, add_account_ids=False)
    insert_rows('ga_form', data=ga_entries, columns=ga_entries[0].keys())
    ga_analytics_log['entries_added'] = len(ga_entries)

    if debug:
        print("\t\t{} form analytics pulled".format(len(ga_entries)))
        print("\t\tpulling GA account analytics")

    ga_account_entries = load_ga_analytics(days_to_pull, add_account_ids=True)
    insert_rows('ga_accounts', data=ga_account_entries, columns=ga_account_entries[0].keys())
    ga_analytics_log['account_entries_added'] = len(ga_account_entries)

    if debug:
        print("\t\t{} account analytics pulled".format(len(ga_account_entries)))

    '''
    PROCESS DATA AGGREGATES
    - set form ID for path/key in google analytics
    - calculate aggregate data for daily & lifetime
    - update transaction means and diffs
    '''
    if debug:
        print("PROCESS DATA AGGREGATES")
        print("\tsetting form ID's")
    # set form ID's by path for google page views
    form_keys = select_rows("form", fields=['path', 'id'])
    for _, fk in form_keys.iterrows():
        update_rows("ga_form",
            data=[[fk['id']]],
            columns=["form"],
            where="path LIKE '%%/for/{}/%%' OR path LIKE '%%/event/{}/%%'".format(fk['path'], fk['path'])
        )

    if debug:
        print("\tcalculating aggregates")
        print("\t\tupdating daily stats")

    # calculate aggregate data for daily & lifetime
    ## update daily data
    form_page_views = select_rows('ga_form', 
        fields=["SUM(views) AS visits", "form"],
        where="date='{}'".format(datetime.now().strptime(format)),
        group_by=["form"]
    )
    trans_avgs_daily = select_rows('transactions',
        fields=[
            "SUM(amount) AS trans_sum", 
            "COUNT(id) AS trans_count", 
            "AVG(amount) AS trans_amount_mean", 
            "STD(amount) AS trans_amount_std", 
            "AVG(hour) AS trans_hour_mean", 
            "STD(hour) AS trans_hour_std",
            "form"
        ],
        where="date='{}'".format(datetime.now().strftime(date_format)),
        group_by=["form"]
    )
    if len(form_page_views) < len(trans_avgs_daily):
        daily_data = form_page_views.merge(trans_avgs_daily, on="form", how="left")
    else:
        daily_data = trans_avgs_daily.merge(form_page_views, on="form", how="left")

    for e in daily_data.dropna().iterrows():
        update_rows("form_daily", 
            data=e.drop('form', axis=1).values, 
            columns=e.drop('form', axis=1).columns, 
            where="date='{}' and id={}".format(datetime.now().strftime(date_format), e['form'])
        )
    
    if debug:
        print("\t\tupdating form lifetime stats")

    ## udpate overall data
    trans_avgs = select_rows('transactions',
        fields=[
            "AVG(amount) AS trans_amount_mean", 
            "STD(amount) AS trans_amount_std", 
            "AVG(hour) AS trans_hour_mean", 
            "STD(hour) AS trans_hour_std", 
            "AVG(day) AS trans_day_mean", 
            "STD(day) AS trans_day_std",
            "AVG(is_fraud) AS mean_fraud",
            "form"
        ],
        group_by=["form"]
    )

    for e in trans_avgs.iterrows():
        update_rows("form", 
            data=e.drop('form', axis=1).values, 
            columns=e.drop('form', axis=1).columns,
            where="id={}".format(e['form'])
        )
    
    if debug:
        print("\t\tupdating transaction diffs")

    ## update transaction diffs from new means
    query = "UPDATE transactions AS T JOIN form AS F ON T.form=F.id SET \
        T.mean_diff_amount=ABS(T.amount-F.trans_amount_mean), \
        T.mean_diff_hour=ABS(T.hour-F.trans_hour_mean), \
        T.mean_diff_day=ABS(T.day-F.trans_day_mean)"
    execute_query(query)

    return [analytics_log, transaction_log, ga_analytics_log]

        
def load_analytics_chain(last_id=None, limit=1000, debug=False):
    more_to_pull = True
    log = []
    if debug:
        limit = 5
    
    last_id += 1

    while more_to_pull:
        if debug:
            print("\t\t\tfetching analytics")
        content = fetch_analytics(last_id=last_id, limit=limit, debug=debug)
        log.append({"analytics_entries_added_len": len(content)})

        if len(log) == 0:
            log.append({"first_analytics_id_inserted": content[0]['id']})

        # if data pulled is less than the limit, than there aren't any more to pull
        if debug:
            more_to_pull = False
        else:
            more_to_pull = len(content) < limit

        start_id = None
        end_id = None

        for row in content:
            if start_id is None or start_id > row['id']:
                start_id = row['id']
            if end_id is None or end_id < row['id']:
                end_id = row['id']

            row['form'] = row['entity']
            del(row['entity'])
            del(row['entityType'])

            # pull the sub lists from the row for p2p, qgiv, etc.
            if 'analytic_p2p' in row or 'analytic_p2p_stats' in row:
                if len(row['analytic_p2p']) > 0:
                    # pull analytic_p2p & analytic_p2p_stats, merge & insert
                    del(row['analytic_p2p']['id'])
                    del(row['analytic_p2p']['stats'])
                    p2p_data = row['analytic_p2p']
                    p2p_data.update(row['analytic_p2p_stats'])
                    
                    insert_rows('analytics_p2p', data=[p2p_data.values()], columns=p2p_data.keys())

                del(row['analytic_p2p'])
                del(row['analytic_p2p_stats'])
            if 'analytic_qgiv' in row or 'analytic_qgiv_stats' in row:
                if len(row['analytic_qgiv']) > 0:
                    # pull analytic_qgiv & analytic_qgiv_stats, merge & insert
                    del(row['analytic_qgiv']['id'])
                    qgiv_data = row['analytic_qgiv']
                    qgiv_data.update(row['analytic_qgiv_stats'])
                    del(qgiv_data['stats'])
                    
                    insert_rows('analytics_qgiv', data=[qgiv_data.values()], columns=qgiv_data.keys())

                del(row['analytic_qgiv'])
                del(row['analytic_qgiv_stats'])
            if 'analytic_cms' in row:
                '''
                if len(row['analytic_cms']) > 0:
                    insert_rows('analytics_cms', data=[row['analytic_cms'].values()], columns=row['analytic_cms'].keys())
                '''
                del(row['analytic_cms'])
            if 'analytic_qgiv_event' in row or 'analytic_qgiv_event_stats' in row:
                '''
                if len(row['analytic_qgiv_event']) > 0:
                    for e in row['analytic_qgiv_event']:
                        for es in row['analytic_qgiv_event_stats']:
                            if 'id' in es and e['stats'] == es['id']:
                                del(e['id'])
                                del(es['id'])
                                qgiv_event_data = e
                                qgiv_event_data.update(es)
                        
                                insert_rows('analytics_qgiv_event', data=[qgiv_event_data.values()], columns=qgiv_event_data.keys())
                '''
                del(row['analytic_qgiv_event'])
                del(row['analytic_qgiv_event_stats'])
            
            # update form path & product type
            curr_entry = select_rows('form', fields=['id'], where="id={}".format(int(row['form'])))
            if len(curr_entry):
                update_rows('form', data=[[row['path'], row['product']]], columns=['path', 'type'], where="id={}".format(row['form']))
            else:
                insert_rows('form', data=[[row['form'], row['org'], row['path'], row['product']]], columns=['id', 'org', 'path', 'type'])
            del(row['path'])
            del(row['product'])
            
            # insert analytic_base
            insert_rows('analytics_base', data=[row.values()], columns=row.keys())
        
        # done importing data, delete them from production
        if start_id is not None and end_id is not None:
            payload = dict(key='DSQR59VwyFhw21PKDF4K', delete=str(start_id)+':'+str(end_id))
            headers = {'content-type' : 'application/json'}
            
            print("DEBUG deleting analytics entries from {} to {}".format(start_id, end_id))
            
            url = 'https://secure.qgiv.com/admin/qgivadmin/utilities/export_analytics.php'
            rsp = requests.post(url, data=payload, headers=headers)
            try:
                content = json.loads(rsp.text)
            except Exception as e:
                print("DEBUG json error from analytics delete call: {}".format(e))
                print("DEBUG response text: {}".format(rsp.text))

            print("DEBUG delete request response: {}".format(content))
    
    log.append({"last_analytics_id_inserted": end_id})
    return log


def load_transactions(last_id=None, pull_date=None, debug=False):
    from datetime import timedelta, datetime
    more_to_pull = True
    limit = 5000
    log = []
    last_id_inserted = None

    if debug:
        limit = 5

    # limit iterations here so it doesn't run out of control for hundreds of iterations trying to catch up
    counter = 0

    while more_to_pull:
        if debug:
            print("\t\t\tfetching transactions")
        # pull transactions from production
        trans_df = fetch_transactions_df(last_id=last_id, pull_date=pull_date, limit=limit, debug=debug)

        log.append({'first_transaction_id_inserted': trans_df["id"].iloc[0]})

        # if the number of transactions returned equals limit, there are most likely more
        if len(trans_df) < limit or debug:
            more_to_pull = False
            if debug and len(trans_df) > 5:
                trans_df = trans_df.head()
        
        # get the new last ID
        last_id = trans_df["id"].iloc[-1]

        if 'refunds' in trans_df.columns:
            trans_df.drop('refunds', axis=1, inplace=True)
        if 'chargebacks' in trans_df.columns:
            trans_df.drop('chargebacks', axis=1, inplace=True)
        if 'recurring_creatingTransaction' in trans_df.columns:
            trans_df.drop('recurring_creatingTransaction', axis=1, inplace=True)

        # insert data
        trans_df['date'] = pd.to_datetime(trans_df['date'])
        trans_df['date'] = trans_df.apply(lambda r:  "{} {}:00:00".format(r['date'].strftime('%Y-%m-%d'), r['hour']), axis=1)
        
        insert_rows('transactions', data=trans_df.values, columns=trans_df.columns)

        # update is_returning_donor & fraud within flag
        day_ago = datetime.today() - timedelta(days=1)
        form_fraud_within_day = []
        for _, row in trans_df.iterrows():
            t_data = {"is_returning_donor": 0}

            # checking if we've seen this email before
            if row['email']:
                prior_transactions = select_rows('transactions', fields=['count(id)'], where="email='{}'".format(row['email']))
                if len(prior_transactions) > 1:
                    t_data['is_returning_donor'] = 1

            # update the transaction row if either value has changed
            if t_data['is_returning_donor']:
                update_rows('transactions', data=[t_data.values()], columns=t_data.keys(), where="id={}".format(int(row['id'])))
        
        # check iteration counter, cap at 4 (20k transactions)
        counter += 1
        if counter == 4:
            break

    log.append({'last_transaction_id_inserted': last_id})
    return log


def fetch_analytics(last_id=None, limit=2500, debug=False):
    # make sure there's a limit that doesn't exceed 10k, otherwise set to 2500
    if debug:
        limit = 5
    elif limit is None or int(limit) > 10000:
        limit = 2500

    # retrieve analytics data
    url = 'https://secure.qgiv.com/admin/qgivadmin/utilities/export_analytics.php'
    if last_id is not None:
        payload = dict(key='DSQR59VwyFhw21PKDF4K', last_id=last_id, limit=limit)
    else:
        payload = dict(key='DSQR59VwyFhw21PKDF4K', limit=limit)
    
    rsp = requests.post(url, data=payload)
    content = json.loads(rsp.text)

    return content['data']


def fetch_transactions_df(last_id=None, pull_date=None, limit=5000, debug=False):
    url = 'https://secure.qgiv.com/admin/qgivadmin/statistics/trans_export.php'
    payload = dict(key='DSQR59VwyFhw21PKDF4K', last_id=last_id, limit=limit)

    rsp = requests.post(url, data=payload)
    content = json.loads(rsp.content)

    trans_df = pd.DataFrame(content, columns=content[0].keys())
    trans_df['timestamp'] = pd.to_datetime(trans_df['timestamp'])
    trans_df['hour'] = trans_df['timestamp'].dt.hour
    trans_df['day'] = trans_df['timestamp'].dt.dayofweek
    trans_df['month'] = trans_df['timestamp'].dt.month
    trans_df['date'] = trans_df['timestamp'].dt.date
    trans_df.drop('timestamp', axis=1, inplace=True)

    trans_df['is_fraud'] = trans_df['error'].str.contains("fraud|Fraud")
    trans_df.drop('error', axis=1, inplace=True)

    return trans_df
