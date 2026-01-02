# Data prep

```{r}
source("~/Repositories/Recommendation/notebooks/conversion-load-n-cleanup.R")
summary(analytic_data$avg_vol)

Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
    0.0    50.0   100.0   236.4   216.9 30000.0  576883 
```

___

# Restrictions

> Hypthesis: The number of restrictions is positively correlated to transaction volume to a point by motivating greater amounts when the donor feels like they have some control over how their gift is used.

We're going to test this by attempting to fit a regression of restrictions to the average transaction volume.

```{r}
plot(analytic_data$restrictions, analytic_data$avg_vol, cex=0.5, col="red")
```

![rest-avg_vol.jpeg](resources/1F2E233EAD782D55EC856D25422F4BA6.jpg)

```{r}
fit.all = glm(avg_vol ~ opt_fields + req_fields + donation_active + multirestriction_system + restrictions + collect_captcha + day + month + I(restrictions*multirestriction_system) + I(restrictions^2) + I(restrictions^2*multirestriction_system) + I(restrictions^3) + I(restrictions^3*multirestriction_system) + I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + I(req_fields+opt_fields) + I((req_fields+opt_fields)^2) + I((req_fields+opt_fields)^3), data=analytic_data)
summary(fit.all)

Call:
glm(formula = avg_vol ~ opt_fields + req_fields + donation_active + 
    multirestriction_system + restrictions + collect_captcha + 
    day + month + I(restrictions * multirestriction_system) + 
    I(restrictions^2) + I(restrictions^2 * multirestriction_system) + 
    I(restrictions^3) + I(restrictions^3 * multirestriction_system) + 
    I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + 
    I(req_fields + opt_fields) + I((req_fields + opt_fields)^2) + 
    I((req_fields + opt_fields)^3), data = analytic_data)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
 -679.4   -185.9   -128.4    -13.1  29727.8  

Coefficients: (2 not defined because of singularities)
                                              Estimate Std. Error t value Pr(>|t|)    
(Intercept)                                  1.539e+02  2.214e+02   0.695 0.486826    
opt_fields                                   3.914e+01  6.925e+00   5.653 1.59e-08 ***
req_fields                                   7.502e+01  2.019e+01   3.715 0.000204 ***
donation_active                              6.673e+00  2.208e+02   0.030 0.975892    
multirestriction_system                     -4.187e+01  3.073e+01  -1.362 0.173093    
restrictions                                 1.893e-01  8.068e-01   0.235 0.814506    
collect_captcha                                     NA         NA      NA       NA    
day                                          8.866e-01  4.159e-01   2.132 0.033040 *  
month                                        5.442e+00  2.356e+00   2.310 0.020913 *  
I(restrictions * multirestriction_system)    1.192e+01  8.081e+00   1.475 0.140116    
I(restrictions^2)                           -4.029e-03  6.985e-03  -0.577 0.564057    
I(restrictions^2 * multirestriction_system) -5.900e-01  5.533e-01  -1.066 0.286245    
I(restrictions^3)                            8.518e-06  1.405e-05   0.606 0.544456    
I(restrictions^3 * multirestriction_system)  1.069e-02  1.066e-02   1.002 0.316145    
I(opt_fields^2)                              3.289e+01  4.052e+00   8.117 4.94e-16 ***
I(opt_fields^3)                             -1.860e+00  2.175e-01  -8.553  < 2e-16 ***
I(req_fields^2)                              3.787e+01  1.054e+01   3.594 0.000326 ***
I(req_fields^3)                             -3.074e+00  1.081e+00  -2.843 0.004470 ** 
I(req_fields + opt_fields)                          NA         NA      NA       NA    
I((req_fields + opt_fields)^2)              -3.996e+01  3.942e+00 -10.137  < 2e-16 ***
I((req_fields + opt_fields)^3)               2.192e+00  2.194e-01   9.991  < 2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for gaussian family taken to be 438542)

    Null deviance: 1.3517e+10  on 30643  degrees of freedom
Residual deviance: 1.3430e+10  on 30625  degrees of freedom
  (576883 observations deleted due to missingness)
AIC: 485088

Number of Fisher Scoring iterations: 2
```

insignificant terms appear to be collect_captcha, donation_active; restrictions p-val broke 80% so adding bases functions for that

