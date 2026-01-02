# Data Exploration

Not seeing any strong relationships here, and what does appear present isn't sufficiently strong to build a meaningful model. Additional testing looking for nonlinear relationships in some ensemble algorithms revealed no features of great importance contributing to the model or predominantly explaining variance.

Not much to go on here. Assuming the contributing factors are going to be in the individual outreach and creating a compelling story on the part of the event (participants recruiting, social media posts, perhaps something in the CMS data revealing customization).

## Modeling

For each page view, we cannot distinguish between those already registered, those visiting for the purposes of seeing the event, donating to the event, registering for the event, etc. This inability to discern the intention of the user makes a fairly high degree of variance unavoidable when modeling against conversion calculations.

After evaluating and testing numerous algorithms, __Random Forest__ continues to be my friend in our nonlinear relationships. It performs much better than any other algorithm attempted, ranging from simple regressions to much more avanced ensemble models. This held true across all metrics and with relatively simple forests of only 100 predictors.

### Registration Conversion

Here we see some dominance in class, category, promo, and teams count. That being said, the prediction performance is still pretty bad considering variance explained, r^2, and MSE. 

Metrics

|                   |                   |
|-------------------|-------------------|
|MSE                | 2.00519151437     |
|Explained variance | 0.000853461869605 |
|R^2                | 0.000833919446057 |

Feature importances

| Feature                 | Importance        |
|-------------------------|-------------------|
| class_count             | 0.175738004739    |
| cat_count               | 0.161261378846    |
| promo_count             | 0.161510568316    |
| rest_count              | 0.0118656674375   |
| fields                  | 0.0969075601821   |
| opt_fields              | 0.0403493466081   |
| req_fields              | 0.0471703863334   |
| allows_reg_ind          | 0.0290808182716   |
| allows_teams            | 0.0108356534603   |
| allows_reg_team_create  | 0.00889787591117  |
| allows_reg_team_join    | 0.0105201364162   |
| allows_opt_reg_donation | 0.030901570135    |
| allows_sub_reg          | 1.4627277453e-06  |
| allows_sub_reg_pfp      | 0.000872150081081 |
| share_home              | 0.0               |
| share_pfp               | 0.0               |
| share_tfp               | 0.0               |
| share_therm             | 0.0               |
| share_donation          | 0.0               |
| allows_social           | 0.00101219520463  |
| teams_count             | 0.21307522533     |

### Donation Count

Here our model performs much better than in registration conversion context but still not happy with the divergence in appearances between the metrics. The MSE looks very good but the $r^2$ and variance explained leave something to be desired.

Metrics

|                    |                  |
|--------------------|------------------|
| MSE                | 0.00254415163591 |
| R2                 | 0.104942330635   |
| Variance explained | 0.104953492146   |

Feature importances

| Feature                 | Importance       |
|-------------------------|------------------|
| class_count             | 0.118080925534   |
| cat_count               | 0.140647272241   |
| promo_count             | 0.109648103475   |
| rest_count              | 0.00124637462527 |
| amt_count               | 0.159619533514   |
| ded_count               | 0.109381327156   |
| fields                  | 0.0515753599736  |
| opt_fields              | 0.0407697301778  |
| req_fields              | 0.0447353380059  |
| allows_reg_ind          | 0.0480758220137  |
| allows_teams            | 0.0534776968697  |
| allows_reg_team_create  | 0.0312583134363  |
| allows_reg_team_join    | 0.0252391102413  |
| allows_opt_reg_donation | 0.0406567620914  |
| allows_pfp_off_don      | 0.0126035608733  |
| allows_tfp_off_don      | 0.0129847697716  |

## Correlations

| Feature                 | Registration Count | Registration Amount |
|-------------------------|--------------------|---------------------|
| sic                     | 0.000565           | -0.002989           |
| visits                  | -0.001713          | -0.002171           |
| class_count             | -0.001805          | -0.002278           |
| cat_count               | 0.002151           | 0.007043            |
| promo_count             | 0.000829           | 0.001696            |
| rest_count              | -0.000215          | -0.000508           |
| amt_count               | -0.001331          | 0.003110            |
| ded_count               | -0.003703          | -0.002439           |
| fields                  | -0.000994          | 0.002158            |
| opt_fields              | -0.001641          | 0.000552            |
| req_fields              | -0.000148          | 0.002712            |
| allows_reg_ind          | -0.007470          | -0.002266           |
| allows_teams            | -0.002488          | -0.000106           |
| allows_reg_team_create  | -0.002684          | -0.000979           |
| allows_reg_team_join    | -0.001748          | -0.000532           |
| allows_opt_reg_donation | -0.000982          | -0.002581           |
| allows_sub_reg_pfp      | 0.002518           | 0.006545            |
| allows_pfp_off_don      | -0.001836          | -0.000329           |
| allows_tfp_off_don      | -0.001836          | -0.000329           |
| sponsors_count          | 0.002183           | 0.000231            |
| inappr_content          | 0.001106           | 0.000722            |
| non_fund_reg            | -0.002101          | -0.002247           |
| sub_reg_count           | 0.005318           | 0.000278            |
| teams_count             | -0.001306          | -0.000662           |

## Visualizations

![form_health_p2p_allows_sub_reg_pfp.png](../../resources/form_health_p2p_allows_sub_reg_pfp.png)
![form_health_p2p_allows_reg_ind.png](../../resources/form_health_p2p_allows_reg_ind.png)
![form_health_p2p_allows_teams.png](../../resources/form_health_p2p_allows_teams.png)
![form_health_p2p_non_fund_reg.png](../../resources/form_health_p2p_non_fund_reg.png)
![form_health_p2p_allows_reg_team_create.png](../../resources/form_health_p2p_allows_reg_team_create.png)
![form_health_p2p_allows_opt_reg_donation.png](../../resources/form_health_p2p_allows_opt_reg_donation.png)
![form_health_p2p_teams_count.png](../../resources/form_health_p2p_teams_count.png)
![form_health_p2p_allows_tfp_off_don.png](../../resources/form_health_p2p_allows_tfp_off_don.png)
![form_health_p2p_fields_count.png](../../resources/form_health_p2p_fields_count.png)
![form_health_p2p_allows_pfp_off_don.png](../../resources/form_health_p2p_allows_pfp_off_don.png)
![form_health_p2p_inappr_content.png](../../resources/form_health_p2p_inappr_content.png)
![form_health_p2p_allows_reg_team_join.png](../../resources/form_health_p2p_allows_reg_team_join.png)
![form_health_p2p_amt_count.png](../../resources/form_health_p2p_amt_count.png)
![form_health_p2p_ded_count.png](../../resources/form_health_p2p_ded_count.png)
![form_health_p2p_req_fields_count.png](../../resources/form_health_p2p_req_fields_count.png)
![form_health_p2p_sponsors_count.png](../../resources/form_health_p2p_sponsors_count.png)
![form_health_p2p_opt_fields_count.png](../../resources/form_health_p2p_opt_fields_count.png)
![form_health_p2p_sub_reg_count.png](../../resources/form_health_p2p_sub_reg_count.png)
![form_health_p2p_rest_count.jpg](../../resources/form_health_p2p_rest_count.jpg)

## General Notes

It is worth noting that some features were consistent across so many forms that they are virtually meaningless in signal quality. The event settings (binary flag values) showed a high degree of similarity between all observations and should probably not be used in any model. Ie, fewer than 20 observations had a value of 0 for allows social thus making this feature pointless to include in the model.