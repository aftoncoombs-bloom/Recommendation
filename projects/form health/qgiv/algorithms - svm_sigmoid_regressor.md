# SVM w/ Sigmoid kernel

## MSE of 52.9006766314

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- collect_captchaXopt_fields
- collect_captcha+opt_fields
- collect_captchaXreq_fields
- collect_captcha+req_fields
- collect_captchaXdonation_active
- collect_captcha+donation_active
- collect_captchaXamounts_system
- collect_captcha+amounts_system
- collect_captchaXmultirestriction_system
- collect_captcha+multirestriction_system
- collect_captchaXrestrictions
- collect_captcha+restrictions
- collect_captchaXpledges_count
- collect_captcha+pledges_count
- collect_captchaXpledge_active
- collect_captcha+pledge_active
- collect_captchaXpermit_anonymous
- collect_captcha+permit_anonymous
- collect_captchaXpermit_mobile
- collect_captcha+permit_mobile
- collect_captchaXpermit_other_amount
- collect_captcha+permit_other_amount
- collect_captchaXenable_donorlogins
- collect_captcha+enable_donorlogins
- collect_captchaXday
- collect_captcha+day
- collect_captchaXmonth
- collect_captcha+month

*MSE:* 52.9006766314

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 52.9078557067

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- amounts_systemXopt_fields
- amounts_system+opt_fields
- amounts_systemXreq_fields
- amounts_system+req_fields
- amounts_systemXdonation_active
- amounts_system+donation_active
- amounts_systemXmultirestriction_system
- amounts_system+multirestriction_system
- amounts_systemXrestrictions
- amounts_system+restrictions
- amounts_systemXpledges_count
- amounts_system+pledges_count
- amounts_systemXpledge_active
- amounts_system+pledge_active
- amounts_systemXpermit_anonymous
- amounts_system+permit_anonymous
- amounts_systemXpermit_mobile
- amounts_system+permit_mobile
- amounts_systemXpermit_other_amount
- amounts_system+permit_other_amount
- amounts_systemXenable_donorlogins
- amounts_system+enable_donorlogins
- amounts_systemXcollect_captcha
- amounts_system+collect_captcha
- amounts_systemXday
- amounts_system+day
- amounts_systemXmonth
- amounts_system+month

*MSE:* 52.9078557067

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.218206244

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- amounts_system^2
- amounts_system^3
- amounts_system^4
- amounts_system^5

*MSE:* 53.218206244

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.218206244

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- multirestriction_system^2
- multirestriction_system^3
- multirestriction_system^4
- multirestriction_system^5

*MSE:* 53.218206244

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.2378140359

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- permit_other_amount^2
- permit_other_amount^3
- permit_other_amount^4
- permit_other_amount^5

*MSE:* 53.2378140359

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.3797289234

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- permit_mobileXopt_fields
- permit_mobile+opt_fields
- permit_mobileXreq_fields
- permit_mobile+req_fields
- permit_mobileXdonation_active
- permit_mobile+donation_active
- permit_mobileXamounts_system
- permit_mobile+amounts_system
- permit_mobileXmultirestriction_system
- permit_mobile+multirestriction_system
- permit_mobileXrestrictions
- permit_mobile+restrictions
- permit_mobileXpledges_count
- permit_mobile+pledges_count
- permit_mobileXpledge_active
- permit_mobile+pledge_active
- permit_mobileXpermit_anonymous
- permit_mobile+permit_anonymous
- permit_mobileXpermit_other_amount
- permit_mobile+permit_other_amount
- permit_mobileXenable_donorlogins
- permit_mobile+enable_donorlogins
- permit_mobileXcollect_captcha
- permit_mobile+collect_captcha
- permit_mobileXday
- permit_mobile+day
- permit_mobileXmonth
- permit_mobile+month

*MSE:* 53.3797289234

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.4274793779

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- collect_captcha^2
- collect_captcha^3
- collect_captcha^4
- collect_captcha^5

*MSE:* 53.4274793779

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.463659398

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- permit_other_amount^2
- permit_other_amount^3

*MSE:* 53.463659398

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.4656164758

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- collect_captcha^2
- collect_captcha^3
- collect_captcha^4

*MSE:* 53.4656164758

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 53.4865514758

*Kernel:* sigmoid

*Columns:*
- opt_fields
- req_fields
- donation_active
- amounts_system
- multirestriction_system
- restrictions
- pledges_count
- pledge_active
- permit_anonymous
- permit_mobile
- permit_other_amount
- enable_donorlogins
- collect_captcha
- conversion
- day
- month
- permit_anonymousXopt_fields
- permit_anonymous+opt_fields
- permit_anonymousXreq_fields
- permit_anonymous+req_fields
- permit_anonymousXdonation_active
- permit_anonymous+donation_active
- permit_anonymousXamounts_system
- permit_anonymous+amounts_system
- permit_anonymousXmultirestriction_system
- permit_anonymous+multirestriction_system
- permit_anonymousXrestrictions
- permit_anonymous+restrictions
- permit_anonymousXpledges_count
- permit_anonymous+pledges_count
- permit_anonymousXpledge_active
- permit_anonymous+pledge_active
- permit_anonymousXpermit_mobile
- permit_anonymous+permit_mobile
- permit_anonymousXpermit_other_amount
- permit_anonymous+permit_other_amount
- permit_anonymousXenable_donorlogins
- permit_anonymous+enable_donorlogins
- permit_anonymousXcollect_captcha
- permit_anonymous+collect_captcha
- permit_anonymousXday
- permit_anonymous+day
- permit_anonymousXmonth
- permit_anonymous+month

*MSE:* 53.4865514758

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='sigmoid', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
