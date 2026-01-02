# Project Log

I started out by gathering all analytics features and running them through a random forest.
Those details are logged in Phase 1.

## Phase 1

Training analytics data straight from the database.

Features include:

```
form_analytics = load_qgiv_analytics(
    base_columns=[
        'id', 'org', 'form', 'date', 'don_form_trans_count'
    ],
    qgiv_columns=[
        'pledges_count', 'events_count', 'events_priv_count', 'restrictions', 'amounts', 'ded_types', 'opt_ded_flds', 'req_ded_flds',
        'opt_fields', 'req_fields', 'pledge_active', 'donation_active', 'multirestriction_system','show_amount', 'permit_anonymous',
        'permit_recurring', 'permit_other_amount', 'permit_create_own_pledge', 'collect_company', 'collect_phone', 'collect_optin',
        'collect_captcha', 'collect_address_mobile', 'enable_donorlogins', 'enable_sms',
    ]
)
```

Pre processing is as follows:

```
def create_training_data(
    form_analytics: pd.DataFrame,
    y_column: str,
    drop_zero_target_rows: bool = False
):
    # Drop all of the rows that do not have a target value
    form_analytics.dropna(subset=[y_column])
    
    # Drop all rows where the target is zero, if True
    if drop_zero_target_rows:
        form_analytics = form_analytics.loc[form_analytics[y_column] > 0]

    # Get the target
    form_analytics_y = form_analytics[[y_column]]
    
    # Remove irrelevant features
    form_analytics_X = form_analytics.drop(['id', 'org', 'form', 'date', y_column], axis=1)

    return train_test_split(
        form_analytics_X,
        form_analytics_y,
        shuffle=False
    )

X_train, X_test, y_train, y_test = create_training_data(
    form_analytics=form_analytics,
    y_column='don_form_trans_count',
    drop_zero_target_rows=False
)
```

### Result

- Algorithm: RandomForestRegressor
- Target: 'don_form_trans_count'
- Samples: 25,009,082
- MSE: 0.8039766826236264

Feature Importances:

This kept killing the kernal after running so I still need to get the feature importances here.

## Phase 2

For speed of development as well as targeting only samples that are relevant, I am dropping all rows where the target variable is zero.

The code is the same as above except the `drop_zero_target_rows` is set to `True`.

### Result

Removing the rows with a zero target raises the MSE and reduces the number of samples, however is probably a better stating point.

- Algorithm: RandomForestRegressor
- Target: 'don_form_trans_count'
- Samples: 391635
- MSE: 17.72217295833897

Feature Importances
                          Importance
collect_address_mobile      0.251665
ded_types                   0.232826
permit_create_own_pledge    0.172287
events_count                0.074776
pledge_active               0.074431
collect_phone               0.069944
collect_company             0.030841
permit_anonymous            0.029448
amounts                     0.021478
restrictions                0.020119
enable_donorlogins          0.012965
enable_sms                  0.003979
req_fields                  0.002398
events_priv_count           0.000724
opt_fields                  0.000709
show_amount                 0.000505
permit_other_amount         0.000366
collect_optin               0.000204
donation_active             0.000152
pledges_count               0.000097
multirestriction_system     0.000054
req_ded_flds                0.000033
permit_recurring            0.000000
collect_captcha             0.000000
opt_ded_flds                0.000000

Based on this information, I removed all input features that have no
importance and found the MSE rose to 36.584075235063736

## Phase 3

I started adding features in an attempt capture the scale of a given organization.
Using transaction data I gathered the yearly volume and transaction counts for a given org and added those as 
features to the inputs. Those features turned out to be in the top third of importance scale and brought the MSE down 
to 13.917314428864882 with the following feature importances.

Feature Importances
                           Importance
pledge_active                0.746100
enable_donorlogins           0.144293
enable_sms                   0.052638
org_yearly_volume            0.045794
req_fields                   0.002078
org_yearly_donation_count    0.002071
restrictions                 0.002067
amounts                      0.001700
collect_phone                0.000765
events_count                 0.000678
show_amount                  0.000672
opt_fields                   0.000206
collect_address_mobile       0.000177
collect_optin                0.000122
ded_types                    0.000119
permit_create_own_pledge     0.000096
events_priv_count            0.000091
permit_anonymous             0.000088
collect_company              0.000078
donation_active              0.000073
permit_other_amount          0.000059
multirestriction_system      0.000017
req_ded_flds                 0.000011
pledges_count                0.000007

For completeness the function to calculate those is:

```
def engineer_features(
    transactions: pd.DataFrame,
    form_analytics: pd.DataFrame
) -> pd.DataFrame:
    
    # Add the orgs total yearly transaction volume to the dataframe
    total_donation_amounts = transactions.groupby('org').sum().reset_index()
    
    form_analytics['org_yearly_volume'] = form_analytics.apply(
        lambda row: total_donation_amounts.loc[total_donation_amounts['org'] == row['org']]['donations_amt'].values[0],
        axis=1
    )
    
    # Add the orgs total yearly transaction counts to the dataframe
    form_analytics['org_yearly_donation_count'] = form_analytics.apply(
        lambda row: total_donation_amounts.loc[total_donation_amounts['org'] == row['org']]['donations_count'].values[0],
        axis=1
    )
    
    return form_analytics
```

I added the average donation size as an input feature and while it did rank highly on the feature importance
list, it did not lower the mse by any significant amount, leaving it at 13.716276435993334 trained on 391,635 samples.

Feature Importances
                          Importance
pledge_active               0.754718
enable_donorlogins          0.136236
enable_sms                  0.053140
yearly_volume               0.042424
average_donation_size       0.003225

I normalized the org scale features with a `MinMaxScaler` after reading a post online that claimed it would help
and it did to a small degree to bring the mse to ~ 13.5.

I'm not sure what other features I can add for org scale at this point so I spent the rest of the day adjusting the settings on the random forest
and no matter what I tried I was only able to bring the mse down to the low 13s so I think it's time to give a new algorithm a shot.

I can feel you rolling your eyes, Jeremy, but i'm calling it now that a neural net is going to be the ticket. But that's for later.

# Support Vector Machine

After converging to a MSE of ~13 with RandomForestRegressors, I'm going to try the same with a SVR.

Turns out our dataset is much to big to train a standard SVR so to get a baseline I am trying a LinearSVR, however I do not think that
we can fit our data with a linear line so i'm not hopeful on the SVM algorithm.

# Gradient Boosting Regressor

Training a `GradientBoostingRegressor` with all of the inputs from the initial random foreset, as well as the org scale featrues gives a mse of 21.88.

To get a better mse I started adding more estimators and settled on 120 which has an mse of 17.00

Increasing the max depth to 5 loweres out mse to around the best I could get with the RandomForest