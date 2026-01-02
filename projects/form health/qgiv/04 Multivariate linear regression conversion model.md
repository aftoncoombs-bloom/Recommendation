Isolated models have proven to perform worse than multivariate models. For instance, the model

$\beta_0+\beta_1req\_fields + \beta_2req\_fields^2 + \beta_3req\_fields^3$

predicts with much less accuracy than a model that includes all relevant fields (_req_fields, opt_fields, req_fields+opt_fields, restrictions, restriction_v_amounts_, and complication variables). While all possible variations have not yet been tested, the models generally appears to perform better when bringing in multiple factors which rationally makes sense given there is no one feature that solely influences a donation decision. Thus we're moving forward with the fully involved multivariate regression approach.

- Attempted Lasso & GLM (w/ backward stepwise selection) with mixed results. Neither beat the multivariate generalized linear model by RSS or [Mean Variance Delta](quiver:///notes/5084E4F6-FD6C-452C-9C8D-5A19359C51D5), but did with select other methods of validation. By my estimation, the additional complication of implementing these do not justify to minor potential accuracy improvement they may provide.
- kNN failed to produce a valid fit, often failing to narrow ties altogether

## Considerations and Assumptions

**Page view counts are unreliable** but we're assuming that this impacts all organizations and forms equally, thus we still rely upon the conversion trends. However, given this we can not evaluate model fit by traditional measures since we ultimately do not use the predicted value, we use the predicted delta. What we are looking for here is an evaluation of a fit's variance from the mean to ensure that the trend of the prediction follows something predictable. 

The value of a prediction that will be used at this point is the _difference between the current predicted value and the predicted value after the proposed change has been made_. 

> For instance, a client starts to add a required field to their form. At some point in this process, the current configuration and the proposed configuration are used to predict their values and the difference between the two is presented to the user as an advisory notice.

___

## Model

According to p-value assessment, the following have been identified as important variables pertaining to predicting conversion rates in Qgiv forms:

1. opt_fields
2. req_fields
3. donation_active
4. multirestriction_system
5. restrictions
6. permit_other_amount
7. collect_captcha
8. day
9. month
10. restrictionsXmultirestriction
11. $restrictions^2$
12. $restrictions^2Xmultirestriction$
13. $restrictions^3$
14. $restrictions^3Xmultirestriction$
15. $opt\_fields^2$
16. $opt\_fields^3$
17. $req\_fields^2$
18. $req\_fields^3$
19. fields
20. $fields^2$
21. $fields^3$

$y = \beta_0 + \beta_1opt\_fields + \beta_2req\_fields + \beta_3donation\_active + \beta_4multirestriction\_system + \beta_5restrictions + \beta_6collect\_captcha + \beta_7day + \beta_8month + \beta_9restrictionsXmultirestriction + \beta_{10}restrictions^2 + \beta_{11}restrictions^2Xmultirestriction + \beta_{12}restrictions^3 + \beta_{13}restrictions^3Xmultirestriction + \beta_{14}opt\_fields^2 + \beta_{15}opt\_fields^3 + \beta_{16}req\_fields^2 + \beta_{17}req\_fields^3 + \beta_{18}fields + \beta_{19}fields^2 + \beta_{20}fields^3 + \epsilon$

### ANOVA on Fit

Analysis of Deviance Table

Model: gaussian, link: identity

Response: conversion

Terms added sequentially (first to last)

| Df                          | Deviance |   Resid. | Df Resid. | Dev      |
| --------------------------- |:--------:| --------:| --------: | -------: |
| NULL                        |          |          |   45540   | 43748187 |
| restrictions                |    1     |    5749  |   45539   | 43742438 |
| opt_fields                  |    1     |    5958  |   45538   | 43736480 |
| req_fields                  |    1     |     603  |   45537   | 43735876 |
| donation_active             |    1     |  84496   |   45536   | 43651380 |
| multirestriction_system     |    0     |    0     |   45536   | 43651380 |
| collect_captcha             |    0     |    0     |   45536   | 43651380 |
| day                         |    1     |   16608  |   45535   | 43634772 |
| month                       |    1     |   5845   |   45534   | 43628927 |
| restrictionsXmultirestriction |   0    |    0     |   45534   | 43628927 |
| restrictions2               |    1     |   93033  |   45533   | 43535894 |
| restrictions2Xmultirestriction |  0    |     0    |   45533   | 43535894 |
| restrictions3               |    1     |   12868  |   45532   | 43523026 |
| restrictions3Xmultirestriction | 0     |    0     |   45532   | 43523026 |
| opt_fields2                 |    1     |  111772  |   45531   | 43411255 |
| req_fields2                 |    1     |   4466   |   45530   | 43406789 |
| fields                      |    0     |    0     |   45530   | 43406789 |
| fields2                     |    1     |   2667   |   45529   | 43404122 |
| req_fields3                 |    1     |    51    |   45528   | 43404072 |
| fields3                     |    1     |  116189  |   45527   | 43287883 |

___

## Data set
### Adjustments

1. _Removed_ top 50 visited entries
2. _Removed_ top 50 transaction count entries
3. _Removed_ entries with 0 visits
4. _Removed_ top 40 conversion rate entries

### Exploration - aggregated data set, limited to Qgiv forms

1. Mean visits: 427.308
2. Mean transaction count: 58.341
3. Mean amounts system active: 0.947
4. Mean conversion: 10.4%

### Exploration - Non-aggregated data set

1. Mean visits: 5.34
2. Mean transaction count: 0.646
3. Mean amounts system active: 0.947
4. Mean conversion: 13.7%

| System           | Transaction Count | Conversion rate | Visits  |
| ---------------- |:-----------------:| ---------------:| ------: |
| Hobnob           | 111721            |  11.59%         | 1529543 |
| Multirestriction | 13608             |  15.14%         | 81403   |
| Amounts          | 242435            |  15.01%         | 1430386 |

___

# Visualizations
![1 conv v rest.png](resources/E6AE5F5AD938212338FD5DAD40CAE41C.png)

![2 conv v reqfields.png](resources/DBF7D308F5D70E5E0718724ABC00AE9F.png)

___

# Adapted R modeling

```{r}
# train model
mv.fit.1 = glm(conversion ~ opt_fields + req_fields + donation_active + multirestriction_system + restrictions + day + month + I(restrictions * multirestriction_system) + I(restrictions^2) + I(restrictions^2 * multirestriction_system) + I(restrictions^3 * multirestriction_system) + I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + I(opt_fields + req_fields) + I((opt_fields + req_fields)^2) + I((opt_fields + req_fields)^3), data=analytic_data)

mv.fit.2 = glm(conversion ~ opt_fields + req_fields + donation_active + multirestriction_system + restrictions + day + month + I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + I(opt_fields + req_fields) + I((opt_fields + req_fields)^2) + I((opt_fields + req_fields)^3), data=analytic_data)

mv.fit.3 = glm(conversion ~ opt_fields + req_fields + restrictions + day + month + I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3), data=analytic_data)

mv.fit.4 = glm(conversion ~ req_fields + I(req_fields^2) + I(req_fields^3), data=analytic_data)

# predictions & mean calculation
pred.1 = lapply(c(0:20), FUN=function(x){
  analytic_data[1226,]$req_fields = x
  predict(mv.fit.1, analytic_data[1226,])
})
pred.2 = lapply(c(0:20), FUN=function(x){
  analytic_data[1226,]$req_fields = x
  predict(mv.fit.2, analytic_data[1226,])
})
pred.3 = lapply(c(0:20), FUN=function(x){
  analytic_data[1226,]$req_fields = x
  predict(mv.fit.3, analytic_data[1226,])
})
pred.4 = lapply(c(0:20), FUN=function(x){
  analytic_data[1226,]$req_fields = x
  predict(mv.fit.4, analytic_data[1226,])
})
means = lapply(c(0:20), FUN=function(x){
  mean(analytic_data[analytic_data$req_fields==x,]$conversion)
})

# visualization
plot(analytic_data$req_fields, analytic_data$conversion, cex=0.3, col="coral3", ylim=c(0,10), xlim=c(0,23))
lines(x=c(0:20), y=pred.1, col="green")
lines(x=c(0:20), y=pred.2, col="darkgreen")
lines(x=c(0:20), y=pred.3, col="aquamarine4")
lines(x=c(0:20), y=pred.3, col="bisque3")
lines(x=c(0:20), y=means, col="blue")
```

![Conversion v req_fields.jpeg](resources/E78EBFBA30DA5BE94B68984ECB52C34E.jpg)

zooming in

![conversion v req_fields zoom.jpeg](resources/ED54383C97501B314A74A60113CF3E03.jpg)

___

## Another required fields prediction example with full complexity model

```{r}
analytic_data[c("id", "timestamp", "org.x", "id", "form", "org.y", "visits", "amounts", "mobile_visits", "don_form_trans_count", "mobile_trans_count", "don_form_trans_vol", "mobile_trans_vol", "one_time_trans_count", "one_time_trans_vol", "total_visits")] = NULL
analytic_data$fields3 = analytic_data$fields^3

mltv.fit = fit.linear_model(analytic_data, "conversion")

# take a look at our example
analytic_data[210,]

# run predictions
mltv.fit.preds.1 = lapply(c(0:20), FUN=function(x){
  analytic_data[210,]$req_fields = x
  analytic_data[210,]$req_fields2 = x^2
  analytic_data[210,]$req_fields3 = x^3
  analytic_data[210,]$fields = x + analytic_data[210,]$opt_fields
  analytic_data[210,]$fields2 = analytic_data[210,]$fields^2
  analytic_data[210,]$fields3 = analytic_data[210,]$fields^3
  predict(mltv.fit[2][[1]], analytic_data[210,])
})
mltv.fit.preds.2 = lapply(c(0:20), FUN=function(x){
  analytic_data[1226,]$req_fields = x
  analytic_data[1226,]$req_fields2 = x^2
  analytic_data[1226,]$req_fields3 = x^3
  analytic_data[1226,]$fields = x + analytic_data[1226,]$opt_fields
  analytic_data[1226,]$fields2 = analytic_data[1226,]$fields^2
  analytic_data[1226,]$fields3 = analytic_data[1226,]$fields^3
  predict(mltv.fit[2][[1]], analytic_data[1226,])
})
mltv.fit.preds.3 = lapply(c(0:20), FUN=function(x){
  analytic_data[19912,]$req_fields = x
  analytic_data[19912,]$req_fields2 = x^2
  analytic_data[19912,]$req_fields3 = x^3
  analytic_data[19912,]$fields = x + analytic_data[19912,]$opt_fields
  analytic_data[19912,]$fields2 = analytic_data[19912,]$fields^2
  analytic_data[19912,]$fields3 = analytic_data[19912,]$fields^3
  predict(mltv.fit[2][[1]], analytic_data[19912,])
})
agg.conv = aggregate(test_data, by=list(test_data$req_fields), FUN=mean, na.rm=TRUE)

# visualize
plot(analytic_data$req_fields, analytic_data$conversion, cex=.5, col="red", xlim=c(0, 12), ylim=c(0,5))
lines(c(0:20), mltv.fit.preds.1, col="black")
lines(c(0:20), mltv.fit.preds.2, col="green")
lines(c(0:20), mltv.fit.preds.3, col="bisque3")
lines(x=agg.conv$Group.1, y=agg.conv$conversion, col="blue")
```

_Data pruning for outliers was not done on this data set_

![anthr-pred-ex.jpeg](resources/5332112A7603962FAF23F86BF5537292.jpg)

Here we're seeing a pretty good fit to the mean conversion rate by MVD for the fully articulated model.

___

## Full model with restrictions v conversion

_Depends upon the above prep code_. To fit this model, we remove the entries with restrictions > 26. This was an outlieing organization using the multirestriction system in a very niche way resulting in extremely high restriction counts & conversion rate. _See Python notebook_:

- org: 29705, form: 94263
- org: 911, form: 894

```{r}
mrest_data = analytic_data[analytic_data$multirestriction_system==1,]
mrest_data = mrest_data[mrest_data$restrictions<26,]
mltv.fit = fit.linear_model(mrest_data, "conversion")

# run predictions
mltv.fit.preds.1 = lapply(c(0:20), FUN=function(x){
  analytic_data[208,]$restrictions = x
  analytic_data[208,]$restrictions2 = x^2
  analytic_data[208,]$restrictions3 = x^3
  analytic_data[208,]$multirestriction = 1
  analytic_data[208,]$restrictionsXmultirestriction = x
  analytic_data[208,]$restrictions2Xmultirestriction = x^2
  analytic_data[208,]$restrictions3Xmultirestriction = x^3
  predict(mltv.fit[2][[1]], analytic_data[208,])
})
mltv.fit.preds.2 = lapply(c(0:20), FUN=function(x){
  analytic_data[2228,]$restrictions = x
  analytic_data[2228,]$restrictions2 = x^2
  analytic_data[2228,]$restrictions3 = x^3
  analytic_data[2228,]$multirestriction = 1
  analytic_data[2228,]$restrictionsXmultirestriction = x
  analytic_data[2228,]$restrictions2Xmultirestriction = x^2
  analytic_data[2228,]$restrictions3Xmultirestriction = x^3
  predict(mltv.fit[2][[1]], analytic_data[2228,])
})
mltv.fit.preds.3 = lapply(c(0:20), FUN=function(x){
  analytic_data[25068,]$restrictions = x
  analytic_data[25068,]$restrictions2 = x^2
  analytic_data[25068,]$restrictions3 = x^3
  analytic_data[25068,]$multirestriction = 1
  analytic_data[25068,]$restrictionsXmultirestriction = x
  analytic_data[25068,]$restrictions2Xmultirestriction = x^2
  analytic_data[25068,]$restrictions3Xmultirestriction = x^3
  predict(mltv.fit[2][[1]], analytic_data[25068,])
})
agg.conv = aggregate(mrest_data, by=list(mrest_data$restrictions), FUN=mean, na.rm=TRUE)

# visualize
plot(mrest_data$restrictions, mrest_data$conversion, cex=.5, col="red", xlim=c(0, 25), ylim=c(0,50))
lines(x=agg.conv$Group.1, y=agg.conv$conversion, col="blue")
lines(c(0:25), mltv.fit.preds.1, col="black")
lines(c(0:25), mltv.fit.preds.2, col="green")
lines(c(0:25), mltv.fit.preds.3, col="bisque3")
```

![rest-v-conversion.jpeg](resources/E2EB552E25AE16BBB627B637D68DE570.jpg)









