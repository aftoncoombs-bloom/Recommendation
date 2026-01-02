# New form conversion

## Dataset review

converted forms: 1,562
converted forms w/ active status: 73.12%
converted forms w/ transactions: 456
converted forms w/ accepted transactions: 197
total transactions of converted forms: 108,350 (8.24%)

New forms still represents a minority of our forms at this point. While we do have a lot of converted forms, only about a third of those converted are active and processing. This should be taken into consideration when trying to interpret the following statistics. The data set used is limited by timeframe in an effort to use the most representative statistics between new forms and old forms. In this limited timeframe, new forms only represent 8.24% of the total transactions. The sample size is sufficient such that we should be able to see true themes developing, but given it is such a minority that it would be unwise to draw conclusions from specific values.

The following statistics are built from transactions and traffic limited as best as possible to year round frontend data except where otherwise explicitly stated. The conversion date of a given form is drawn a system log message that is created when it is converted without respect for it's status at the time.

## Baseline statistics

For greater context of the data, here is baseline data for both recent history and the isolated timeframe.

All forms (2017+) - one time:
----------------------------------------
Conversion:
- Mean: 1.65%
- Median: 0.00%
Per transaction:
- Mean: $241.76
- Median: $100.00

All forms (2017+) - recurring:
----------------------------------------
Conversion:
- Mean: 1.76%
- Median: 0.00%
Per transaction:
- Mean: $128.81
- Median: $45.00

Recurring frequency:
- Mean: 25 days 15:30
- Median: 26 days 03:25

Qgiv frontend traffic grouped by new form/old form since first form conversion (2020-12-09)
-------------------------------------------------------
Page views:
- Old forms: 867,460
- New forms: 35,750

Normalized:
- Old forms: 96.04%
- New forms: 3.95%

Normalized, past 30 days:
- Old forms: 84.99%
- New forms: 15.01%

Device category traffic overall for relevant time period
-------------------------------------------------------
_All_ 

|         | page views | percentage |
|---------|------------|------------|
| desktop | 4,516,604  |   59.15%   |
| tablet  |   230,368  |    3.02%   |
| mobile  | 2,889,081  |   37.83%   |

_New vs Old_

|         | old form   | old form perc | new form | new form perc |
|---------|------------|---------------|----------|---------------|
| desktop | 4,432,682  |    58.96%     |  83,922  |    70.75%     |
| tablet  |   228,702  |     3.04%     |   1,666  |     1.40%     | 
| mobile  | 2,856,044  |    37.99%     |  33,037  |    27.85%     |

## Conversion

The date of the first conversion (12/09/2020) is rather close to the holiday season so in an effort to get a more fair representation of old forms this was rounded back a few months to 09/01/2020. References to 'all' are references to the data represented within the time frame of 09/01/2020 to the present. The following are statistics drawn from all data within the isolated timeframe, so this will include new forms that are newly created.

### All within the isolated timeframe

|                              |  New forms    |  Old forms         |
|------------------------------|---------------|--------------------|
| Form sample size             | 197 (2.74%)   | 7,001 (97.26%)     |
| Transaction sample size      | 2,205 (0.84%) | 259,860.0 (99.16%) |
| Conversion                   | 9.71%         | 5.88%              |
| One time mean conversion     | 3.29%         | 3.09%              |
| One time median conversion   | 0.00%         | 0.00%              |
| Recurring mean conversion    | 6.97%         | 3.28%              |
| Recurring median conversion  | 0.00%         | 0.00%              |
| One time mean transaction    | \$321.88      | \$259.98           |
| One time median transaction  | \$113.57      | \$107.42           |
| Recurring mean transaction   | \$67.38       | \$370.32           |
| Recurring median transaction | \$42.62       | \$46.17            |
| Mean recurring frequency     | 9 days 10:56  | 9 days 10:56       |
| Median recurring frequency   | 11 days 16:00 | 11 days 16:00      |
| One time / recurring ratio   | 1.98          | 2.23               |


