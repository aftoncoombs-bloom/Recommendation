# Features

1. required fields
2. optional fields
3. required fields + optional fields
4. restrictions in amounts
5. restrictions in multirestriction
6. required dedication fields
7. optional dedication fields

___

## Data prep

```{r}
# load data sets
analytic_base <- read.csv("~/Repositories/datasets/analytic_base.csv")
analytic_qgiv_stats <- read.csv("~/Repositories/datasets/analytic_qgiv_stats.csv")
transactions <- read.csv("~/Repositories/datasets/transactions.csv")

# merge dataframes
analytic_data <- merge(analytic_base, analytic_qgiv_stats, by.x="id", by.y="base")
rm(analytic_base)
rm(analytic_qgiv_stats)
analytic_data <- analytic_data[analytic_data$total_visits > 0,]
# remove duplicate columns (ie, ID)
analytic_data <- analytic_data[, !duplicated(colnames(analytic_data))]

# add conversion column
analytic_data$conversion <- analytic_data$don_form_trans_count/analytic_data$total_visits * 100
```

___

## Looking at all p values & ANOVA

```{r}
fit.all = lm(conversion ~ pledges_count + events_count + restrictions + amounts + opt_ded_flds + req_ded_flds + opt_fields + req_fields + multirestriction_system, data=analytic_data)
summary(fit.all)

Call:
lm(formula = conversion ~ pledges_count + events_count + restrictions + 
    amounts + opt_ded_flds + req_ded_flds + opt_fields + req_fields + 
    multirestriction_system, data = analytic_data)

Residuals:
    Min      1Q  Median      3Q     Max 
  -9.34   -2.08   -1.89   -1.79 2598.04 

Coefficients: (1 not defined because of singularities)
                          Estimate Std. Error t value Pr(>|t|)    
(Intercept)              1.5915440  0.0456483  34.865  < 2e-16 ***
pledges_count            0.0165000  0.0098960   1.667   0.0954 .  
events_count            -0.0341136  0.0054925  -6.211 5.27e-10 ***
restrictions             0.0061077  0.0008558   7.137 9.55e-13 ***
amounts                  0.0613301  0.0086369   7.101 1.24e-12 ***
opt_ded_flds                    NA         NA      NA       NA    
req_ded_flds             0.0148554  0.0344003   0.432   0.6659    
opt_fields               0.0901135  0.0097016   9.289  < 2e-16 ***
req_fields              -0.1312972  0.0185580  -7.075 1.50e-12 ***
multirestriction_system  5.3950880  0.0776532  69.477  < 2e-16 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 16.17 on 607518 degrees of freedom
Multiple R-squared:  0.008308,	Adjusted R-squared:  0.008295 
F-statistic: 636.2 on 8 and 607518 DF,  p-value: < 2.2e-16

anova(fit.all)

Analysis of Variance Table

Response: conversion
                            Df    Sum Sq Mean Sq   F value    Pr(>F)    
pledges_count                1      5664    5664   21.6524 3.269e-06 ***
events_count                 1     11708   11708   44.7546 2.235e-11 ***
restrictions                 1     24055   24055   91.9564 < 2.2e-16 ***
amounts                      1        14      14    0.0518    0.8200    
req_ded_flds                 1       455     455    1.7377    0.1874    
opt_fields                   1      6193    6193   23.6756 1.140e-06 ***
req_fields                   1     20576   20576   78.6546 < 2.2e-16 ***
multirestriction_system      1   1262715 1262715 4827.0117 < 2.2e-16 ***
Residuals               607518 158922737     262                        
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
```

_Noticing that the fitted p-values & ANOVA results do not agree on all features._ Features disagreeing are 

- pledges_count
- amounts

pledges_count is flagged as an insignificant feature in the fit analysis while ANOVA flags it as significant, whereas amounts is flagged as significant in the fit analysis and insignificant by ANOVA.

___

## Required Fields

