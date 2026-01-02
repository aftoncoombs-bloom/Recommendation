import math
import pandas as pd


PATH_LOGS = "/Users/jeremyvanvalkenburg/Repositories/datasets/logs/logs.csv"
PATH_ORGS = "/Users/jeremyvanvalkenburg/Repositories/datasets/churn/organizations.clean.csv"
PATH_INTEGRATIONS = "/Users/jeremyvanvalkenburg/Repositories/datasets/integrations_org_download.csv"
PATH_CHURNED_ORGS = "/Users/jeremyvanvalkenburg/Repositories/datasets/churn/churned_orgs.csv"
TRANS_PATH = "/Users/jeremyvanvalkenburg/Repositories/datasets/transactions/transactions.csv"

PATH_FTRS = "rf_ftrs.csv"
PATH_MDL = "rf_churn.pkl"

PATH_PRIORPREDS = "churn_warning_preds.csv"

# df_orgs = pd.read_csv(PATH_ORGS)


def get_org_close_date(org):
    if not math.isnan(org):
        return df_orgs[df_orgs['id']==int(org)]['date_closed'].iloc[0]
    else:
        return None


def get_org_id_for_name(x):    
    if x is not None and df_orgs[df_orgs['org_name']==x] is not None and len(df_orgs[df_orgs['org_name']==x]) > 0:
        return df_orgs[df_orgs['org_name']==x]['id'].iloc[0]
    else:
        return None


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


def label_log_entry(msg):
    for i, l in enumerate(entry_labels):
        if l in msg:
            return i
    return None


def update_orgs():
    print("updating org statuses")
    DOMAIN = "https://secure.qgiv.com/"
    URL = "admin/qgivadmin/utilities/export_tables.php"
    post_data = {'key': 'DSQR59VwyFhw21PKDF4K', 'table': 'org'}

    print("\tquerying production for orgs")
    rsp = requests.post(DOMAIN + URL, data=post_data)
    org_data = json.loads(rsp.text)
    orgs = pd.DataFrame(org_data[0])

    orgs['url'] = orgs['website']
    orgs.drop('website', axis=1, inplace=True)
    
    print("\tstoring org data")
    orgs.to_csv(PATH_ORGS, index=False)