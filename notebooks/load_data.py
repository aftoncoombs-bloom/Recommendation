import pandas as pd

analytic_base = pd.read_csv('~/Repositories/datasets/analytic_base.csv')
analytic_qgiv = pd.read_csv('~/Repositories/datasets/analytic_qgiv_stats.csv')

ab = analytic_base[['id', 'org', 'form', 'timestamp', 'visits', 'mobile_visits', 'don_form_trans_count', 'don_form_trans_vol']]
aq = analytic_qgiv[['id', 'base', 'org', 'total_visits', 'opt_fields', 'req_fields', 'donation_active', 'amounts_system', 'multirestriction_system', 'restrictions', 'pledges_count', 'pledge_active', 'permit_anonymous', 'permit_mobile', 'permit_other_amount', 'enable_donorlogins', 'collect_captcha']]
d = pd.merge(ab, aq, left_on="id", right_on="base")

# filter out not visited observations
df = d[d.visits > 0]
# add conversion
conversion = pd.DataFrame({'conversion':df["don_form_trans_count"]/df["total_visits"]*100})
# merge conversion w/ the rest of the data
df = pd.concat([df, conversion], axis=1)
# add day_of_month & month
date_data = pd.DataFrame({
        'day': pd.to_datetime(df.timestamp).apply(lambda x: x.day), 
        'month': pd.to_datetime(df.timestamp).apply(lambda x: x.month)})
# merge date data w/ the rest of the data
df = pd.concat([df, date_data], axis=1)

df.replace(np.NaN, 0, inplace=True)

# drop possibly misleading columns
df.drop('timestamp', axis=1, inplace=True)
df.drop('org_x', axis=1, inplace=True)
df.drop('form', axis=1, inplace=True)
df.drop('id_x', axis=1, inplace=True)
df.drop('visits', axis=1, inplace=True)
df.drop('mobile_visits', axis=1, inplace=True)
df.drop('don_form_trans_count', axis=1, inplace=True)
df.drop('don_form_trans_vol', axis=1, inplace=True)
df.drop('id_y', axis=1, inplace=True)
df.drop('base', axis=1, inplace=True)
df.drop('org_y', axis=1, inplace=True)
df.drop('total_vists', axis=1, inplace=True)
