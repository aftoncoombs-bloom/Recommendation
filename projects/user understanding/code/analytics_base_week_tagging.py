import pandas as pd


PATH_ORGFORMS = "org_forms.csv"
PATH_ORGSTARTS = "org_start_dates.csv"
PATH_ANALYTICS = "analytics/analytic_base.csv"

print("Loading org start dates")
df_start_dates = pd.read_csv(PATH_ORGSTARTS)

print("Loading analytics for org start dates")
analytics_data = None
counter = 0
for chunk in pd.read_csv(PATH_ANALYTICS, low_memory=False, chunksize=100000):
    min_date = chunk['tm_stamp'].min()
    for _, r in df_start_dates[df_start_dates['week_52']>=min_date].iterrows():
        msk = (chunk['org']==r['org'])&(chunk['tm_stamp']>=r['start_date'])&(chunk['tm_stamp']<=r['week_52'])

        if analytics_data is None:
            analytics_data = chunk[msk]
        else:
            analytics_data = analytics_data.append(chunk[msk])
    
    counter += 1
    if counter > 0 and counter % 10 == 0:
        print("\tdone with {} chunks".format(counter))

analytics_data.to_csv("analytics_base_week_tags.csv", index=False)