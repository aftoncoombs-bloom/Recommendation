'''
Script requires updated organization status and integrations data to perform the 
inference. This data is available from report download end points in the control
panel, not available through the API.

1. Update org status & integrations data every week
2. Update org status & integrations in redshift
3. Run script to predict most likely churn candidates
4. Check inputs for the predicted churn organizations to determine the features that deviate the most from the mean in order to provide some evidence of why they were identified
'''

import psycopg2, datetime
import pandas as pd
from sklearn.externals import joblib


def run_churn_prediction(num_results=50, orgs_to_exclude=[]):
    # load model
    mdl = load_model()

    # load data
    df = load_log_data()

    # perform prediction
    df['y_pred'] = mdl.predict_proba(df.drop('org', axis=1))[:,1]

    # return most confident predictions
    return df[['org', 'y_pred']][~df['org'].isin(orgs_to_exclude)].sort_values('y_pred', ascending=True).iloc[-num_results:]


def load_log_data():
    # query for last 12 months of org log entries
    last_12_months = datetime.date.today() - datetime.timedelta(days=365)
    q = "select * from logs where created>{} and org!=0".format(last_12_months)
    data = redshift_query(q)

    # prep data
    df = pd.DataFrame(data)
    df['org'] = df['org'].fillna(0).astype(int)
    df['systemId'] = df['systemId'].fillna(0).astype(int)
    df['message_label'] = df['message'].apply(label_log_entry)

    df['created'] = pd.to_datetime(df['created'])
    df['month'] = df['created'].dt.month
    df['year'] = df['created'].dt.year
    df['monthyear'] = df.apply(lambda x: str(x['year'])+'/'+str(x['month']), axis=1)
    df = df.merge(pd.get_dummies(df['message_label'],prefix='label'), left_index=True, right_index=True)

    message_label_cols = [c for c in df.columns if 'label_' in c]
    log_agg = df.groupby(['org', 'monthyear'])[message_label_cols].mean().reset_index()
    log_agg['monthyear'] = pd.to_datetime(log_agg['monthyear'])

    # load integrations flags
    q = "select id from integrations"
    integrations_orgs = redshift_query(q)
    log_agg['integrations'] = log_agg['org'].apply(lambda x: 1 if x in integrations_orgs else 0)

    # isolate active orgs
    q = "select id from organizations where status='active'"
    active_orgs = redshift_query(q)
    log_agg = log_agg[log_agg['org'].isin(active_orgs)]

    # return input data
    return log_agg


def load_model():
    # open & process file
    mdl = joblib.load(open('churn.pkl'))

    # return model
    return mdl['model']


def redshift_query(query):
    con = psycopg2.connect(
        dbname="dev",
        host="redshift-cluster-1.ciakb4n4btde.us-east-1.redshift.amazonaws.com",
        port=5439,
        user="redshiftuser",
        password="Keggyg-notpih-farhy4")

    cur = con.cursor()

    cur.execute(query)
    return cur.fetchall()


def label_log_entry(msg):
    entry_labels = [
        "has reached their fundraising",
        "has reached its fundraising",
        "has earned the %badge",
        "had the %badge",
        "donated %amount",
        "made a donation to",
        "was donated to",
        "A donation was made to",
        "% registered",
        "joined %team",
        "has been registered",
        "reset account password",
        "switched donation from",
        "activated recurring",
        "updated donor information",
        "deleted team",
        "Raise Your First Donation",
        "Share on Facebook / Twitter",
        "Upload Your Avatar",
        "Recruit a Team Member",
        "Update Your Personal Page",
        "Send a Fundraising Email",
        "updated organization",
        "added participant",
        "added payment method",
        "edited payment method",
        "deleted payment method",
        "cancelled recurring",
        "deleted participant",
        "changed settings for recipient",
        "resent email receipt to email",
        "updated personal information for transaction",
        "updated donation information for transaction",
        "updated recurring",
        "updated personal information for recurring",
        "updated frequency information for recurring",
        "updated payment method for recurring",
        "updated amount for recurring",
        "updated payment expiration date for recurring",
        "paused recurring",
        "updated billing information for recurring",
        "changed end date",
        "changed start date",
        "updated registration information for transaction",
        "changed code from",
        "changed fee from",
        "voided transaction",
        "linked transaction",
        "unlinked transaction",
        "link transaction",
        "linked recurring",
        "unlinked recurring",
        "added a return for transaction",
        "added a chargeback for transaction",
        "refund",
        "custom report",
        "set form",
        "changed form",
        "changed organization",
        "resent notification",
        "resent admin notification",
        "sent password reset email",
        "edited team",
        "changed maximum quantity",
        "disabled promo",
        "switched participant",
        "switched team",
        "updated account password",
        "added Form widget",
        "updated Form widget",
        "cloned a new form",
        "edited donor",
        "created Fixed Fee",
        "updated Fixed Fee",
        "updated One Time Fee",
        "created One Time Fee",
        "promoted participant",
        "added recipient",
        "sms code",
        "verified donation",
        "changed username",
        "merchant account",
        "signup",
        "edited participant",
        "removed participant",
        "API Access",
        "status from active"
    ]

    for i, l in enumerate(entry_labels):
        if l in msg:
            return i
    return None