import pandas as pd


PATH_ORGFORMS = "org_forms.csv"
PATH_ORGSTARTS = "org_start_dates.csv"
PATH_ANALYTICS = "analytics/analytic_base.csv"


print("Cleanup on analytics")
print("\tloading analytics file")
df = pd.read_csv(PATH_ANALYTICS, low_memory=False)

print("\tclean up form & form type")
df['form'] = df['entity']
df.drop('entity', axis=1, inplace=True)

df['form_type'] = df['entityType']
df.drop('entityType', axis=1, inplace=True)

print("\torg ID setting")
form_orgs = pd.read_csv(PATH_ORGFORMS)
df['org'] = df['form'].apply(lambda x: form_orgs[form_orgs['form']==x]['org'].iloc[0] if len(form_orgs[form_orgs['form']==x]) > 0 else None)

print("\tstoring updates")
df.to_csv(PATH_ANALYTICS, index=False)
print("Done")