```{r}
fit.all = glm(avg_vol ~ opt_fields + req_fields + multirestriction_system + restrictions + I(restrictions^2) + I(restrictions^3) + I(restrictions^4) + day + month + I(restrictions*multirestriction_system) + I(restrictions^2) + I(restrictions^2*multirestriction_system) + I(restrictions^3) + I(restrictions^3*multirestriction_system) + I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + I(req_fields+opt_fields) + I((req_fields+opt_fields)^2) + I((req_fields+opt_fields)^3), data=analytic_data)
summary(fit.all)

Call:
glm(formula = avg_vol ~ opt_fields + req_fields + multirestriction_system + 
    restrictions + I(restrictions^2) + I(restrictions^3) + I(restrictions^4) + 
    day + month + I(restrictions * multirestriction_system) + 
    I(restrictions^2) + I(restrictions^2 * multirestriction_system) + 
    I(restrictions^3) + I(restrictions^3 * multirestriction_system) + 
    I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + 
    I(req_fields + opt_fields) + I((req_fields + opt_fields)^2) + 
    I((req_fields + opt_fields)^3), data = analytic_data)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
 -688.0   -185.9   -128.6    -12.7  29730.2  

Coefficients: (1 not defined because of singularities)
                                              Estimate Std. Error t value Pr(>|t|)    
(Intercept)                                  1.619e+02  1.801e+01   8.990  < 2e-16 ***
opt_fields                                   3.903e+01  6.927e+00   5.635 1.77e-08 ***
req_fields                                   7.488e+01  2.020e+01   3.708 0.000210 ***
multirestriction_system                     -4.319e+01  3.082e+01  -1.401 0.161095    
restrictions                                -3.056e-01  1.169e+00  -0.261 0.793774    
I(restrictions^2)                            1.273e-02  2.947e-02   0.432 0.665785    
I(restrictions^3)                           -8.409e-05  1.588e-04  -0.529 0.596506    
I(restrictions^4)                            1.353e-07  2.311e-07   0.585 0.558293    
day                                          8.889e-01  4.159e-01   2.137 0.032599 *  
month                                        5.472e+00  2.357e+00   2.322 0.020242 *  
I(restrictions * multirestriction_system)    1.239e+01  8.119e+00   1.526 0.127125    
I(restrictions^2 * multirestriction_system) -6.046e-01  5.538e-01  -1.092 0.274999    
I(restrictions^3 * multirestriction_system)  1.074e-02  1.066e-02   1.007 0.313912    
I(opt_fields^2)                              3.282e+01  4.054e+00   8.094 5.99e-16 ***
I(opt_fields^3)                             -1.842e+00  2.198e-01  -8.379  < 2e-16 ***
I(req_fields^2)                              3.760e+01  1.055e+01   3.566 0.000364 ***
I(req_fields^3)                             -3.023e+00  1.085e+00  -2.787 0.005330 ** 
I(req_fields + opt_fields)                          NA         NA      NA       NA    
I((req_fields + opt_fields)^2)              -3.985e+01  3.947e+00 -10.096  < 2e-16 ***
I((req_fields + opt_fields)^3)               2.172e+00  2.221e-01   9.779  < 2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for gaussian family taken to be 438537.1)

    Null deviance: 1.3517e+10  on 30643  degrees of freedom
Residual deviance: 1.3430e+10  on 30625  degrees of freedom
  (576883 observations deleted due to missingness)
AIC: 485087

Number of Fisher Scoring iterations: 2

```

p-val on restrictions based features is slowly decreasing at higher degrees but clearly not a significant term without invalid manipulation (ie, higher order degrees, probably overfitting)

restrictionsXmultirestriction seems more legit... 12%, increasing with degrees

