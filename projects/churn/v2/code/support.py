import math
import pandas as pd
import numpy as np

import sys
sys.path.insert(1, '../../../../scripts/')
from s3_support import *


PATH_FTRS = "rf_ftrs.csv"
PATH_MDL = "rf_churn.pkl"


def get_orgs_logged_in_last_3_months():
    q = '''select
                distinct(users.org) as org
            from login
                left join users on login.user_id=users._id
            where
                login.original_timestamp >= add_months(current_date, -3);'''
    
    return redshift_query_read(q, schema="secure")


def get_diff_mean_growth_churned(churned_orgs_ids):
    q = '''select
                org,
                count(distinct form) as forms,
                date_trunc('month', date) as month,
                count(id) as count,
                sum(amount) as volume
            from transactions
                where status='A'
                group by org, date_trunc('month', date)
                order by date_trunc('month', date) desc;'''
    df_trans_agg = redshift_query_read(q)
    df_trans_agg['month'] = pd.to_datetime(df_trans_agg['month'])
    df_trans_agg.sort_values('month', ascending=True, inplace=True)

    org_growth_data = []

    for org in df_trans_agg['org'].unique():
        this_df = df_trans_agg[df_trans_agg['org']==org].copy()
        if len(this_df) <= 1:
            continue
        this_df['growth'] = this_df['volume'].diff() / this_df['volume'].shift(1)

        org_growth_data.append({
            'org': org,
            'growth': this_df['growth'].replace([np.inf, -np.inf], np.nan).dropna().mean()
        })

    growth_df = pd.DataFrame(org_growth_data)
    growth_df['churned'] = growth_df['org'].isin(churned_orgs_ids)
    
    mean_churned_growth_rate = growth_df[growth_df['churned']]['growth'].mean()
    
    growth_df['mean_diff_growth_churned'] = growth_df['growth'] - mean_churned_growth_rate
    
    return growth_df[['org', 'mean_diff_growth_churned']]


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