```{r}
# plotting
par(mfrow=c(2,2))
plot(analytic_data$req_fields, analytic_data$don_form_trans_vol)
plot(analytic_data$req_fields, analytic_data$don_form_trans_count)
plot(analytic_data$req_fields, analytic_data$conversion)
plot(analytic_data$req_fields, analytic_data$visits)
```

![req_fields relations.jpeg](resources/C075ADEFEA776AA16A711C3F0728D038.jpg)

___

## Optional Fields

```{r}
# plotting
par(mfrow=c(2,2))
plot(analytic_data$opt_fields, analytic_data$don_form_trans_vol)
plot(analytic_data$opt_fields, analytic_data$don_form_trans_count)
plot(analytic_data$opt_fields, analytic_data$conversion)
plot(analytic_data$opt_fields, analytic_data$visits)
```

![opt_fields relations.jpeg](resources/F4D80A992052BD7D189075D91E0B63F8.jpg)

___

## Optional Fields + Required Fields

```{r}
# prep
analytic_data$fields = analytic_data$req_fields + analytic_data$opt_fields
# plotting
par(mfrow=c(2,2))
plot(analytic_data$fields, analytic_data$don_form_trans_vol)
plot(analytic_data$fields, analytic_data$don_form_trans_count)
plot(analytic_data$fields, analytic_data$conversion)
plot(analytic_data$fields, analytic_data$visits)
```

![fields relations.jpeg](resources/5EB94E379ED1D7E8D24494ABED332AE2.jpg)

___

## Restrictions in Amounts

```{r}
# prep
amts_data = analytic_data[analytic_data$multirestriction_system == 0,]
# plotting
par(mfrow=c(2,2))
plot(amts_data$restrictions, amts_data$don_form_trans_vol)
plot(amts_data$restrictions, amts_data$don_form_trans_count)
plot(amts_data$restrictions, amts_data$conversion)
plot(amts_data$restrictions, amts_data$visits)
```

![restrictions relations.jpeg](resources/A70EF80EDA12D1612A01A50924EC431E.jpg)

___

## Restrictions in Multirestriction

```{r}
# prep
mltrst_data = analytic_data[analytic_data$multirestriction_system == 1,]
# plotting
par(mfrow=c(2,2))
plot(mltrst_data$restrictions, mltrst_data$don_form_trans_vol)
plot(mltrst_data$restrictions, mltrst_data$don_form_trans_count)
plot(mltrst_data$restrictions, mltrst_data$conversion)
plot(mltrst_data$restrictions, mltrst_data$visits)
```

![mltrest relations.jpeg](resources/20ECE47F5887033F440EB6F436C72023.jpg)

___

## Required Dedication Fields

```{r}
# plotting
par(mfrow=c(2,2))
plot(analytic_data$req_ded_flds, analytic_data$don_form_trans_vol)
plot(analytic_data$req_ded_flds, analytic_data$don_form_trans_count)
plot(analytic_data$req_ded_flds, analytic_data$conversion)
plot(analytic_data$req_ded_flds, analytic_data$visits)
```

![req_ded_flds relations.jpeg](resources/255E9C8B31D5B22526A990F3D0F28B34.jpg)

### fit

Quadratic fit
```{r}
fit.req_ded_flds.2 = lm(conversion~req_ded_flds+I(req_ded_flds^2), data=analytic_data)
anova(fit.req_ded_flds.2)

---------------------------------------------------------------
Analysis of Variance Table

Response: conversion
                      Df    Sum Sq Mean Sq F value    Pr(>F)    
req_ded_flds           1       327   327.3  1.2408 0.2653191    
I(req_ded_flds^2)      1      3774  3774.0 14.3075 0.0001553 ***
Residuals         607524 160250014   263.8                      
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
---------------------------------------------------------------

summary(fit.req_ded_flds.2)

---------------------------------------------------------------
Call:
lm(formula = conversion ~ req_ded_flds + I(req_ded_flds^2), data = analytic_data)

Residuals:
    Min      1Q  Median      3Q     Max 
  -3.35   -2.36   -2.36   -2.36 2597.64 

Coefficients:
                  Estimate Std. Error t value Pr(>|t|)    
(Intercept)        2.36473    0.02135 110.757  < 2e-16 ***
req_ded_flds      -0.39398    0.10012  -3.935 8.32e-05 ***
I(req_ded_flds^2)  0.07644    0.02021   3.783 0.000155 ***
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 16.24 on 607524 degrees of freedom
Multiple R-squared:  2.559e-05,	Adjusted R-squared:  2.23e-05 
F-statistic: 7.774 on 2 and 607524 DF,  p-value: 0.0004205
---------------------------------------------------------------
```

