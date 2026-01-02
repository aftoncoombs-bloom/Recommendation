Exploring the relationships between classification and category counts to registration count, amount, conversion and donation count, amount, and conversion.

# Classification

Value distribution:

| metric | value  |
|--------|--------|
| mean   |  5.03  |
| std    | 22.847 |
| mode   |  0     |
| unique | 65     |

Correlations and feature importance from random forest:

|     feature    | correlation | feature importance |
|----------------|-------------|--------------------|
| reg amount     |   0.002278  |   0.109922880832   |
| reg count      |   0.001805  |   0.184880252543   |
| reg conversion |   0.007188  |   0.12091805936    |
| don volume     |   0.075125  |   0.217142477669   |
| don count      |   0.104031  |   0.138553345564   |
| don conversion |   0.005044  |   0.109342008573   |

The correlations are all pretty weak but it is evident that the random forest model is finding a meaningful (and likely nonlinear) relationship between the classification count and most of these values. The feature importance values are among the highest of within the model.

It is apparent to me that there is something to this, but I have yet to find the underlying relationship between the number of classifications and the fundraising outcome values I'm modeling against. This is certainly a worthy addition to the feature set for the model as the importance value implies, but there is certainly more to be found here in terms of interpretation. It is possible that the spread of values (65 uniques) for classification count is diluting these values and making it difficult to reveal their true relationship to the outcomes.

## Deeper dive

Looking at the value counts, there are definitely quite a groupings (by classification count) that have a very small number of observations, so attempting to narrow the view down to the entries that truly matter (tentatively trying only those entries with greater than 100 entries per classification count) and rerunning the correlation.

```python
s = df.class_count.value_counts().sort_index()
df[df.class_count.isin(s[s>100].index)][['class_count', 'don_count', 'donation_conversion']].corr()
```

correlation between classification count and donation count: -0.097608
correlation between classification count and donation conversion: 0.185567

This filter certainly helped smooth out the visualization of this relationship (classification count on the x axis, number of corresponding observations on the y axis), this didn't really help with the donation count correlation. Donation conversion on the other hand was significantly improved from about 5% to about 19%.

Looking at the conversion rates in different value ranges:

| classification count range | mean donation conversion |
|----------------------------|--------------------------|
| (-0.291, 24.25]            |        0.011067          |
| (24.25, 48.5]              |        0.017430          |
| (48.5, 72.75]              |        0.025005          |
| (72.75, 97.0]              |        0.007589          |
| (97.0, 145.5]              |        0.000000          |
| (145.5, 242.5]             |        NaN               |
| (242.5, 291.0]             |        0.000000          |

Here, prior ranges of 0 to 50 at 1% and 49 to 97 at 2%, neither of which is terribly strong but makes sense. Broadened the cuts out a bit to capture more narrow windows and now seeing some stronger trends building from 0 to 97, peaking at 2.5% between 49 and 73. The total worthwhile range here appearing to be 0 to 97 classifications, which is such a wide range. This certainly explains the improvement in correlation when limiting the value range to < 100 classifications.

# Category

Value distribution:

| metric | value  |
|--------|--------|
| mean   |  3.128 |
| std    |  3.976 |
| mode   |  1     |
| unique | 26     |

Correlations:

|    feature     | correlation | feature importance |
|----------------|-------------|--------------------|
| reg amount     |   0.007043  |   0.135840000731   |
| reg count      |   0.002151  |   0.173049213546   |
| reg conversion |   0.004348  |   0.145226961353   |
| don volume     |   0.028014  |   0.0572038392748  |
| don count      |   0.026822  |   0.0490335853609  |
| don conversion |   0.047141  |   0.132199345656   |

Much like the classification count, these values are not looking great except for the feature importances. The category count is clearly contributing something of value to the random forest model output but the correlations are so low, and the feature importances not so substantial, that I am inclined to conclude that there is yet again an underlying relationship here that has yet to be revealed. And yet again, clearly a worthy contributor to the model.

## Deeper dive

Looking at just the entries with greater than 100 entries by value count of cateogory count and rerunning the correlation.

```python
s = df.cat_count.value_counts().sort_index()
df[df.cat_count.isin(s[s>50].index)][['cat_count', 'don_count', 'donation_conversion']].corr()
```

Correlation between category count and donation count: -0.028011
Correlation between category count and donation conversion: -0.047536

Same as the classification, this smooths out the visualization but doesn't seem to help out the correlation to donation count much at all. Donation conversion correlation was significantly improved, 5 times greater than before removing the less observed counts. The same effect is seen in classifications after filtering out the less observed counts.

Looking at mean conversion for category count ranges.

| category count range | mean donation conversion |
|----------------------|--------------------------|
| (-0.048, 8.0]        |         0.011669         |
| (8.0, 16.0]          |         0.004495         |
| (16.0, 20.0]         |         0.012486         |
| (20.0, 24.0]         |         0.001233         |
| (24.0, 32.0]         |         0.004130         |
| (32.0, 40.0]         |         0.0              |
| (40.0, 48.0]         |         0.025145         |

Seeing here that the greatest conversion rate is between 40 and 48 at 2.5%, next is between 16 and 20 at 1.2%. Little all over the place, which explains the correlations but not the feature importances.

Notebooks:
- [class and cat examination](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/Class%20and%20Cat%20examination.ipynb)
- [donation count modeling](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/Donation%20Count%20Modeling.ipynb)