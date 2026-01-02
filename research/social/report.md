# Value of a Share

The intent was to determine a quantitative value to a share in social media (ie, each tweet is worth \$23.16 in donations). Unfortunately, it was not possible to tie visits originating from social media to specific transactions so this value cannot be determined. It is however possible to answer other questions regarding social media engagement.

First it is important to consider the source data to maintain perspective as data is unavailable for the majority of organizations. While all efforts have been made to retrieve as much as possible, it is likely data for additional organizations exists but was not retrieved. Checking the social settings available in the production database shows 2,945 forms have entered a Facebook URL and 2,302 forms have entered a Twitter URL. The Facebook forms represented in our dataset as retrieved from the Facebook API is substantially greater (23,655) but the Twitter forms as retrieved from the Twitter API represented is substantially lower (154). __It is reasonable to assume that we have failed to retrieve a large number of Twitter interactions while the Facebook data is likely much more complete.__

__Twitter__

154 forms, 135 organizations
4.42 average tweets per form
5.04 average tweets per organization
1.66 average likes per tweet
14.7 average retweets

__Facebook__

23,655 forms, 4,331 organizations
12.77 average reactions per form
1.59 average comments per form
13.53 average shares per form

2,280 of forms have more than 0 reactions; 132.53 average
1,379 forms have more than 0 comments; 27.27 average
2,973 forms have more than 0 shares; 107.69 average


## 1. Does more shares correlate to more social traffic?

_Correlation metrics range from 1.0 to -1.0, with 1.0 being a perfect linear relationship and -1.0 being an inverse linear relationship. A correlation of 0 is indicative of no relationship whatsoever._

The number of shares is very weakly correlated to social visits with Facebook at 0.15 and Twitter at -0.2. The data is generally quite noisy with a few highly engaged organizations but mostly appearing to be random.

## 2. How many visits does each share generate?

Calculating the actual visits per share continues to appear quite random with a lot of noise. While the mean appears quite good, the median tells a less positive and more realistic story. The weight of specific outliers that manage extremely high engagement pulls these averages rather high, generating many visits per share, while far lower engagement is far more common.

__Visits per Share__

|        | Facebook | Twitter |
|--------|----------|---------|
| Mean   |  2.47    |  3.53   |
| Median |  0.54    |  0.0    |

## 3. Do organizations with more shares and/or social visits have more donations?

The correlation between social engagement and transaction processing is extremely weak and to be taken as random. Looking at the visualizations, it is clear that there is a lot of noise and several outliers, which supports an interpretation that there are select organizations which are highly engaged that outperform others.

|              | Trans Count Corr | Trans Vol Corr |
|--------------|------------------|----------------|
| TW Tweets    |      -0.06       |        0.01    |
| TW Retweets  |      -0.07       |       -0.02    |
| TW Likes     |      -0.06       |       -0.06    |
| FB Reactions |       0.002      |       -0.007   |
| FB Shares    |      -0.01       |       -0.02    |

__Transaction Counts:__

|                     |  Mean  | Median |
|---------------------|--------|--------|
| All                 |  39.89 |   6.00 |
| FB                  |  41.30 |   7.00 |
| TW                  | 121.59 |  23.00 |
| Not socialy engaged |  17.18 |   2.00 |

__Transaction Volume:__

|                     |     Mean    |    Median   |
|---------------------|-------------|-------------|
| All                 |  \$4,816.71 |    \$519.75 |
| FB                  |  \$5,010.83 |    \$589.00 |
| TW                  | \$15,972.23 |  \$3,560.60 |
| Not socialy engaged |  \$1,694.27 |    \$106.00 |

## 4. Do organizations with more shares and/or social visits have higher or lower average donation amounts?

The available social data is limited to a specific window of time so the transaction data was also limited to this same window. As with other relations, the correlation here is very weak with -0.05 for both tweets and Facebook shares to mean transaction volume. While the correlations are seemingly random, the average donation amounts for socially engaged organizations is greater than the organizations that are not socially engaged.

|                      |   Mean   |  Median  |
|----------------------|----------|----------|
| All                  | \$162.83 |  \$71.34 |
| Facebook             | \$165.11 |  \$74.90 |
| Twitter              | \$178.57 | \$112.87 |
| Not socially engaged | \$126.28 |  \$49.07 |

## 5. Do organizations with more shares and/or social visits have higher or lower conversion?

Social media engagement shows again a very weak relation to conversion rates. With Facebook engagement correlation to conversion being -0.003 and Twitter engagement correlation to conversion being -0.008, we can assume this relation is random. In reviewing the actual conversion rates are lower among the organizations that are recorded to be socially engaged. Again, the data is limited to a specific window of time.

|                 | Conversion |
|-----------------|------------|
| All             |   7.50\%   |
| FB active       |   7.14\%   |
| TW active       |   5.20\%   |
| Social inactive |   7.69\%   |

## Conclusion

While the averages do in many instances favor the socially engaged forms, the correlations are always close to random. This should be interpreted as a random relation between the number of shares and performance. As such, we are not able to determine that more shares and engagement in general will correlate to greater fundraising. And while the Facebook is likely fairly represented, the Twitter data is heavily skewed as we know there are more organizations active on Twitter than we were able to retrieve from the API. This may be indicative of a select minority that are more explicit in their calls to action on the platform, thus easier for us to search for, and proving to be generally more effective at translating that activity into fundraising. It is not possible at this time to make this claim with any certainty.