Cubic fit

```{r}
fit.req_ded_flds.3 = lm(conversion~req_ded_flds+I(req_ded_flds^2)+I(req_ded_flds^3), data=analytic_data)
anova(fit.req_ded_flds.3)

---------------------------------------------------------------
Analysis of Variance Table

Response: conversion
                      Df    Sum Sq Mean Sq F value    Pr(>F)    
req_ded_flds           1       327   327.3  1.2408 0.2653169    
I(req_ded_flds^2)      1      3774  3774.0 14.3077 0.0001552 ***
I(req_ded_flds^3)      1      1708  1708.3  6.4762 0.0109328 *  
Residuals         607523 160248306   263.8                      
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
---------------------------------------------------------------

summary(fit.req_ded_flds)

---------------------------------------------------------------
Call:
lm(formula = conversion ~ req_ded_flds + I(req_ded_flds^2) + 
    I(req_ded_flds^3), data = analytic_data)

Residuals:
    Min      1Q  Median      3Q     Max 
  -2.66   -2.37   -2.37   -2.37 2597.63 

Coefficients:
                  Estimate Std. Error t value Pr(>|t|)    
(Intercept)        2.36841    0.02140 110.677  < 2e-16 ***
req_ded_flds      -0.73531    0.16737  -4.393 1.12e-05 ***
I(req_ded_flds^2)  0.28372    0.08392   3.381 0.000723 ***
I(req_ded_flds^3) -0.02553    0.01003  -2.545 0.010933 *  
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 16.24 on 607523 degrees of freedom
Multiple R-squared:  3.625e-05,	Adjusted R-squared:  3.131e-05 
F-statistic: 7.342 on 3 and 607523 DF,  p-value: 6.447e-05
---------------------------------------------------------------
```

### visualization

```{r}
fit.req_ded_flds.2 = lm(conversion~req_ded_flds+I(req_ded_flds^2), data=analytic_data)
fit.req_ded_flds.3 = lm(conversion~req_ded_flds+I(req_ded_flds^2)+I(req_ded_flds^3), data=analytic_data)
fit.req_ded_flds.4 = lm(conversion~req_ded_flds+I(req_ded_flds^2)+I(req_ded_flds^3)+I(req_ded_flds^4), data=analytic_data)

plot(analytic_data$req_ded_flds, analytic_data$conversion, ylim=c(0,10), cex=0.3)

req_ded_flds.mean = aggregate(analytic_data$conversion~analytic_data$req_ded_flds, FUN=mean)
lines(req_ded_flds.mean$`analytic_data$req_ded_flds`, req_ded_flds.mean$`analytic_data$conversion`, col="blue")

fit.req_ded_flds.preds.2 = lapply(c(0:7), FUN=function(x){
  analytic_data[210,]$req_ded_flds = x
  predict(fit.req_ded_flds.2, analytic_data[210,])
})
fit.req_ded_flds.preds.3 = lapply(c(0:7), FUN=function(x){
  analytic_data[210,]$req_ded_flds = x
  predict(fit.req_ded_flds.3, analytic_data[210,])
})
fit.req_ded_flds.preds.4 = lapply(c(0:7), FUN=function(x){
  analytic_data[210,]$req_ded_flds = x
  predict(fit.req_ded_flds.4, analytic_data[210,])
})
lines(c(0:7), fit.req_ded_flds.preds.2, col="green")
lines(c(0:7), fit.req_ded_flds.preds.3, col="purple")
lines(c(0:7), fit.req_ded_flds.preds.4, col="red")
```

