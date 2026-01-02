Exploring the binary settings of the P2P event looking at correlation and feature importance as it corresponds to donation count, donation conversion, registration count, and registration conversion.

Features modeled against:

|        Feature          |     Mean   | Standard deviation |
|-------------------------|------------|--------------------|
| registration count      | 0.37093802 |    2.76980622132   |
| registration amount     | 3.89125182 |    46.411891162    |
| registration conversion | 0.16248978 |   1.49476779465    |
| donation count          | 0.78600575 |  3.41695877792409  |
| donation amount         | 59.2210437 | 289.40387710304617 |
| donation conversion     | 0.01124785 |  0.0542243230004   |


# Teams enabled

Correlation to registration count: 0.001514
Correlation to registration amount:  0.003068
Correlation to donation count: 0.048644
Correlation to donation amount: 0.025398
Feature importance to donation count: 0.008856269604
Feature importance to donation conversion: 0.0534776968697

The correlation and feature importance for teams enabled setting is not terribly strong in any target, but the value counts here present a value imbalance that makes it difficult to extract any meaningful information from it anyway.

| value | count  |
|-------|--------|
|   1   | 227966 |
|   0   |  39811 |
|   5   |    319 |

There are so many observations where teams are enabled that whatever effect it may be having is not likely to surface.

## Rebalancing

After rebalancing the data set, we see the following

Correlations to allows teams:

|       column        | correlation |
|---------------------|-------------|
| registration count  |  0.004526   |
| registration amount |  0.003325   |
| donation volume     |  0.046075   |
| donation count      |  0.096507   |
| reg conversion      |  0.011977   |
| don conversion      |  0.017141   |

Feature importances from random forest:

|       column        |   importance  |
|---------------------|---------------|
| registration count  | 0.01413269488 |
| registration amount | 0.04388463572 |
| donation volume     | 0.00954260601 |
| donation count      | 0.00764364463 |
| reg conversion      | 0.02860379081 |
| don conversion      | 0.06516829085 |

None of the correlations here are particularly strong, but there is a relative peak at donation count. This does not appear to carry over to the relationship modeled as the importance for donation count is the weakest. The strongest here is donation conversion, which is still in the single digit percentages. Not very inspiring.

# Individual registration enabled

Correlation to registration count: 0.006384
Correlation to registration amount: 0.000548
Correlation to donation count: 0.106651
Correlation to donation amount: 0.078250
Feature importance to donation count: 0.0861925404332
Feature importance to donation conversion: 0.0480758220137

| value |  count |
|-------|--------| 
|  1    | 202906 |
|  0    |  64875 |
|  5    |    315 |

Yet another pretty severe class imbalance here, still can't meaningfully interpret the information.

## Rebalancing

After rebalancing, definitely seeing changes but nothing astonishing.

Correlations to allows individual registration:

|       column        | correlation |
|---------------------|-------------|
| registration count  |  0.006806   |
| registration amount |  0.000478   |
| donation volume     |  0.079857   |
| donation count      |  0.111167   |
| reg conversion      |  0.000067   |
| don conversion      |  0.072403   |

Feature importances from random forest:

|       column        |   importance  |
|---------------------|---------------|
| registration count  | 0.03409156853 |
| registration amount | 0.04224474667 |
| donation volume     | 0.01512378536 |
| donation count      | 0.04717260189 |
| reg conversion      | 0.04243875151 |
| don conversion      | 0.07390540616 |

_All random forest models used the same feature set so this should be a fair indication of the role played in each target by the individual registration setting._ The strongest importance here is donation count and donation conversion. In the case of donation count, it aligns well with the correlations. It is worth noting that while these values, the correlations and importances, are objectively low, they are typical of those seen across the board for all features in the P2P models.


# Social enabled

| value | count  |
|-------|--------|
|   0   | 268066 |
|   1   |     30 |

The class imbalance here makes any interpretation of the results absolutely meaningless.

Correlation to registration count: 0.002530
Correlation to registration amount: 0.000887
Correlation to donation count: 0.002433
Correlation to donation amount: 0.002165
Feature importance to donation count: 
Feature importance to registration count: 0.00101219520463

__My guess here is that the real information I'm looking for in this feature is going to be found in the social post tracking information that is missing from my dataset rather than in the activation setting anyway.__

__Share TFP & PFP, and most other similar settings are similarly severely imbalanced that it is not possible to draw any conclusions from their outcomes.__

__Notebooks__
[Rebalanced modeling - individual registrations & teams](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/rebalanced%20modeling%20-%20individual%20registrations%20and%20teams.ipynb)
[data exploration](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/data%20exploration.ipynb)
[exploration](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/exploration.md)