As we can see here, new form is represented in the extreme minority of less than 3% of forms and less than 1% of transactions. We see a slight improvement in one time mean conversions for new forms but the difference is probably insufficient to be considered valid. The recurring conversion more than doubled so it stands out as a theme that we may be able to rely upon. As stated earlier, the specific value shouldn't be considered valid given the extreme minority of the sample size.

There is a great difference between the mean's and median's of transaction values for both new and old forms. The mean's of transaction values are often skewed heavily by a few extremely large transactions, so this is to be expected. There is an improvement in one time per transaction values for new forms, but I think the median value is a better representation here. While the difference is not as substantial in the median as the mean, it is still a meaningful increase at > 5%. Recurring on the other hand sees a decrease, quite dramatically in the mean but a more tepid decrease in the median at around 9.5%. While this might be a little discouraging at first glance, it is important to remember the doubling of recurring conversion. If we are to take these numbers as absolute, twice the recurring the transactions each which are 10% less is still a signficant increase of revenue.


### Last 30 days

This data considers all active, processing forms for the last 30 days. This will exclude potential extremes of the holiday season and presumably a greater proportion of new form observations will be of mature, stable form activity. 

|                              |  New forms    |  Old forms         |
|------------------------------|---------------|--------------------|
| Form sample size             | 180 (4.03%)   | 4,353 (97.36%)     |
| Transaction sample size      | 1,709 (4.52%) | 36,139 (95.48%)    |
| One time mean conversion     | 4.12%         | 2.93%              |
| One time median conversion   | 0.00%         | 0.00%              |
| Recurring mean conversion    | 9.38%         | 3.79%              |
| Recurring median conversion  | 0.00%         | 0.00%              |
| One time mean transaction    | \$325.44      | \$221.79           |
| One time median transaction  | \$103.95      | \$102.15           |
| Recurring mean transaction   | \$62.70       | \$1,812.03         |
| Recurring median transaction | \$40.08       | \$46.46            |
| Mean recurring frequency     | 7 days 04:01  | 8 days 19:44       |
| Median recurring frequency   | 0 days 00:00  | 7 days 00:00       |
| One time / recurring ratio   | 2.16          | 1.72               |


We see a greater proportional increase in the transaction sample size for new forms here than the forms sample size. This may seem unimportant but is worth noting as it is what we should expect to see if the new forms do in fact have a greater conversion rate than the old forms so it is a small contribution to our confidence in the interpretation of the themes we are seeing in the data. We see a continuation here of the conversion trends we saw in all data, but to a greater degree than before. We see a 40% improvement in one time conversion and a 150% improvement in recurring conversion for new forms.

With the very noticeable exception of recurring mean transaction value for old forms, the per transaction average values are not too dissimilar from all the data we saw previously. Regarding the recurring mean for old forms, this value is extremely skewed by a small number of very large transactions. Again, I think the median values are a better representation and these values are not meaningfully different which adds confidence to the validity of those values.


### Forms w/ transactions in new & old, isolated timeframe

This data is a direct comparison of data only from forms with transactions on the old form and the new form and includes all tranactions from the isolated timeframe.

|                              |  New forms    |  Old forms         |
|------------------------------|---------------|--------------------|
| Form sample size             | 196 (2.80%)   | 196 (2.80%)        |
| Transaction sample size      | 2,205 (0.84%) | 11,122 (4.24%)     |
| Transactions per form        | 5.89          | 33.67              |
| One time mean conversion     | 3.30%         | 6.76%              |
| One time median conversion   | 0.00%         | 0.00%              |
| Recurring mean conversion    | 6.98%         | 8.29%              |
| Recurring median conversion  | 0.00%         | 0.00%              |
| One time mean transaction    | \$321.88      | \$303.33           |
| One time median transaction  | \$113.57      | \$104.00           |
| Recurring mean transaction   | \$67.38       | \$736.48           |
| Recurring median transaction | \$42.62       | \$39.14            |
| Mean recurring frequency     | 9 days 10:56  | 9 days 10:56       |
| Median recurring frequency   | 11 days 16:00 | 11 days 16:00      |
| One time / recurring ratio   | 1.98          | 2.13               |