```{r}
fit.isolated = glm(avg_vol ~ multirestriction_system + restrictions + I(restrictions^2) + I(restrictions^3) + I(restrictions^4) + day + month + I(restrictions*multirestriction_system) + I(restrictions^2*multirestriction_system) + I(restrictions^3*multirestriction_system), data=analytic_data)
summary(fit.isolated)

Call:
glm(formula = avg_vol ~ multirestriction_system + restrictions + 
    I(restrictions^2) + I(restrictions^3) + I(restrictions^4) + 
    day + month + I(restrictions * multirestriction_system) + 
    I(restrictions^2 * multirestriction_system) + I(restrictions^3 * 
    multirestriction_system), data = analytic_data)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
 -445.1   -190.0   -136.5    -21.3  29769.1  

Coefficients:
                                              Estimate Std. Error t value Pr(>|t|)    
(Intercept)                                  1.860e+02  1.744e+01  10.661   <2e-16 ***
multirestriction_system                     -4.482e+01  3.047e+01  -1.471   0.1413    
restrictions                                -3.738e-01  1.142e+00  -0.327   0.7434    
I(restrictions^2)                            2.016e-02  2.607e-02   0.773   0.4393    
I(restrictions^3)                           -1.286e-04  1.371e-04  -0.938   0.3484    
I(restrictions^4)                            2.026e-07  1.986e-07   1.020   0.3078    
day                                          8.970e-01  4.168e-01   2.152   0.0314 *  
month                                        5.736e+00  2.356e+00   2.435   0.0149 *  
I(restrictions * multirestriction_system)    1.161e+01  8.037e+00   1.445   0.1485    
I(restrictions^2 * multirestriction_system) -5.458e-01  5.468e-01  -0.998   0.3182    
I(restrictions^3 * multirestriction_system)  9.936e-03  1.058e-02   0.939   0.3475    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for gaussian family taken to be 440849.2)

    Null deviance: 1.3517e+10  on 30643  degrees of freedom
Residual deviance: 1.3505e+10  on 30633  degrees of freedom
  (576883 observations deleted due to missingness)
AIC: 485240

Number of Fisher Scoring iterations: 2

```

_pretty clear from the isolated model that the restrictions are not strongly correlated with volume_

___

# Fields

> Hypothesis: the number of fields, optional or required, are not correlated to the average transaction volume.

We are going to test this by reviewing the relationships between the fields and average transaction volume, as well as attempting to fit regressions of fields, required fields, and optional fields to average volume.

```{r}
par(mfrow=c(2,2))
plot(analytic_data$req_fields, analytic_data$avg_vol, cex=0.5, col="red")
plot(analytic_data$opt_fields, analytic_data$avg_vol, cex=0.5, col="red")
plot(I(analytic_data$req_fields+analytic_data$opt_fields), analytic_data$avg_vol, cex=0.5, col="red")
```

![req_fields-avg_vol.jpeg](resources/677C7108E84A340D1EE31821D48628EC.jpg)

```{r}
fit.flds.isolated = glm(avg_vol ~ opt_fields + req_fields + day + month + I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + I(req_fields+opt_fields) + I((req_fields+opt_fields)^2) + I((req_fields+opt_fields)^3), data=analytic_data)
summary(fit.flds.isolated)

Call:
glm(formula = avg_vol ~ opt_fields + req_fields + day + month + 
    I(opt_fields^2) + I(opt_fields^3) + I(req_fields^2) + I(req_fields^3) + 
    I(req_fields + opt_fields) + I((req_fields + opt_fields)^2) + 
    I((req_fields + opt_fields)^3), data = analytic_data)

Deviance Residuals: 
    Min       1Q   Median       3Q      Max  
 -673.8   -187.3   -128.9    -12.1  29727.0  

Coefficients: (1 not defined because of singularities)
                               Estimate Std. Error t value Pr(>|t|)    
(Intercept)                    162.9647    17.4283   9.351  < 2e-16 ***
opt_fields                      40.2478     6.8973   5.835 5.42e-09 ***
req_fields                      87.8233    18.9986   4.623 3.80e-06 ***
day                              0.8980     0.4159   2.159  0.03084 *  
month                            5.5473     2.3484   2.362  0.01817 *  
I(opt_fields^2)                 32.7188     4.0486   8.081 6.63e-16 ***
I(opt_fields^3)                 -1.8571     0.2166  -8.573  < 2e-16 ***
I(req_fields^2)                 32.0808    10.0998   3.176  0.00149 ** 
I(req_fields^3)                 -2.5412     1.0437  -2.435  0.01491 *  
I(req_fields + opt_fields)           NA         NA      NA       NA    
I((req_fields + opt_fields)^2) -40.1503     3.9388 -10.194  < 2e-16 ***
I((req_fields + opt_fields)^3)   2.2055     0.2183  10.102  < 2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

(Dispersion parameter for gaussian family taken to be 438649.3)

    Null deviance: 1.3517e+10  on 30643  degrees of freedom
Residual deviance: 1.3437e+10  on 30633  degrees of freedom
  (576883 observations deleted due to missingness)
AIC: 485087

Number of Fisher Scoring iterations: 2
```

P-values would indicate that the fields are strongly correlated to the average transaction volume.