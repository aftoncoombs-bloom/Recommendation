# SVM w/ Linear kernel

## MSE of 147.757754514

*Kernel:* linear

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
- opt_fields^2
- opt_fields^3
- opt_fields^4

*MSE:* 147.757754514

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.86246274

*Kernel:* linear

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
- month^2
- month^3
- month^4

*MSE:* 147.86246274

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863382369

*Kernel:* linear

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
- donation_active^2
- donation_active^3

*MSE:* 147.863382369

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863405867

*Kernel:* linear

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
- month_bckt_3
- month_bckt_5
- month_bckt_10

*MSE:* 147.863405867

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863492026

*Kernel:* linear

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
- donation_active^2

*MSE:* 147.863492026

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863554964

*Kernel:* linear

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
- donation_active^2
- donation_active^3
- donation_active^4
- donation_active^5

*MSE:* 147.863554964

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863564701

*Kernel:* linear

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
- permit_mobile^2
- permit_mobile^3
- permit_mobile^4
- permit_mobile^5

*MSE:* 147.863564701

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863595471

*Kernel:* linear

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
- restrictions_bckt_3
- restrictions_bckt_5

*MSE:* 147.863595471

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863604701

*Kernel:* linear

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
- req_fields^2
- req_fields^3

*MSE:* 147.863604701

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)

___

## MSE of 147.863611466

*Kernel:* linear

*Columns:*
- permit_other_amount+enable_donorlogins
- permit_other_amount+pledges_count
- enable_donorlogins
- permit_other_amount+amounts_system
- permit_other_amountXmultirestriction_system
- month
- permit_other_amountXpledges_count
- permit_other_amount+req_fields
- permit_mobile
- pledges_count
- permit_other_amountXrestrictions
- permit_anonymous
- pledge_active
- permit_other_amountXenable_donorlogins
- permit_other_amountXday
- permit_other_amount+permit_anonymous
- permit_other_amount+opt_fields
- permit_other_amountXreq_fields
- permit_other_amount+multirestriction_system
- permit_other_amount+month
- opt_fields
- permit_other_amountXopt_fields
- day
- permit_other_amountXpermit_anonymous
- restrictions
- permit_other_amount+day
- req_fields
- permit_other_amount+pledge_active
- amounts_system
- permit_other_amount+permit_mobile
- permit_other_amount+restrictions
- multirestriction_system
- permit_other_amountXamounts_system
- conversion

*MSE:* 147.863611466

*Model Object:* 
SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
  kernel='linear', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
