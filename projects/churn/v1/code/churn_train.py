import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from churn_support import *


print("reading in data")
df_logs = pd.read_csv(PATH_LOGS, low_memory=False)
df_integrations = pd.read_csv(PATH_INTEGRATIONS)
df_trans = pd.read_csv(TRANS_PATH, low_memory=False)

print("prep features")
print("\tupdate churned orgs")
df_orgs = pd.read_csv(PATH_ORGS)
df_churned_orgs = df_orgs[~df_orgs['date_closed'].isnull()]
df_churned_orgs.to_csv(PATH_CHURNED_ORGS, index=False)

print("\tgetting P2P org list from transaction history")
p2p_orgs = df_trans[df_trans.source=='p2p']['org'].unique().tolist()

print("\tfiltering orgs with fewer than 100 transactions")
orgs_trans_counts = df_trans.groupby('org')['id'].count().reset_index()
orgs_never_viable = orgs_trans_counts[orgs_trans_counts['id']<100]['org'].tolist()

print("\tprepping logs")

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

print("\tprepping integrations data")
print("\t\tmap the org name's to ID's")
df_integrations['id'] = df_integrations['Org'].apply(get_org_id_for_name)
df_integrations['close_date'] = df_integrations['id'].apply(get_org_close_date)

print("\tcompiling integrations with logs")
df_agged['integrations'] = df_agged['org'].isin(df_integrations['id'].unique())

print("train models")
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
df_reformatted['integrations'] = df_reformatted['org'].isin(df_integrations['id'].unique())

print("\t\tstore reformatted training data to CSV for reuse")
df_reformatted.to_csv(PATH_FTRS, index=False)

print("\t\ttraining full model")
train_X, test_X, train_y, test_y = train_test_split(df_reformatted.drop(['org', 'churned', 'reindex'], axis=1).fillna(0.0), df_reformatted[target_col], test_size=0.33)

rf = RandomForestClassifier(n_estimators=1000)
rf.fit(train_X, train_y)

print("\t\tstore model")
joblib.dump(rf, PATH_MDL)

print("DONE")
print("artifacts")
print("\t- {}".format(PATH_FTRS))
print("\t- {}".format(PATH_MDL))