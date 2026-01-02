# Neural Network

## MSE of 46.5578909833

*Architecture:* (20, 4)
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
- restrictions^2
- restrictions^3

*MSE:* 46.5578909833

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(20, 4), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 46.5842777004

*Architecture:* (20, 5)
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
- day^2
- day^3
- day^4

*MSE:* 46.5842777004

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(20, 5), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 46.7841122372

*Architecture:* (20, 5)
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
- day_bckt_3
- day_bckt_5
- day_bckt_10

*MSE:* 46.7841122372

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(20, 5), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 47.2981900702

*Architecture:* (20, 5)
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
- day^2
- day^3
- day^4
- day^5

*MSE:* 47.2981900702

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(20, 5), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 47.4146702722

*Architecture:* (30, 5)
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

*MSE:* 47.4146702722

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(30, 5), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 47.5116721631

*Architecture:* (20, 4)
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
- restrictions^2
- restrictions^3
- restrictions^4

*MSE:* 47.5116721631

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(20, 4), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 47.8370942731

*Architecture:* (10, 4)
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
- opt_fields_bckt_3
- opt_fields_bckt_5
- opt_fields_bckt_10

*MSE:* 47.8370942731

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(10, 4), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 47.9142432342

*Architecture:* (15, 3)
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

*MSE:* 47.9142432342

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(15, 3), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 48.027889992

*Architecture:* (15, 3)
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

*MSE:* 48.027889992

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(15, 3), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)

___

## MSE of 48.1041108999

*Architecture:* (20, 4)
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

*MSE:* 48.1041108999

*Model Object:* 
MLPRegressor(activation='relu', alpha=0.0001, batch_size='auto', beta_1=0.9,
       beta_2=0.999, early_stopping=False, epsilon=1e-08,
       hidden_layer_sizes=(20, 4), learning_rate='constant',
       learning_rate_init=0.001, max_iter=200, momentum=0.9,
       nesterovs_momentum=True, power_t=0.5, random_state=None,
       shuffle=True, solver='adam', tol=0.0001, validation_fraction=0.1,
       verbose=False, warm_start=False)