The direct comparison of forms, pre and post conversion, does not look as promising as other views of the data. We see a falling conversion for one time and recurring, and a decrease in per transaction mean values. The median per transaction values do increase slightly. This timeframe does include the holiday season which  contains a greater proportion of old form observations than new form observations.


### Forms w/ transactions in new & old, last 60 days:

This data is again a direct comparison of data from forms with transactions on the old form and the new form, but is isolated to the last 60 days. We have a greater proportion of new form observations than old form observations, including more observations of established new forms and excluding the holiday season which would favor the old forms.

|                              |  New forms     |  Old forms         |
|------------------------------|----------------|--------------------|
| Form sample size             | 161 (7.62%)    | 58 (2.74%)         |
| Transaction sample size      | 1,684 (48.84%) | 447 (12.96%)       |
| Transactions per form        | 5.53           | 6.00               |
| One time mean conversion     | 9.62%          | 3.53%              |
| One time median conversion   | 0.00%          | 0.00%              |
| Recurring mean conversion    | 6.98%          | 3.18%              |
| Recurring median conversion  | 0.00%          | 0.00%              |
| One time mean transaction    | \$336.08       | \$410.29           |
| One time median transaction  | \$103.00       | \$87.50            |
| Recurring mean transaction   | \$62.48        | \$62.37            |
| Recurring median transaction | \$40.00        | \$31.00            |
| Mean recurring frequency     | 6 days 02:59   | 6 days 02:59       |
| Median recurring frequency   | 0 days 00:00   | 0 days 00:00       |
| One time / recurring ratio   | 2.22           | 5.57               |


We see a 172% increase in one time conversion and a 120% increase in recurring conversion. With respect to per transaction values, one time and recurring noticeably improve by median. While this is probably the most reliably indicative performance comparison we have looked at thus far, the improvements are likely exaggerated due to the minority representation of old form activity.

### Conclusion

As has been stated before, it is important to not draw conclusions from specific values but at this juncture I do believe we have sufficient data to begin to interpret a theme. I think it is safe to assume that we will see a slight increase in one time conversion and a noticeable, if not substantial, increase in recurring conversion. There are consistent variations in per transaction means but largely are not so differentiated that it would be fair to assume these will remain roughly the same. With the improvement in conversion rates, it does appear safe to say that new forms are performing better than older forms on a number of fronts.

Specific form features and settings were checked but we have insufficient data at this juncture to determine anything meaningul as all statistics appeared random or undifferentiated between new and old forms.

## New form settings & features

As with the other form features and settings, we have insufficient data to interpret anything meaningful from breaking down by groups. As these are newly deployed, it was worth looking at them even knowing in advance that conclusions would be unreliable.

### Mean new settings values:

Sample means were examined from the new form features. For example, per form, an appearance setting of 0 that switched to 1 halfway through it's tracked lifetime will be represented as 0.5.  

- Recurring CTA after: 0.000071
- Recurring CTA before: 0.000607
- Appearance (single vs multi-step): 0.002642
- Conditional fields count: 0.000006

The setting values are rather low as there are a lot of samples not utilizing these features. Low numbers could be indicative of either low or late adoption, not exclusively one or the other.

For conversion values, the value was averaged with all other forms with the same setting or feature value which resulted in sample sizes from 5 to 40 with random results. With such low sample sizes and no discernable relationships or trends, this data is omitted.

## Device category

This data was built using the device category field from Google Analytics and our transaction user agent string data. I can only assume that Google Analytics data is valid and have no reason to believe otherwise. Our transaction user agent string data however cannot be presumed to be absolutely reliable. 

