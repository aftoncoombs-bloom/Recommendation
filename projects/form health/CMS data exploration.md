# CMS data exploration

Widget type legend

| type | name |
|:--:|:--:|
| 14 | FORM_ADDITIONAL_INFO |
| 15 | FORM_BILLING_INFO |
| 17 | FORM_DONATIONS |
| 18 | FORM_PLEDGES |
| 19 | FORM_EVENTS |
| 20 | FORM_LEGAL_INFO |
| 21 | FORM_PART_INFO |
| 22 | FORM_PERSONAL_INFO |
| 23 | FORM_POLITICAL_INFO |
| 24 | FORM_SHARING |
| 25 | FORM_PAYMENT_INFO |
| 54 | OVERRIDE |

## Data prep

I felt it necessary to store the CMS data in a type-first structure for the sake of avoiding having to alter the table in the event of adding widget types. The data, straight out of the database, is as such:

```
   id  stats   org  form  weight  type
0   1   9070  1100  1083     101    24 
1   2   9070  1100  1083     103    22
2   3   9070  1100  1083     104    15 
3   4   9070  1100  1083     105    14
4   5   9070  1100  1083     106    54
```

While this maximizes the flexibility for storage, it's not useful for modeling. As such, we need to restructure the data into a sparse, high dimensional form, collapsing the multiple rows per entry into a single row that gives us all of the types and their positions.

```
   id  stats   org  form  weight  24  22  15  14  54
0   1   9070  1100  1083     101 101 103 104 105 106
```

This structure will allow us to easily model the widget type positions in relation to the conversion and volumes, which will need to be appended to the data frame. 

In order to restrcture the data, we can use the following script:

```{python}
import pandas as pd

df = pd.read_csv("~/Repositories/datasets/analytic_cms.csv")
df.type.unique()
array([ 24.,  22.,  15.,  14.,  54.,  21.,  25.,  17.,  18.,  19.,  23.,
        20.])

df['24'] = 0
df['22'] = 0
df['15'] = 0
df['14'] = 0
df['54'] = 0
df['21'] = 0
df['25'] = 0
df['17'] = 0
df['18'] = 0
df['19'] = 0
df['23'] = 0
df['20'] = 0

for s in df.stats.unique():
    for widget in ['24', '22', '15', '14', '54', '21', '25', '17', '18', '19', '23', '20']:
        df.loc[df.stats==s, str(widget)] = df[(df.stats==s) & (df.type==int(widget))].weight
df = df.groupby('stats').max()
```

_Note that widgets not present in the page result in NaN values set for the weight._

Now we have a data structure that lends itself more to modeling but we still need to pull the conversion and volume over from the other analytics data frames by _stats.id_.
___

## Exploration

First we will review the distributions of weights (the widget positions) within the data.

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

There isn't a lot of variance with the widgets other than the order of the donations, pledges, and events controls (17, 18, 19). My guess here is that not a lot of users are rearranging their forms and could result in insufficient data to establish any real patterns here.

## Correlation

|          |  don_form_trans_vol | don_form_trans_count | conversion |
|:---------------------------:|:-----------:|:----------:|:-----:|
| don_form_trans_vol          |  1.000000   |   0.044298 | 0.000342 |
| don_form_trans_count        |  0.044298   |   1.000000 | 0.605606 |
| 24                          |  -0.010847  |   -0.028226 | -0.004354 |
| 22                          |  -0.001237  |   0.004786 | 0.000267 |
| 15                          |   0.013636  |   0.024928 | -0.003513 |
| 14                          |   0.051458  |   0.058090 | 0.001337 |
| 54                          |  -0.002138  |   0.015736 | -0.001067 |
| 21                          |  -0.001250  |   0.005338 | -0.001021 |
| 25                          |   0.000520  |  -0.020848 | 0.000816 |
| 17                          |   0.002598  |   0.015179 | 0.005293 |
| 18                          |   0.002575  |   0.015443 | 0.005342 |
| 19                          |   0.002623  |   0.015400 | 0.005354 |
| 23                          |  -0.023392  |  -0.123941 | -0.044075 |
| 20                          |  -0.121698  |  -0.125762 | 0.030446 |

 
___

## Plan

1. ~~Pull CMS data from production~~
2. ~~Data formatting~~
3. ~~Pull updated transaction data to cover the CMS dates~~
4. ~~Mapping transaction volumes, counts, and conversion~~
5. ~~Modeling on conversion~~
6. ~~Modeling on volume~~
