Focusing on the donation conversion here in order to isolate donation form variables from registration in the focus of exploration.

_Ignoring the binary settings values here as they're dominated by class imbalance and/or primarily focused on registration actions rather than donations.__

# Correlations

|  feature   | correlation |
|------------|-------------|
| fields     | -0.028306   |
| req fields | -0.011564   |
| amounts    | -0.012636   |
| rest       |  0.002628   |

Nothing particularly strong here but worth noting that the restriction count is the only feature positively correlated to donation conversion. The fields and amounts would appear to decrease conversion with increase in value. This was also seen in the Qgiv data.

Value counts:

| value | req_fields | fields | amt_count |
|-------|------------|--------|-----------|
|   0   |   115691   |  94115 |     2311  |
|   1   |    73038   |  59935 |      453  |
|   2   |    29833   |  39650 |        6  |
|   3   |    17130   |  24811 |     8858  |
|   4   |    16330   |  13617 |   127571  |
|   5   |     3409   |  12575 |    70206  |
|   6   |     3498   |   6173 |    34186  |
|   7   |      196   |   1032 |    10965  |
|   8   |     4412   |   2475 |     5489  |
|   9   |      228   |   2778 |     1765  |
|   10  |     2402   |   2713 |     3701  |
|   11  |      859   |    787 |     1338  |
|   12  |        0   |   1914 |      851  |
|   13  |        0   |   3442 |        0  |
|   16  |        0   |    402 |        0  |
|   17  |     1070   |      0 |        0  |
|   21  |        0   |   1070 |        0  |
|   26  |        0   |      0 |      396  |
|   27  |        0   |    607 |        0  |

There is a notable peak in amount count at 4 amounts (default settings?) and for required fields at 0. Fields seems to be more evenly distributed, descending until it reached 8 fields which does seem like far too many for a reasonable user experience but we do not differentiate in the data between registration fields and donation fields, so I would assume the majority of these fields are for registrations where a greater tolerance of increased user input would be expected. This does complicate the findings for this endeavor.

# Modeling

## Random forest

Modeling with a simple random forest, averaging over 10 iterations, yields the following:

RF(100) w/ features: fields, req_fields, amt_count, rest_count
	MAE: 0.0168341722051
	MSE: 0.00259278782936
	R2: 0.031519321741
	Feature importances:
		fields: 0.246273920055
		req_fields: 0.171808131882
		amt_count: 0.575117898704
		rest_count: 0.00680004935796
        
RF(100) w/ features: fields, req_fields, amt_count
	MAE: 0.0168454516767
	MSE: 0.00231322526401
	R2: 0.0329237784036
	Feature importances:
		fields: 0.25655629023
		req_fields: 0.208124529214
		amt_count: 0.535319180556
        
The model appears resistant to feature engineering, tried exponential expansions on all fields, the differences were negligible. I take this as a good sign that the underlying relationship has been found and the algorithm is seeing through any efforts to exacerbate or enhance that relationship. Dropping __rest_count__ results in slightly better mse but worse $r^2$, mae shows no meaningful change. It is likely that the dominance of the amount count feature is due to the fact that registration and donation fields are lumped together here, and given multirestriction giving is not supported in P2P the amount count is the only feature here that is 100% reliable as a predictor lacking noise. It is impressive that the random forest with only 100 predictors would pick this up.

RF(250) w/ features: fields, req_fields, amt_count, rest_count
	MAE: 0.0168471709112
	MSE: 0.00307737077769
	R2: 0.0338701245984
	Feature importances:
		fields: 0.248923475007
		req_fields: 0.184764138706
		amt_count: 0.55925025065
		rest_count: 0.00706213563651
        
Increasing the number of trees to 250 seems to have actually hurt the metrics.


RF w/ features: fields, req_fields, amt_count, rest_count, cat_count, class_count
	MAE: 0.0150268149541
	MSE: 0.00263096717535
	R2: 0.069196291761
	Feature importances:
		fields: 0.11715661813
		req_fields: 0.0906079303341
		amt_count: 0.313795840797
		rest_count: 0.00570044304856
		cat_count: 0.213633482757
		class_count: 0.259105684934

While category and classification counts meaningfully contribute to the prediction, they don't appear to be helping the metrics at all.

## Linear regression

Modeling a linear regression, averaging over 10 iterations, yields the following:

LR w/ features: fields, req_fields, amt_count, rest_count
	MAE: 0.0184695418815
	MSE: 0.00323663117817
	R2: 0.00161589949338
	Feature importances:
		fields: -0.00118757296583
		req_fields: 0.00127150200287
		amt_count: -0.000547332324987
		rest_count: 0.000228639000712
        
We have a better $r^2$ here, but the mse & mae are slightly worse. What's more interesting is that amount count has been devalued significantly from it's prominent influence in the random forest model. Trying a bit of feature modeling resulted in similar outcomes to the random forest with negligible improvements, and in most cases appeared to hurt the model. I'm fairly certain the noise of the page views not intended for donations and failure to discriminate between registration and donation fields is throwing any potential linear relationship that could be found.

LR w/ features: fields, req_fields, amt_count
	MAE: 0.0184918155127
	MSE: 0.00355866424902
	R2: 0.00163261984474
	Feature importances:
		fields: -0.00122044437803
		req_fields: 0.00128121920847
		amt_count: -0.000526154944642
        
LR w/ features: fields, req_fields, rest_count
	MAE: 0.0184653058499
	MSE: 0.00247635205642
	R2: 0.00197965597344
	Feature importances:
		fields: -0.00116360432083
		req_fields: 0.00118494846372
		rest_count: -3.78406740828e-05
        
LR w/ features: fields, req_fields
	MAE: 0.0184260694621
	MSE: 0.00209342401328
	R2: 0.00205397039705
	Feature importances:
		fields: -0.00118656362259
		req_fields: 0.00119974393391
        
No other features should be relevant to donation conversion save for the CMS or social data which I have yet to get ahold of, and these models appear to be immune or repulsed by feature engineering. I think this is the end of the line until I can integrate some CMS or social data. That being said, the random forest model does appear to perform relatively well, and certainly much better than any model did with the full feature set ($r^2$: 0.098, mse: 0.003), and may be production-ready.