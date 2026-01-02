import datetime
import pandas as pd
import numpy as np
from sklearn.externals import joblib
from churn_support import *


print("load features")
df_orgs = pd.read_csv(PATH_ORGS, low_memory=False)
df_priorpreds = pd.read_csv(PATH_PRIORPREDS, low_memory=False)
df_trans = pd.read_csv(TRANS_PATH, low_memory=False)

print("\tprepping active org filter for status and activity")
# status filter
target_active_orgs = df_orgs[df_orgs['status']==1]['id'].tolist()

# activity filter
six_months_ago = datetime.date.today() - datetime.timedelta(6*365/12)
df_trans['date'] = pd.to_datetime(df_trans['date'])
df_trans_orgdate = df_trans[df_trans['date']>=six_months_ago][['date', 'org']]
df_trans_agg = df_trans_orgdate.groupby('org')['date'].count().reset_index()
# narrow org list to active orgs with more than 10 transactions in the last 6 months
target_active_orgs = df_trans_agg[(df_trans_agg['date']>=10)&(df_trans_agg['org'].isin(target_active_orgs))]['org'].tolist()

# load and format features
df_reformatted = pd.read_csv(PATH_FTRS)
# filter to active orgs
df_reformatted = df_reformatted[df_reformatted['org'].isin(target_active_orgs)]
ftrs = df_reformatted[(~df_reformatted['churned'])&(~df_reformatted['org'].isin(df_priorpreds['org'].tolist()))].drop(['churned', 'org', 'reindex'], axis=1).fillna(0.)

print("load model")
mdl = joblib.load(open(PATH_MDL, 'rb'))

print("perform prediction")
y_pred = mdl.predict_proba(ftrs)
y_pred_df = pd.DataFrame(y_pred)
y_pred_df['org'] = df_reformatted[~df_reformatted['churned']]['org']
top_preds = y_pred_df.sort_values(1, ascending=False).head(10).dropna()

predicted_orgs = top_preds['org'].tolist()

print("add predictions to history")
tdy = datetime.datetime.today()

y_preds_df = pd.DataFrame([{'org': o, 'date_predicted': tdy} for o in predicted_orgs])
df_priorpreds = df_priorpreds.append(y_preds_df)
df_priorpreds['org'] = df_priorpreds['org'].astype(int)
df_priorpreds.to_csv(PATH_PRIORPREDS, index=False)

print("Report:")
print("-"*40)
y_pred_orgs = y_pred_df[~y_pred_df['org'].isna()].sort_values(1, ascending=False).head()['org'].tolist()

labels = []
for f in ftrs.columns:
    if 'month_0' in f:
        labels.append(f.replace('month_0_', ''))

for o in y_pred_orgs:
    inp = df_reformatted[df_reformatted['org']==o]
    
    print("Organization {}".format(int(o)))
    label_diffs = {}
    for c in inp.drop(['org', 'churned', 'reindex'], axis=1).columns:
        if c == 'integrations':
            print("\tintegrations: {}".format(inp[c].iloc[0]))
        else:
            label_diffs[c] = inp[c].fillna(0).iloc[0] - df_reformatted[c].mean()
            
    these_vals_means = {}
    for l in labels:
        these_vals = []
        for k in label_diffs.keys():
            if l in k:
                these_vals.append(label_diffs[k])
        
        these_vals_means[entry_labels[int(l.replace('label_', ''))]] = np.mean(these_vals)
    
    decision_statement = []
    for e in sorted(these_vals_means.items(), key=lambda kv: kv[1]):
        if abs(e[1]) > 0.015:
            if e[1] > 0.:
                decision_statement.append("{} (up)".format(e[0]))
            else:
                decision_statement.append("{} (down)".format(e[0]))
    print("\t{}".format(", ".join(decision_statement)))