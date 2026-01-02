import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl
from sklearn.model_selection import train_test_split
from churn_support import *
import datetime

import sys
sys.path.insert(1, '../../../../scripts/')
from s3_support import *

print("-"*20)
print("prepping features")
print("-"*20)


print("\treading in logs, integrations, transactions, and orgs")
df_orgs = get_dataframe_from_file("qgiv-stats-data", "organizations.names.csv")
df_logs = redshift_query_read("select * from logs")
df_integrations = get_dataframe_from_file("qgiv-stats-data", 'integrations.csv')
df_trans = redshift_query_read("select * from transactions where status='A' and date>=DATEADD('month', -6, CURRENT_DATE)")

print("\tisolating churned orgs")
df_churned_orgs = df_orgs[~df_orgs['date_closed'].isnull()]

print("\tgetting P2P org list from transaction history")
p2p_orgs = df_trans[df_trans.source=='p2p']['org'].unique().tolist()

print("\tfiltering orgs with fewer than 100 transactions")
orgs_trans_counts = df_trans.groupby('org')['id'].count().reset_index()
orgs_never_viable = orgs_trans_counts[orgs_trans_counts['id']<100]['org'].tolist()

print("\tprepping logs data")
print("\t\tset message labels and date values")
df_logs['created'] = pd.to_datetime(df_logs['created'])
df_logs['month'] = df_logs['created'].dt.month
df_logs['year'] = df_logs['created'].dt.year
df_logs = df_logs[~df_logs['org'].isin(orgs_never_viable)]
df_logs['monthyear'] = df_logs.apply(lambda x: str(x['year'])+'/'+str(x['month']), axis=1)
df_logs['message_label'] = df_logs['message'].apply(label_log_entry)
df_logs = df_logs.merge(pd.get_dummies(df_logs['message_label'],prefix='label'), left_index=True, right_index=True)

print("\t\taggregate log label values per org per month")
message_label_cols = [c for c in df_logs.columns if 'label_' in c]
log_agg = df_logs.groupby(['org', 'monthyear'])[message_label_cols].mean().reset_index()

print("\t\textract last 12 months of log entries per organization")
agged_org_data = []
log_agg['monthyear'] = pd.to_datetime(log_agg['monthyear'])

for o in log_agg['org'].unique():
    _agg = log_agg[log_agg['org']==o].copy()
    _agg.sort_values('monthyear', ascending=False, inplace=True)
    _this_data = _agg.iloc[-12:].copy()
    _this_data['reindex'] = 0
    counter = 0
    for _, r in _this_data.iterrows():
        r['reindex'] = counter
        agged_org_data.append(r.to_dict())
        counter += 1

df_agged = pd.DataFrame(agged_org_data)
df_agged['churned'] = df_agged['org'].isin(df_churned_orgs['id'].tolist())
df_agged = df_agged[df_agged['org']!=0]

print("\tcompiling integrations with logs")
df_agged['integrations'] = df_agged['org'].isin(df_integrations['org'].unique())


print("-"*20)
print("training models")
print("-"*20)

ftr_cols = [c for c in df_agged.columns if 'label_' in c] + ['integrations']
target_col = 'churned'

print("\ttrain simple model for feature selection")
train_X, test_X, train_y, test_y = train_test_split(df_agged[ftr_cols], df_agged[target_col], test_size=0.33)

rf = RandomForestClassifier(n_estimators=1000)
rf.fit(train_X, train_y)

feats = {} # a dict to hold feature_name: feature_importance
for feature, importance in zip(train_X.columns, rf.feature_importances_):
    feats[feature] = importance #add the name/value pair 

# isolate the most important features from the simple model for the real model
importances = pd.DataFrame.from_dict(feats, orient='index').rename(columns={0: 'Gini-importance'})
important_ftrs = importances.sort_values(by='Gini-importance').iloc[-10:].reset_index()["index"]
# list formatting the important features output
important_ftrs = list(important_ftrs)