The transactions were filtered to the previously used timeframe (9/01/2020 forward) and approximately 11% of the transactions do not have user agent string values. Furthermore, the device categorization was used based upon keys found in the string. The raw data presents in the form of "Mozilla50iPadCPUOS1252likeMacOSXAppleWebKit605...". The most efficient way to categorize these was to find the most common token words to identify the device such as "iPad" for the prior example case. Reasonable effort was put into accurately categorize the data but should not be assumed to be absolutely accurate.

The Android useragent strings do not consistently identify the device category so it is not possible to categorize Android devices as "phone" vs "tablet" without an extensive list for specific devices. iPad devices can be reliably identified and represent a little more than 11,000 transactions which can be contrasted with more than 134,000 for iPhone. Given the iPad transactions, I believe it safe to assume that tablets generally represent a relatively low number of transactions so being unable to distinguish between Android tablets and Android phones, tablet devices were merged into "mobile" for the following.

All

|           | Desktop | Mobile |
|-----------|---------|--------|
| One time  |  7.78%  |  4.95% |
| Recurring |  2.35%  |  0.46% |

Isolated timeframe device conversion means

|              | Desktop conversion | Mobile conversion |
|--------------|--------------------|-------------------|
| New template |        9.02%       |        4.87%      |
| Old template |        7.24%       |        4.49%      |

Last 60 days

|              | Desktop conversion | Mobile conversion |
|--------------|--------------------|-------------------|
| New template |        9.90%       |        4.50%      |
| Old template |        5.92%       |        4.07%      |


# Bounces

This data was newly downloaded from Google Analytics so I calculated general stats for fun.

## Historical bounce rate

All time

|      | Mean  | Median |
|------|-------|--------|
| P2P  | 20.1% | 0.0%   |
| Qgiv | 25.1% | 0.0%   |

By year 

|      | P2P    | Qgiv   |
|------|--------|--------|
| 2018 | 17.12% | 25.63% |
| 2019 | 17.65% | 27.43% |
| 2020 | 22.89% | 23.11% |
| 2021 | 21.92% | 18.79% |


## New forms bounce rate

All time bounce rates:
- Old forms: 22.85%
- New forms: 13.39%

2021 bounce rates:
- Old forms: 20.44%
- New forms: 13.52%

Last 30 days bounce rates:
- Old forms: 18.42%
- New forms: 14.89%

Bounce rates for new forms is also consistently lower than old forms by 20% to 40%, depending upon which dataset we choose. It is interesting to note however that with the forward moving focus of time bounce rates for old forms decrease and new forms increase. These might merge eventually as it does appear to be trending in that direction so we should keep an eye on it.

# Session duration

This data was also newly downloaded so it is included for fun or something. I am not aware of known anomalies in this data (as sourced from Google Analytics) but the observations contain many abnormalities. I might be misunderstanding what is being tracked, but there are not infrequent observations with multiple page views, 0 bounces, but also a 0 session duration. Based upon my interpretation of this data point, it should not be possible to have a 0 average session duration with 0 bounces unless there were also 0 page views. So not going to read anything into this but it's here.

P2P
- mean: 194.49
- median: 0.00
Qgiv
- mean: 195.35
- median: 0.00

All vs new form:
- Old form: 195.181249
- New form: 84.216112

2021 all vs new form:
- Old form: 194.883008
- New form: 83.106275

Past 30 days all vs new form:
- Old form: 178.592348
- New form: 50.525578

## Removing 0 values

Sample size:
- all: 27,236,308
- non-zero: 6,445,848 (23.67%)

P2P:
- mean: 1093.65
- median: 245.00

Qgiv:
- mean: 728.06
- median: 199.00

All vs new form:
- Old form: 844.099719
- New form: 284.689782

2021 all vs new form:
- Old form: 842.496811
- New form: 282.720871

Past 30 days all vs new form:
- Old form: 929.721204
- New form: 675.828070