![req_ded_flds-conversion.jpeg](resources/461E7A63DF3D8FF865F19938D71A11AD.jpg)

Pretty sure the more sparse, higher field count observations are unfairly pulling the conversion rate up. Taking a look at the representation:

```{r}
aggregate(analytic_data$conversion~analytic_data$req_ded_flds, FUN=mean)
  analytic_data$req_ded_flds analytic_data$conversion
1                          0                2.3674564
2                          1                1.9818144
3                          2                1.4568516
4                          3                0.9555314
5                          4                2.6809528
6                          5                2.9357662
7                          6                1.0285608
8                          7                3.0397438
```

```{r}
lapply(c(0:7), FUN=function(x){
  print(paste(x, 'req ded fields:', dim(analytic_data[analytic_data$req_ded_flds==x,])[1]))
})
[1] "0 req ded fields: 575405"
[1] "1 req ded fields: 19938"
[1] "2 req ded fields: 3905"
[1] "3 req ded fields: 779"
[1] "4 req ded fields: 2748"
[1] "5 req ded fields: 3208"
[1] "6 req ded fields: 897"
[1] "7 req ded fields: 647"
```

_need to try removing the top outliers from the data set_

```{r}
# remove top 5% of conversion (outliers)
analytic_data = analytic_data[analytic_data$conversion < 500,]
# remove entries with conversion > 50 & required dedication fields > 5 (14 entries removed)
analytic_data = analytic_data[analytic_data$conversion < 50 & analytic_data$req_ded_flds < 5,]

# attempt a new fits
fit.req_ded_flds.2 = lm(conversion~req_ded_flds+I(req_ded_flds^2), data=analytic_data)
fit.req_ded_flds.3 = lm(conversion~req_ded_flds+I(req_ded_flds^2)+I(req_ded_flds^3), data=analytic_data)
fit.req_ded_flds.4 = lm(conversion~req_ded_flds+I(req_ded_flds^2)+I(req_ded_flds^3)+I(req_ded_flds^4), data=analytic_data)

# re-plot everything
plot(analytic_data$req_ded_flds, analytic_data$conversion, ylim=c(0,10), cex=0.3)

req_ded_flds.mean = aggregate(analytic_data$conversion~analytic_data$req_ded_flds, FUN=mean)
lines(req_ded_flds.mean$`analytic_data$req_ded_flds`, req_ded_flds.mean$`analytic_data$conversion`, col="blue")

fit.req_ded_flds.preds.2 = lapply(c(0:7), FUN=function(x){
  analytic_data[210,]$req_ded_flds = x
  predict(fit.req_ded_flds.2, analytic_data[210,])
})
fit.req_ded_flds.preds.3 = lapply(c(0:7), FUN=function(x){
  analytic_data[210,]$req_ded_flds = x
  predict(fit.req_ded_flds.3, analytic_data[210,])
})
fit.req_ded_flds.preds.4 = lapply(c(0:7), FUN=function(x){
  analytic_data[210,]$req_ded_flds = x
  predict(fit.req_ded_flds.4, analytic_data[210,])
})
lines(c(0:7), fit.req_ded_flds.preds.2, col="green")
lines(c(0:7), fit.req_ded_flds.preds.3, col="purple")
lines(c(0:7), fit.req_ded_flds.preds.4, col="red")
```

![pruned req ded flds.png](resources/E2057F6BDE7A87E1A3AFF3924A964EBA.png)

This is not looking good for a solid fit. Whatever prediction accuracy there may be here, the variance **doesn't appear to be produce anything truly useful**, even after attempting to carve up the data set.

___

## Optional Dedication Fields

```{r}
summary(analytic_data$opt_ded_flds)

   Min. 1st Qu.  Median    Mean 3rd Qu.    Max. 
      0       0       0       0       0       0
```
This will show that the optional dedication fields are all 0.