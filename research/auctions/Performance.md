# Summary

__Confirmed Recommendations__

1. Bid increments are shown to increase winning bid values. It is recommended that bid increments be no less than 10% of the value or $5, whichever is greater.
2. Reserves can be demonstrated to increase winning bid values but we cannot statistically determine an optimal percentage of the item value. We can only recommend utilizing reserves at this time.

# 0 Prep

## Objectives 

Auction item performance
- before/after, sort of recommendations for aution item listing
- suggest bidding increment based on starting price
- performance score after auction (high activity, high ending price vs starting price, large delta between value and winning bid)
- account for traffic and engagement levels (low traffic/engagement auctions shouldn't punish items)
- compelling reason to force the user to enter item value prior to starting price?

## Process

- need to qualify successful vs unsuccessful auctions and/or items
    - start with score objective in order to easily identify
    - performance needs to be tuned to traffic
- identify settings to be recommended
    - starting price vs value
    - bidding increment
    
## Sources

- auctionitem: bid increment, value, reserve
- bidders: bids
- transauction: purchase price

## Data

Number of items: 23,792
Items value > $0: 18,004
Items price > value: 9,375
Items w/ > 1 bidders (considering anonymous): 560
Items w/ > 1 bids: 19,241
Items w/ value > $0 and > 1 bidders: 14,664

__Restrict data to (1) items with value > \$0 and (2) > 1 bids.__ This will elliminate items that can't be compared to a base value of the item being auctioned and those that failed to gain real engagement.

# 1 Score

## objective 

performance score after auction (high activity, high ending price vs starting price, large delta between value and winning bid)

## analysis

look at price over value and bid increments as ratio of value

### price/value ratio

_outperformers_ are quantified as items with winning bids greater than their values; _underperformers_ are quantified as items with winning bids equal to or less than their value

3,334 (22.7%) outperformers
11,330 (77.3%) underperformers

Outperformers
- Mean price ratio: 12.39
- Median price ratio: 1.29
- Mean bid increment ratio: 0.81
- Median bid increment ratio: 0.10
Underperformers
- Mean price ratio: 0.62
- Median price ratio: 0.62
- Mean bid increment ratio: 0.07
- Median bid increment ratio: 0.06

Price/value ratio sample sizes

| Price/value |   All items   | Outperformers | Underperformers |
|-------------|---------------|---------------|-----------------|
| 0.0 to 0.25 |   602 (4.1%)  |         0     |         602     |
| 0.25 to 0.5 | 2,519 (17.2%) |         0     |       2,519     |
| 0.5 to 0.75 | 4,453 (30.4%) |         0     |       4,453     |
| 0.75 to 1.0 | 3,054 (20.8%) |         0     |       3,054     |
| 1.0 to 1.25 | 2,165 (14.8%) |     1,463     |           0     |
| 1.25 to 1.5 |   749 (5.1%)  |       749     |           0     |
| 1.5 to 2.0  |   627 (4.3%)  |       627     |           0     |
| 2.0 to 5.0  |   396 (2.7%)  |       396     |           0     |
| 5.0 to 10.0 |    55 (0.4%)  |        55     |           0     |
| 10.0+       |    44 (0.3%)  |        44     |           0     |

### engagement - bid activity

All bids
- Median: 7.00
- Mean: 32.69
Outperformers bids
- Median: 11.00
- Mean: 34.42
Underperformers bids
- Median: 6.00
- Mean: 32.18

Bids sample sizes

|  Bids range | Outperformers | Underperformers |
|-------------|---------------|-----------------|
| (0, 3)      |   158 (4.7%)  |   1,828 (16.1%) |
| (3, 6)      |   356 (10.7%) |   3,774 (33.3%) |
| (6, 9)      |   627 (18.8%) |   2,399 (21.2%) |
| (9, 12)     |   643 (19.3%) |   1,235 (10.9%) |
| (12, 15)    |   452 (13.6%) |     718 (6.3%)  |
| (15, 20)    |   464 (13.9%) |     565 (5.0%)  |
| (20, 30)    |   366 (11.0%) |     473 (4.2%)  |
| 30+         |   268 (8.0%)  |     338 (3.0%)  |

[](01.01)

outperformers clearly have a tendency toward greater engagement, peaking in the 6 to 9 group. underperformers however peak in the 3 to 6 group with the 0 to 3 group extremely close behind. causation cannot be immediately discerned here, however, as we would naturally expect greater engagement to result in greater bid values and push an item into the outperformer category.

engagement could be a good metric for determining performance but we need to determine qualities of the item that prove influential in engagement.

### performance consistency

looking at average overperformer/underperformer ranks per form. is a form generally one or the other for all auction items or is it random?

|        | outperformer | underperformer |
|--------|--------------|----------------|
| mean   |     20.37%   |      79.63%    |
| median |     14.29%   |      85.71%    |

Forms w/ > 50% outperforming items

|        | outperformer | underperformer |
|--------|--------------|----------------|
| mean   |     74.79%   |      25.21%    |
| median |     69.23%   |      30.77%    |

Forms w/ > 50% underperforming items

|        | outperformer | underperformer |
|--------|--------------|----------------|
| mean   |     14.62%   |      85.38%    |
| median |     12.50%   |      87.50%    |

Item performance does appear to be rather consistent with underperforming items, but the outperforming items appears more random

### reserve

2,110 (14.39%) items w/ a reserve

| has reserve |  outperformer  | underperformer |
|             |  mean | median |  mean | median |
|-------------|-------|--------|-------|--------|
|    False    | 21.46 |  0.0   | 78.54 |   1.0  |
|    True     | 30.33 |  0.0   | 69.67 |   1.0  |

__the incidence of outperformers is greater among itmes with a reserve__

reserve/value ratio (0.0, 0.25):
- sample size: 214
- op: mean 0.24; median 0.00
- up: mean 0.76; median 1.00
- price_ratio: mean 0.64; median 0.50
reserve/value ratio (0.25, 0.5):
- sample size: 1,022
- op: mean 0.18; median 0.00
- up: mean 0.82; median 1.00
- price_ratio: mean 0.76; median 0.67
reserve/value ratio (0.5, 0.75):
- sample size: 539
- op: mean 0.38; median 0.00
- up: mean 0.62; median 1.00
- price_ratio: mean 0.96; median 0.87
reserve/value ratio (0.75, 1.0):
- sample size: 264
- op: mean 0.52; median 1.00
- up: mean 0.48; median 0.00
- price_ratio: mean 1.23; median 1.04

The reserve ratio performance appears to track closely with with the reserve itself. Ie, the median item performance in each reserve ratio segment is very close to a slight gain above the average reserve ratio for the given segment. This is an unsurprising result and does not lead to a conclusion of an ideal reserve ratio.

value (0, 25): 732 items
- p/v: mean 47.95; median 1.00
- p/v w/ reserve: mean 248.90; median 1.10
- p/v w/out reserve: mean 3.33; median 1.00
- mean diff w/ reserve: mean 7,371.22%; median 10.00%
value (25, 50): 1,983 items
- p/v: mean 1.10; median 0.90
- p/v w/ reserve: mean 1.06; median 1.00
- p/v w/out reserve: mean 1.10; median 0.90
- mean diff w/ reserve: mean -3.81%; median 11.11%
value (50, 100): 3,480 items
- p/v: mean 0.91; median 0.80
- p/v w/ reserve: mean 0.99; median 0.85
- p/v w/out reserve: mean 0.90; median 0.80
- mean diff w/ reserve: mean 10.69%; median 5.77%
value (100, 150): 2,034 items
- p/v: mean 0.78; median 0.72
- p/v w/ reserve: mean 0.82; median 0.73
- p/v w/out reserve: mean 0.77; median 0.71
- mean diff w/ reserve: mean 6.87%; median 2.67%
value (150, 250): 2,402 items
- p/v: mean 0.74; median 0.66
- p/v w/ reserve: mean 0.80; median 0.70
- p/v w/out reserve: mean 0.72; median 0.65
- mean diff w/ reserve: mean 10.74%; median 7.69%
value (250, 500): 2,301 items
- p/v: mean 0.68; median 0.61
- p/v w/ reserve: mean 0.83; median 0.69
- p/v w/out reserve: mean 0.65; median 0.60
- mean diff w/ reserve: mean 26.84%; median 15.65%
value 500: 1,732 items
- p/v: mean 1.75; median 0.57
- p/v w/ reserve: mean 0.81; median 0.69
- p/v w/out reserve: mean 2.03; median 0.53
- mean diff w/ reserve: mean -59.80%; median 30.61%

Mean diff means: 1,051.82%
Mean diff medians: 11.93%

There is a consistent advantage to implementing a reserve with an auction item. There are outliers dragging the mean's into unreasonable values but examining the median's shows a clear advantage with an average gain of 12% throughout all values segments for items with a reserve value with more pronounced effects with high value items ($250+).

# 2 bid increment

## objective

evaluate bid increment relative to item auction performance to try to find an optimal value to recommend to users

## analysis

we will start by examining bid increments as a ratio or percentage of the item value

3,334 (22.7%) outperformers
11,330 (77.3%) underperformers

### bid increment ratio

looking at the bid increment/value ratio or percentage of item value

All bid increment ratio sample sizes
(0.0, 0.025): 1,868 auction items; median price/value: 0.54
(0.025, 0.05): 2,876 auction items; median price/value: 0.60
(0.05, 0.075): 3,591 auction items; median price/value: 0.70
(0.075, 0.1): 1,771 auction items; median price/value: 0.77
(0.1, 0.15): 3,412 auction items; median price/value: 0.88
(0.15, 0.2): 448 auction items; median price/value: 0.94
(0.2, 0.5): 618 auction items; median price/value: 1.01
(0.5, 0.75): 8 auction items; median price/value: 3.00
0.75: 72 auction items; median price/value: 7.50

Outperformers bid increment ratio sample sizes
(0.0, 0.025): 210 auction items; median price/value: 1.22
(0.025, 0.05): 305 auction items; median price/value: 1.24
(0.05, 0.075): 672 auction items; median price/value: 1.22
(0.075, 0.1): 455 auction items; median price/value: 1.23
(0.1, 0.15): 1,135 auction items; median price/value: 1.30
(0.15, 0.2): 173 auction items; median price/value: 1.33
(0.2, 0.5): 309 auction items; median price/value: 1.40
(0.5, 0.75): 6 auction items; median price/value: 3.40
0.75: 69 auction items; median price/value: 8.00

Underperformers bid increment ratio sample sizes
(0.0, 0.025): 1,658 auction items; median price/value: 0.50
(0.025, 0.05): 2,571 auction items; median price/value: 0.56
(0.05, 0.075): 2,919 auction items; median price/value: 0.62
(0.075, 0.1): 1,316 auction items; median price/value: 0.67
(0.1, 0.15): 2,277 auction items; median price/value: 0.70
(0.15, 0.2): 275 auction items; median price/value: 0.75
(0.2, 0.5): 309 auction items; median price/value: 0.80
(0.5, 0.75): 2 auction items; median price/value: 1.00
0.75: 3 auction items; median price/value: 0.00

[](02.01)

charting raw counts. earlier peaks in the underperformers is clearly indicating that underperformers tend to use smaller bid increments relative the item value.

in order to more easily see the difference, we will normalize the sample sizes to see them in equal dimension.

[](02.02)

normalized, it is clear to see that underperforming auction items have a tendency toward bid increments of 2.5% to 5% of the item value whereas the outperforming auction items have a tendency toward bid increments of 7.5% to 10% of the item value

__this is a good stat for a recommendation__

looking at all auction items, the median price/value ratio increases with an increase in the bid increment/value consistently

(0.0, 0.025)
         index  price_ratio
3  (0.0, 0.25]          276
0  (0.25, 0.5]          556
1  (0.5, 0.75]          516
2  (0.75, 1.0]          294
4  (1.0, 1.25]          117
5  (1.25, 1.5]           38
6   (1.5, 2.0]           28
7   (2.0, 5.0]           22
8  (5.0, 10.0]            1

(0.025, 0.05)
         index  price_ratio
3  (0.0, 0.25]          181
1  (0.25, 0.5]          874
0  (0.5, 0.75]          915
2  (0.75, 1.0]          585
4  (1.0, 1.25]          163
5  (1.25, 1.5]           76
6   (1.5, 2.0]           40
7   (2.0, 5.0]           25
8  (5.0, 10.0]            1

(0.05, 0.075)
         index  price_ratio
6  (0.0, 0.25]           81
2  (0.25, 0.5]          765
0  (0.5, 0.75]         1202
1  (0.75, 1.0]          860
3  (1.0, 1.25]          360
4  (1.25, 1.5]          154
5   (1.5, 2.0]           96
7   (2.0, 5.0]           59
8  (5.0, 10.0]            3

(0.075, 0.1)
         index  price_ratio
7  (0.0, 0.25]           13
2  (0.25, 0.5]          278
0  (0.5, 0.75]          551
1  (0.75, 1.0]          467
3  (1.0, 1.25]          258
4  (1.25, 1.5]           94
5   (1.5, 2.0]           78
6   (2.0, 5.0]           24
8  (5.0, 10.0]            1

(0.1, 0.15)
         index  price_ratio
7  (0.0, 0.25]           15
3  (0.25, 0.5]          396
1  (0.5, 0.75]          874
0  (0.75, 1.0]          974
2  (1.0, 1.25]          500
4  (1.25, 1.5]          308
5   (1.5, 2.0]          195
6   (2.0, 5.0]          120
8  (5.0, 10.0]            8

(0.15, 0.2)
         index  price_ratio
8  (0.0, 0.25]            3
4  (0.25, 0.5]           42
1  (0.5, 0.75]           92
0  (0.75, 1.0]          136
2  (1.0, 1.25]           72
3  (1.25, 1.5]           57
6   (1.5, 2.0]           18
5   (2.0, 5.0]           20
7  (5.0, 10.0]            6

(0.2, 0.5)
         index  price_ratio
7  (0.0, 0.25]            5
6  (0.25, 0.5]           31
2  (0.5, 0.75]           75
0  (0.75, 1.0]          196
1  (1.0, 1.25]          114
3  (1.25, 1.5]           74
4   (1.5, 2.0]           61
5   (2.0, 5.0]           56
8  (5.0, 10.0]            4

(0.5, 0.75)
         index  price_ratio
3  (0.0, 0.25]            0
4  (0.25, 0.5]            0
5  (0.5, 0.75]            0
1  (0.75, 1.0]            2
6  (1.0, 1.25]            0
7  (1.25, 1.5]            0
2   (1.5, 2.0]            1
0   (2.0, 5.0]            3
8  (5.0, 10.0]            0

0.75
         index  price_ratio
2  (0.0, 0.25]            1
4  (0.25, 0.5]            0
5  (0.5, 0.75]            0
6  (0.75, 1.0]            0
7  (1.0, 1.25]            0
8  (1.25, 1.5]            0
3   (1.5, 2.0]            1
0   (2.0, 5.0]           23
1  (5.0, 10.0]           19

there is a consistent intersection of peaking price/value ratio samples around 0.75 to 1.25 bid increment/value ratios. we still see a strong positive correlation between the two metrics but pushing greater bid increment/value ratios could have unforeseen negative effects if recommended universally. _a safe course of action would be to recommend a 10% bid increment/value ratio while never recommending to decrease the bid increment in cases that users feel greater values are desirable. over time, as this recommendation is applied, we will see a new floor develop at 10% and we can reassess with larger sample sizes._

## bid increment value

looking at the absolute value of bid increment (ie, $1, $5, etc.)

### price/value ratio

All bid increment sample sizes
(0.0, 1.0): 577 auction items; median price/value: 0.71
(1.0, 2.5): 786 auction items; median price/value: 0.76
(2.5, 5.0): 387 auction items; median price/value: 0.80
(5.0, 7.5): 4,669 auction items; median price/value: 0.76
(7.5, 10.0): 70 auction items; median price/value: 0.80
(10.0, 15.0): 4,345 auction items; median price/value: 0.72
(15.0, 25.0): 1,389 auction items; median price/value: 0.69
(25.0, 50.0): 1,414 auction items; median price/value: 0.68
(50.0, 100.0): 665 auction items; median price/value: 0.67
100.0: 362 auction items; median price/value: 0.70

Underperformers bid increment sample sizes
(0.0, 1.0): 440 auction items; median price/value: 0.60
(1.0, 2.5): 574 auction items; median price/value: 0.63
(2.5, 5.0): 275 auction items; median price/value: 0.65
(5.0, 7.5): 3,496 auction items; median price/value: 0.65
(7.5, 10.0): 56 auction items; median price/value: 0.73
(10.0, 15.0): 3,411 auction items; median price/value: 0.63
(15.0, 25.0): 1,140 auction items; median price/value: 0.62
(25.0, 50.0): 1,142 auction items; median price/value: 0.60
(50.0, 100.0): 533 auction items; median price/value: 0.60
100.0: 263 auction items; median price/value: 0.55

Outperformers bid increment sample sizes
(0.0, 1.0): 137 auction items; median price/value: 1.25
(1.0, 2.5): 212 auction items; median price/value: 1.30
(2.5, 5.0): 112 auction items; median price/value: 1.30
(5.0, 7.5): 1,173 auction items; median price/value: 1.30
(7.5, 10.0): 14 auction items; median price/value: 1.41
(10.0, 15.0): 934 auction items; median price/value: 1.25
(15.0, 25.0): 249 auction items; median price/value: 1.25
(25.0, 50.0): 272 auction items; median price/value: 1.31
(50.0, 100.0): 132 auction items; median price/value: 1.40
100.0: 99 auction items; median price/value: 1.55

among the underperformers, price/value ratios appear to be random across all bid increment values. on the other hand, it does appear that among the outperformers a greater bid increment value will drive a greater price/value ratio. 

while this relationship does sppear consistent among the outperformers, i imagine that bid increment value needs to be largely dependent upon the auction item value. for instance, while statistically it does appear that 100 bid increments will drive the greatest price/value ratio, it may not be acceptable to auction bidders for an item worth less than 100.

### number of bids

All bid increment sample sizes
(0.0, 1.0): 577 auction items; median bids: 11.00
(1.0, 2.5): 786 auction items; median bids: 10.00
(2.5, 5.0): 387 auction items; median bids: 6.00
(5.0, 7.5): 4,669 auction items; median bids: 7.00
(7.5, 10.0): 70 auction items; median bids: 6.00
(10.0, 15.0): 4,345 auction items; median bids: 6.00
(15.0, 25.0): 1,389 auction items; median bids: 6.00
(25.0, 50.0): 1,414 auction items; median bids: 6.00
(50.0, 100.0): 665 auction items; median bids: 6.00
100.0: 362 auction items; median bids: 7.00

Underperformers bid increment sample sizes
(0.0, 1.0): 440 auction items; median bids: 11.00
(1.0, 2.5): 574 auction items; median bids: 8.00
(2.5, 5.0): 275 auction items; median bids: 5.00
(5.0, 7.5): 3,496 auction items; median bids: 6.00
(7.5, 10.0): 56 auction items; median bids: 6.00
(10.0, 15.0): 3,411 auction items; median bids: 5.00
(15.0, 25.0): 1,140 auction items; median bids: 5.00
(25.0, 50.0): 1,142 auction items; median bids: 5.00
(50.0, 100.0): 533 auction items; median bids: 5.00
100.0: 263 auction items; median bids: 5.00

Outperformers bid increment sample sizes
(0.0, 1.0): 137 auction items; median bids: 15.00
(1.0, 2.5): 212 auction items; median bids: 16.00
(2.5, 5.0): 112 auction items; median bids: 9.00
(5.0, 7.5): 1,173 auction items; median bids: 11.00
(7.5, 10.0): 14 auction items; median bids: 13.00
(10.0, 15.0): 934 auction items; median bids: 10.00
(15.0, 25.0): 249 auction items; median bids: 10.00
(25.0, 50.0): 272 auction items; median bids: 11.00
(50.0, 100.0): 132 auction items; median bids: 10.00
100.0: 99 auction items; median bids: 14.00

__lower bid increments will drive more bids, but it levels out fairly quickly beyond 2__. Given the choice between 2 and 5, the average number of bids will have to be 2.5 times greater than the higher bid count in order to drive the same transaction amount. the numbers do not bear this out. in the underperformers, the greater bid increment values are about half that of the lower values and the outperformers are about 2/3.

# 3 traffic

## objective

explore influence of traffic, relation to performance of auctions. does item performance change with traffic differences? can we disqualify certain auctions from the data due to low/inadequate traffic?

## analysis

Median form page views:
Outperformers: 86.0
Underperformers: 32.0

Underperformers are seeing nearly a third of the traffic of the overperformers, which could explain the lack of fundraising as a function of attention. The bid increment/item value ratios hold fairly consistently in both groups so the correlation is clearly present. 

We will attempt to calculate a traffic adjusted bidding performance rank in order to account for this difference.

outperformer
False    0.125000
True     0.178571

Outperformers do indeed receive more bids per page view than underperformers. So traffic alone is to not accountable for the differences.

Correlations

| outperformer |              | price ratio | views stayed |
|--------------|--------------|-------------|--------------|
| False        | price ratio  |    100%     |     1.62%    |
|              | views stayed |    1.62%    |     100%     |
| True         | price ratio  |    100%     |    -3.18%    |
|              | views stayed |   -3.18%    |     100%     |

The correlation between traffic and winning bid/value ratio is very weak in both groups, so it is clear that traffic is not a strong factor of maximizing winning bid

Views stayed sample sizes

views_stayed
(0, 10]           1081
(10, 25]          1256
(25, 50]           881
(50, 100]          943
(100, 500]         704
(500, 1000]         10
(1000, 2500]       289
(2500, 5000]       645
(5000, 7500]       186
(7500, 10000]      222
(10000, 20000]     120
(20000, 30000]     337

Medians

|  views_stayed  | outperformer | price_ratio | bids |
|----------------|--------------|-------------|------|
| (0, 10]        |     0.0      |  0.720000   |  8.0 |
| (10, 25]       |     0.0      |  0.750000   |  7.0 |
| (25, 50]       |     0.0      |  0.700000   |  7.0 |
| (50, 100]      |     0.0      |  0.760000   |  7.0 |
| (100, 500]     |     0.0      |  0.740370   |  7.0 |
| (500, 1000]    |     0.0      |  0.775000   |  2.5 |
| (1000, 2500]   |     0.0      |  0.714286   |  7.0 |
| (2500, 5000]   |     0.0      |  0.700000   |  7.0 |
| (5000, 7500]   |     0.0      |  1.000000   |  4.0 |
| (7500, 10000]  |     0.0      |  0.640000   |  6.0 |
| (10000, 20000] |     0.0      |  0.732143   |  7.0 |
| (20000, 30000] |     0.0      |  0.700000   |  4.0 |

Means

|  views_stayed  | outperformer | price_ratio |   bids   |
|----------------|--------------|-------------|----------|
| (0, 10]        |   0.195190   |  2.646740   | 52.09343 | 
| (10, 25]       |   0.259554   |  1.041826   | 8.763535 |
| (25, 50]       |   0.160045   |  0.733357   | 9.860386 |
| (50, 100]      |   0.249205   |  36.232965  | 10.31071 |
| (100, 500]     |   0.294034   |  1.252121   | 9.126420 |
| (500, 1000]    |   0.200000   |  0.877254   | 463.9000 | 
| (1000, 2500]   |   0.304498   |  0.953103   | 75.32179 |
| (2500, 5000]   |   0.209302   |  0.785453   | 8.285271 |
| (5000, 7500]   |   0.456989   |  2.864416   | 6.795699 |
| (7500, 10000]  |   0.171171   |  0.703837   | 8.500000 |
| (10000, 20000] |   0.166667   |  0.767543   | 9.700000 |
| (20000, 30000] |   0.136499   |  0.741968   | 4.421365 |

Grouping by traffic, we can see that outperform/underperform and price/value ratios are evenly distributed while the bids counts very much appear random. These bins are fairly evenly accounting for representation in the sample sets so it appears to either have no or very weak influence over other features beyond extremes.

# 4 item count

## objective

determine if number of items in a given auction influences the amount of bidding. could this skew bidding attention to weaken what would otherwise be successful auction items?

## analysis

| outperformer | count |  mean | median |
|--------------|-------|-------|--------|
|     0.0      |  433  | 38.77 |  29.0  |
|     0.5      |    4  | 28.00 |  25.0  |
|     1.0      |   31  | 35.64 |  22.0  |


The sample sizes are rather small here but the data is not so differentiated as to lead me to believe that this will be going somewhere important.

(0.0, 0.1): samples: 204, items: mean 50.42, median 50.16
(0.1, 0.2): samples: 108, items: mean 63.24, median 62.67
(0.2, 0.3): samples: 66, items: mean 61.22, median 61.01
(0.3, 0.4): samples: 37, items: mean 58.36, median 57.85
(0.4, 0.5): samples: 18, items: mean 62.50, median 62.14
(0.5, 0.6): samples: 12, items: mean 50.56, median 50.19
(0.6, 0.7): samples: 9, items: mean 57.75, median 57.58
(0.7, 0.8): samples: 2, items: mean 33.00, median 33.00
(0.8, 0.9): samples: 3, items: mean 63.33, median 63.33
(0.9, 1.0): samples: 9, items: mean 21.19, median 19.50