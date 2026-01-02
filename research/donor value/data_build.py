import pandas as pd
from datetime import datetime
import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *

print("{:%Y-%m-%d %H:%M}: loading transactions".format(datetime.now()))
q = "select * from transactions where status='A' and date >= '01-01-2017' order by date desc"
df = redshift_query_read(q)

print("Iterating through {:,} donors".format(len(df['email'].unique())))

donor_data = []
for donor in df['email'].unique().tolist():
    _df = df[df['email']==donor]
    donor_data.append({
        'donor': donor,
        'transactions': len(_df),
        'total_amount': _df['amount'].sum(),
        'avg_amount': _df['amount'].mean(),
        'donations_amt': _df['donations_amt'].sum(),
        'donations_count': _df['donations_count'].sum(),
        'purchases_amt': _df['purchases_amt'].sum(),
        'purchases_count': _df['purchases_quantity'].sum(),
        'events_amt': _df['events_amt'].sum(),
        'events_tickets': _df['events_tickets'].sum(),
        'registrations_amt': _df['registrations_amt'].sum(),
        'registrations_count': _df['registrations_count'].sum(),
        'smspledge_amt': _df['smspledge_amt'].sum(),
        'smspledge_count': _df['smspledge_amt'].sum(),
        'don_form_count': len(_df[_df['source']=='don_form']), 
        'don_form_amount': _df[_df['source']=='don_form']['amount'].sum(), 
        'vt_count': len(_df[_df['source']=='vt_count']), 
        'vt_amount': _df[_df['source']=='vt']['amount'].sum(),
        'p2p_count': len(_df[_df['source']=='p2p']), 
        'p2p_amount': _df[_df['source']=='p2p']['amount'].sum(),
        'kiosk_count': len(_df[_df['source']=='kiosk']), 
        'kiosk_amount': _df[_df['source']=='kiosk']['amount'].sum(),
        'mobile_count': len(_df[_df['source']=='mobile']), 
        'mobile_amount': _df[_df['source']=='mobile']['amount'].sum(),
        'sms_count': len(_df[_df['source']=='sms']), 
        'sms_amount': _df[_df['source']=='sms']['amount'].sum(),
        'mobilevt_count': len(_df[_df['source']=='don_form']),
        'mobilevt_amount': _df[_df['source']=='mobilevt']['amount'].sum(),
        'fb_count': len(_df[_df['source']=='fb']), 
        'fb_amount': _df[_df['source']=='fb']['amount'].sum(),
        'givi_count': len(_df[_df['source']=='givi']),
        'givi_amount': _df[_df['source']=='givi']['amount'].sum(),
        'recurring_total_transactions': len(_df[_df['recurring']!=0]),
        'recurring_total_amount': _df[_df['recurring']!=0]['amount'].sum(),
        'recurring': len(_df['recurring'].unique()),
        'recurring_amount': _df.groupby('recurring')['amount'].first().sum(),
        'first_transaction': _df['date'].min(),
        'last_transaction': _df['date'].max()
    })
    if len(donor_data) % 50000 == 0:
        print("{:%Y-%m-%d %H:%M}: done with {} donors".format(datetime.now(), len(donor_data)))
        save_dataframe_to_file("qgiv-stats-data", "donor.agg.csv", pd.DataFrame(donor_data))
        

save_dataframe_to_file("qgiv-stats-data", "donor.agg.csv", pd.Dataframe(donor_data))
print("done with all ({}) donors".format(len(donor_data)))