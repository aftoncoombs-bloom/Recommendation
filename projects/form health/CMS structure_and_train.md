# CMS data approach

There's a latent, discrete structure here that I believe needs to be attended to. I think a tree-based algorithm is going to perform best here for modeling purposes.

## Data prep

```{python}
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("~/Repositories/datasets/cms_data.restructured.csv")
X_train, X_test, y_train, y_test = train_test_split(df.drop('conversion', axis=1), df['y'], test_size=0.33, random_state=12)
```

## Data characteristics

- CMS data runs from 2016-11-21 to 2017-02-14
- 2279936 observations; 2274194 observations with visits; lacking transaction data within the CMS data csv (0 observations with transaction count or volumes != 0

## GBM

Going to start with GBM to roll together the tree-based algorithm and a basic ensemble model.

Data structure:

id  |   stats   |   org     |   form    |   [ widget type ... ]

where the widget type columns are the weight values for that widget.

Run trials on estimators and learning rate:

```{python}
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

fits = []

for n in [200, 300, 400, 500, 600, 700, 800]:
    for l_r in [0.001, 0.003, 0.005, 0.008, 0.01, 0.03, 0.05, 0.08, 0.1]:
        # clear variables for safety
        gbr = None
        y_pred = None
        mse = None

        # instantiate & train model
        gbr = GradientBoostingRegressor(n_estimators=n, learning_rate=l_r)
        gbr.fit(X_train, y_train)

        # run prediction
        y_pred = gbr.predict(X_test)

        # evaluate fit
        mse = mean_squared_error(y_test, y_pred)
        fits.append({"estimators": n, "learning_rate": l_r, "mse": mse})

print(fits)
```

___

```{python}
cms.groupby('type').weight.mean()
cms.groupby('type').weight.std()
```

|    |    mean      |     std       |
|----|:------------:|:-------------:|
| 14 |   105.007927 |    0.992156   |
| 15 |   104.245242 |    0.726040   |
| 17 |   193.005383 |   35.423148   |
| 18 |   193.976913 |   35.430945   |
| 19 |   194.926918 |   35.480351   |
| 20 |   109.889764 |    0.344187   |
| 21 |   107.059184 |    0.625263   |
| 22 |   103.048355 |    0.501140   |
| 23 |   102.756506 |    0.653172   |
| 24 |   101.183865 |    1.466978   |
| 25 |   107.966796 |    0.824734   |
| 54 |   106.091849 |    0.548807   |

```{python}
import matplotlib.pyplot as plt

plt.xlabel("Type")
plt.ylabel("Weight")
widget_types = cms.groupby('type').weight.unique().keys()
plt.boxplot(cms.groupby('type').weight.unique().tolist(), labels=widget_types)
```

![](resources/cms_widget_type_weights.jpg)

```{python}
cms_type = cms.groupby('type')
cms_type_keys = cms_type.weight.unique().keys()
print("| type | unique values | count | mean | std |")
print("|:--:|:--:|:---:|:--:|:--:|")
for i in cms_type_keys:
    print('| '+str(i)+' | '+str(len(cms_type.weight.unique()[i]))+' | '+str(len(cms[cms.type==i]))+' | '+str(cms[cms.type==i].weight.mean())+' | '+str(cms[cms.type==i].weight.std())+' | ')

```
| type | unique values | count | mean | std |
|:--:|:--:|:---:|:--:|:--:|
| 14 | 10 | 228468 | 105.007926712 | 0.992155509928 | 
| 15 | 8 | 228656 | 104.245241761 | 0.726039938579 | 
| 17 | 12 | 228688 | 193.00538288 | 35.4231476749 | 
| 18 | 11 | 228660 | 193.976913321 | 35.4309445895 | 
| 19 | 13 | 228455 | 194.926917774 | 35.4803507221 | 
| 20 | 3 | 889 | 109.88976378 | 0.344187335058 | 
| 21 | 10 | 228543 | 107.059183611 | 0.625263401465 | 
| 22 | 9 | 228623 | 103.048354715 | 0.501140054242 | 
| 23 | 3 | 538 | 102.756505576 | 0.65317193473 | 
| 24 | 11 | 222838 | 101.183864511 | 1.46697804638 | 
| 25 | 10 | 228619 | 107.966796286 | 0.824734394108 | 
| 54 | 8 | 226959 | 106.091849189 | 0.548807123557 | 


```{python}
cms_type.weight.value_counts()
```
| type | weight | count |
|:--:|:--:|:--:|
| 14 | 105 | 192961 |
|    | 103 | 10653 |
|    | 106 | 7926 |
|    | 109 | 5680 |
|    | 107 | 3781 |
|    | 101 | 2626 |
|    | 104 | 2222 |
|    | 102 | 1657 |
|    | 108 | 927 |
|    | 100 | 35 |
| 15 | 104 | 194728 |
|    | 106 | 14573 |
|    | 105 | 13091 |
|    | 107 | 2496 |
|    | 108 | 2160 |
|    | 102 | 999 |
|    | 103 | 556 |
|    | 109 | 53 |
| 17 | 200 | 211411 |
|    | 100 | 7516 |
|    | 0  | 4963 |
|    | 201 | 2933 |
|    | 300 | 1402 |
|    | 101 | 228 |
|    | 400 | 106 |
|    | 1   | 39 |
|    | 202 | 39 |
|    | 401 | 26 |
|    | 500 | 14 |
|    | 301 | 11 |
| 18 | 201 | 212551 |
|    | 101 | 7322 |
|    | 1   | 4980 |
|    | 301 | 1403 |
|    | 202 | 1224 |
|    | 200 | 591 |
|    | 102 | 308 |
|    | 401 | 127 |
|    | 100 | 104 |
|    | 0   | 36 |
|    | 501 | 14 |
| 19 | 202 | 210664 |
|    | 102 | 7328 |
|    | 2   | 5020 |
|    | 200 | 2791 |
|    | 302 | 1396 |
|    | 201 | 676 |
|    | 101 | 301 |
|    | 100 | 122 |
|    | 402 | 104 |
|    | 400 | 25  |
|    | 502 | 14  |
|    | 300 | 11  |
|    | 0   | 3   |
| 20 | 110 | 773 |
|    | 109 | 107 |
|    | 111 |  9  |
| 21 | 107 |  196834 |
|    | 108 | 20018 |
|    | 109 | 4865 |
|    | 106 | 2581 |
|    | 103 | 1499 |
|    | 104 | 1496 |
|    | 105 | 1064 |
|    | 101 | 171 |
|    | 110 | 9 |
|    | 102 | 6 |
| 22 | 103 | 200433 |
|    | 104 | 14287 |
|    | 102 | 7454 |
|    | 105 | 2556 |
|    | 101 | 2218 |
|    | 106 | 1118 |
|    | 100 | 294 |
|    | 107 | 241 |
|    | 108 | 22 |
| 23 | 103 | 472 |
|    | 101 | 65  |
|    | 102 | 1   |
| 24 | 101 | 187676 |
|    | 100 | 24632 |
|    | 109 | 4248 |
|    | 108 | 2408 |
|    | 106 | 1357 |
|    | 102 | 861 |
|    | 105 | 476 |
|    | 103 | 360 |
|    | 107 | 338 |
|    | 104 | 312 |
|    | 110 | 170 |
| 25 | 108 | 196798 |
|    | 109 | 22534 |
|    | 107 | 2850 |
|    | 103 | 2572 |
|    | 105 | 1632 |
|    | 104 | 953 |
|    | 102 | 650 |
|    | 106 | 256 |
|    | 101 | 227 |
|    | 110 | 147 |
| 54 | 106 | 196286 |
|    | 107 | 18490 |
|    | 108 | 5504 |
|    | 105 | 3019 |
|    | 103 | 1606 |
|    | 104 | 1317 |
|    | 109 | 681 |
|    | 102 | 56 |

# Modeling

Data prep

```{r}
library(gbm)
library(randomForest)

cms = read.csv("~/Repositories/datasets/cms_data.restructured.csv")
cms = cms[cms$visits>0,]

drops = c("Unnamed..0","Unnamed..0.1","type","weight","mobile_visits","mobile_trans_count","mobile_trans_vol")
cms = cms[,!(names(cms) %in% drops)]

cms$conversion = cms$don_form_trans_count / cms$visits
cms$avg_volume = cms$don_form_trans_vol / cms$don_form_trans_count
cms[is.na(cms$avg_volume),]$avg_volume = 0

factors = c("X24","X22","X15","X14","X54","X21","X25","X17","X18","X19","X23","X20")
for (f in factors) {
  cms[,f] = as.factor(cms[,f])
}

## 75% of the sample size
smp_size <- floor(0.75 * nrow(cms))

## set the seed to make your partition reproductible
set.seed(123)
train_ind <- sample(seq_len(nrow(cms)), size = smp_size)

cms.train <- cms[train_ind, ]
cms.test <- cms[-train_ind, ]

summary(cms$conversion)
     Min.   1st Qu.    Median      Mean   3rd Qu.      Max. 
   0.0000    0.0000    0.0000    0.1886    0.2500 1636.0000 
summary(cms$avg_volume)
    Min.  1st Qu.   Median     Mean  3rd Qu.     Max. 
       0        0        0     1570       33 40000000 
```

## Null Hypothesis Benchark

Assuming no relationship between the control positions, we could always issue a prediction of the mean conversion and avergae volume. For the sake of having a baseline comparison, we will calculate some performance metrics for the mean prediction.

MAE
```{r}
mean(mean(cms.test$avg_volume) - cms.test$avg_volume)
[1] -3.620989e-13
mean(mean(cms.test$conversion)-cms.test$conversion)
[1] 2.128462e-17
```

MSE
```{r}
mean((mean(cms.test$conversion)-cms.test$conversion)^2)
[1] 0.6745144
mean((mean(cms.test$avg_volume)-cms.test$avg_volume)^2)
[1] 44625763938
```

## GBM on Conversion

```{r}
model.gbm = gbm(conversion ~ X24+X22+X15+X14+X54+X21+X25+X17+X18+X19+X23+X20, data=cms.train, n.trees=100, shrinkage=0.01)
summary(model.gbm)

    var   rel.inf
X24 X24 42.844932
X19 X19 39.151893
X54 X54  5.170576
X25 X25  3.657711
X17 X17  3.400290
X22 X22  2.834463
X21 X21  1.544386
X14 X14  1.395749
X15 X15  0.000000
X18 X18  0.000000
X23 X23  0.000000
X20 X20  0.000000

test.y = predict(model.gbm, cms.test, n.trees=100)

mean(test.y-cms.test$conversion)
[1] 0.003836285

mean((test.y - cms.test$conversion)^2)
[1] 0.6739808
```

Form sharing (X24) and form events (X19) controls are the strongest features. The MSE is only slightly better than mean prediction.

![GBM Model Summary](resources/cms_gbm.jpeg)

Now we'll take a look at isolating the features of influence by removing all 0 features.

```{r}
model.gbm = gbm(conversion ~ X24+X22+X14+X54+X21+X25+X17+X19, data=cms.train, n.trees=100, shrinkage=0.01)
summary(model.gbm)

    var    rel.inf
X24 X24 44.7448810
X19 X19 35.5587156
X54 X54  6.6782978
X22 X22  4.5671955
X17 X17  3.8320073
X21 X21  2.5051781
X25 X25  1.1971413
X14 X14  0.9165834
```

![GBM Conversion feature selected](resources/gbm_conv_fs.jpeg)

```{r}
test.y = predict(model.gbm, cms.test, n.trees=100)

mean(test.y-cms.test$conversion)
[1] 0.003026907

mean((test.y - cms.test$conversion)^2)
[1] 0.6739884
```

## GBM on Average Volume

```{r}
model.gbm.vol = gbm(avg_volume ~ X24+X22+X15+X14+X54+X21+X25+X17+X18+X19+X23+X20, data=cms.train, n.trees=100, shrinkage=0.01)
summary(model.gbm.vol)

    var     rel.inf
X14 X14 98.06796720
X15 X15  1.90130791
X54 X54  0.03072489
X24 X24  0.00000000
X22 X22  0.00000000
X21 X21  0.00000000
X25 X25  0.00000000
X17 X17  0.00000000
X18 X18  0.00000000
X19 X19  0.00000000
X23 X23  0.00000000
X20 X20  0.00000000

mean(test.y - cms.test$avg_volume)
[1] -1552.006

mean((test.y - cms.test$avg_volume)^2)
[1] 44514213728
```

Form additional info (X14) seems to be the only control that matters in this model

![GBM CMS avg_vol](resources/gbm_cms_avg_vol.jpeg)

Removing the 0 influence parameters results in a slight redistribution.

```{r}
model.gbm.vol = gbm(avg_volume ~ X15+X14+X54, data=cms.train, n.trees=100, shrinkage=0.01)

summary(model.gbm.vol)
    var   rel.inf
X14 X14 96.997235
X15 X15  3.002765
X54 X54  0.000000
```

![GBM CMS avg_vol Isolated](resources/gbm_cms_avg_vol_iso.jpeg)

```{r}
test.y = predict(model.gbm.vol, cms.test, n.trees=100)
mean(test.y - cms.test$avg_volume)
[1] -1553.096
```

The MAE here is -1553.096, which looks pretty bad but the standard deviation of average volume is 132841.2 and the mean is 1570, so it's actually not that bad. This is slightly worse than the full model, but given the scale I don't think it's of consequence. Still not happy with this performance, however.

```{r}
mean((test.y - cms.test$avg_volume)^2)
[1] 44514066602
```

**Conversion**

|                  |     MAE      |     MSE    |
|:----------------:|:------------:|:----------:|
| Mean conv        | 2.128462e-17 | 0.6745144  |
| GBM conv         | 0.003836285 |  0.6739808  |
| GBM conv (FS)    |  0.6739884  | 0.003026907 |

**Average volume**

|                  |     MAE      |     MSE    |
|:----------------:|:------------:|:----------:|
| Mean avg vol     | -3.6209e-13 | 44625763938 |
| GBM avg vol      |  -1552.006  | 44514213728 |
| GBM avg vol (FS) |  -1553.096  | 44514066602 |

The MAE's on the mean predictions perform really well, but given it's MAE I don't believe it's reliable particularly given the close performance between the models by MSE. By MSE, the feature selection filtered GBM is performing significantly better than the others on conversion, and only slightly better than the others on the average volume. It's entirely possible that there is no strong relationship in terms of average transaction volume but there's a clear relationship with conversion rates.

_Judging from the GBM, the only features relevant to average transaction volume are **additional info**, **billing info**, and **overrides**, while **billing info**, **pledges**, **legal info** and **political info** are not relevant to conversion and **form events** and **form sharing** appearing to play to the strongest roles._