print("\tfull model training with best features from simple model")
print("\t\treformatting training data for optimized features")
# reformat dataset to include the most important features for the last 12 months of logs so that we have 1 row per organization
reformatted_data = []
for o in df_agged['org'].unique():
    _df = df_agged[df_agged['org']==o][important_ftrs+['org', 'reindex', 'churned']]
    
    _this_org_data = {}
    for _, r in _df.sort_values('reindex', ascending=True).iterrows():
        for c in _df.columns:
            if 'label_' in c:
                _this_org_data["month_{}_{}".format(r['reindex'], c.replace('.0', ''))] = r[c]
            elif c not in _this_org_data:
                _this_org_data[c] = r[c]
    reformatted_data.append(_this_org_data)
                
df_reformatted = pd.DataFrame(reformatted_data)
df_reformatted['integrations'] = df_reformatted['org'].isin(df_integrations['org'].unique())

print("\t\ttraining full model")
train_X, test_X, train_y, test_y = train_test_split(df_reformatted.drop(['org', 'churned', 'reindex'], axis=1).fillna(0.0), df_reformatted[target_col], test_size=0.33)

rf = RandomForestClassifier(n_estimators=1000)
rf.fit(train_X, train_y)


print("-"*20)
print("predictions and building report")
print("-"*20)

print("\tfiltering to orgs with activity within the past 6 months")
target_active_orgs = df_orgs[df_orgs['status']=='active']['id'].tolist()

six_months_ago = datetime.date.today() - datetime.timedelta(6*365/12)
df_trans['date'] = pd.to_datetime(df_trans['date'])
df_trans_orgdate = df_trans[df_trans['date']>=pd.Timestamp(six_months_ago)][['date', 'org']]
df_trans_agg = df_trans_orgdate.groupby('org')['date'].count().reset_index()
# narrow org list to active orgs with more than 10 transactions in the last 6 months
target_active_orgs = df_trans_agg[(df_trans_agg['date']>=10)&(df_trans_agg['org'].isin(target_active_orgs))]['org'].tolist()

# filter to active orgs
try:
    df_priorpreds = get_dataframe_from_file("qgiv-stats-data", "preds.churn.csv")
    print("\t{} prior preds found".format(len(df_priorpreds)))
except:
    df_priorpreds = pd.DataFrame(columns=['org', 'date_predicted'])
    print("\tno prior preds found")
    
df_reformatted = df_reformatted[df_reformatted['org'].isin(target_active_orgs)]
ftrs = df_reformatted[(~df_reformatted['churned'])&(~df_reformatted['org'].isin(df_priorpreds['org'].tolist()))].drop(['churned', 'org', 'reindex'], axis=1).fillna(0.)

print("\tperform prediction")
y_pred = rf.predict_proba(ftrs)
y_pred_df = pd.DataFrame(y_pred)
y_pred_df['org'] = df_reformatted[~df_reformatted['churned']]['org']

print("\t\t{} unfiltered predicions".format(len(y_pred_df)))
top_preds = y_pred_df[~y_pred_df['org'].isin(df_priorpreds['org'].tolist())].sort_values(1, ascending=False).head(20).dropna()

predicted_orgs = top_preds['org'].tolist()

print("\t\tadd {} predictions to history".format(len(predicted_orgs)))
tdy = datetime.datetime.today()

y_preds_df = pd.DataFrame([{'org': o, 'date_predicted': tdy} for o in predicted_orgs])
df_priorpreds = df_priorpreds.append(y_preds_df, sort=True)
df_priorpreds['org'] = df_priorpreds['org'].astype(int)
save_dataframe_to_file("qgiv-stats-data", "preds.churn.csv", df_priorpreds)

print("Report:")
print("-"*40)

labels = []
for f in ftrs.columns:
    if 'month_0' in f:
        labels.append(f.replace('month_0_', ''))

for o in predicted_orgs:
    inp = df_reformatted[df_reformatted['org']==o]
    
    try:
        org_name = df_orgs[df_orgs['id']==int(o)]['org_name'].iloc[0]
    except:
        org_name = '(Not found)'
    
    print("{} ({})".format(org_name, int(o)))
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

