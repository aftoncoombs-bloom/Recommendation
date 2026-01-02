'''
Implementation/Adoption

we want to see if the client has engaged with the features. check form settings to see if settings have been changed/configured/enabled, etc.
'''
# global
1. select count(id) from Notification where (systemType=4 and systemId={form ID}) or (systemType=3 and systemId={org ID})  # custom notifications
2. select count(id) from ServiceIntegration where entityType=3 and entity={org ID}  # integrations
3. select count(id) from Report where entityType=3 and entity={org ID}  # custom reports
4. # admin accounts
5. select count(id) from Form_MerchantAccount where form={} group by paymentMethods  # payment gateways
6. select count(id) from Embed where entity={form ID} and entityType=4  # embed
7. select count(id) from TransPromise where form={}  # promise

# check year round settings
1. select count(id) from Restriction where form={}  # restrictions
2. select count(id) from Fields where form={}  # custom fields
3. select count(id) from Pledge where form={}  # pledges
4. select count(id) from Form where enableRecurring='y'  # recurring
5. select count(id) from Event where form={}  # events
6. select count(id) from Event where form={} and allowDonation=1  # event donations
7. select count(p.id) from PartInfo as p left join Event on p.event=e.id where e.form={}  # event fields
8. select count(id) from hn_PromoCode where entityType=4 and entity={}  # event promo
9. select count(id) from SMSShortCode where form={}  # sms/text to give
10. select count(id) from Form where org={} and enableDonorLogins=1  # donor logins
11. # donor login onetime
12. # donor login recurring
13. # donor login stored payment methods

# check p2p

''''
Bidirectional Adoption

we want to see if the donors have engaged with the features. check presence in transactions.
'''
# get source transactions
select count(id) from Transaction where form={} group by source

7. select count(distinct ga.id) from TransGiftAssist as ga left join Transaction as t on t.id=ga.transaction where t.form={}  # gift assist

# check year round settings
1. select count(distinct t.id) from Transaction as t left join TransDonation as td on td.transaction=t.id where td.restriction <> null and form={}  # restrictions
2. select count(distinct fld.id) from FieldData as fld left join Transaction as t on fld.transaction=t.id where fld.transEvent=0 and fld.transRegistration=0 and t.form={}  # fielddata
3. select coutn(distinct td.pledge) from TransDonation as td left join Transaction as t on t.id=td.transaction where td.pledge<>0 and t.form={}  # pledge
4. select count(id) from Transaction where recurring <> null and form={}  # recurring
5. select count(distinct te.transaction) from TransEvent as te left join Transaction as t on te.transaction=t.id where t.form={}  # events
6. select count(distinct td.id) from TransDonation as td left join Transaction as t left join td.transaction=t.id left join TransEvent as te on te.transaction=t.id where t.form={}  # event donation
7. select count(distinct pd.id) from PartData as pd  # event fielddata
8. select count(distinct p.id) from TransPromo as p left join TransEvent as te on te.id=p.entity left join Transaction as t on t.id=te.transaction where p.entityType=10  # event promo
9. 
10.
11.
12.
13.

# check p2p


'''
check percentage of transactions represented
'''
# get total transactions count for percentage
select count(id) from Transaction where form={}