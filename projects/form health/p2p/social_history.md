# Overview

This data is drawn from the automated social posting history record. Data was also brought in from a variety of other sources to establish relationships between these automated posts and other system factors and metrics.

The date times appear to be evenly distributed with nothing in particular standing out. There's a lull in the middle of the night as would be expected. There's roughly a 30% reduction in activity over the weekend, which mirrors general activity within the system seen in other system logs. The activity appears to be quite evenly distributed throughout the month. **Might be worth the effort of timing prompts to participants to post around peak conversion times at the beginning and middle of the months (payday).**

# How does it relate to fundraising?

The social posters definitely raise more money. Mean funds raised by posters $424.38 vs nonposters at $219.03, but this metric may be misleading given that only 9.8% of the registrants are posters.

# How does it relate to other registrant data points?

Participants who had an automated social post: 9.8%.

Bucketed counts:

| posts count | # participants | % participants |
|-------------|----------------|----------------|
| (0, 1]      |    1768        |      39.39     |
| (1, 2]      |     412        |      27.8      |
| (2, 3]      |     151        |      12.34     |
| (3, 5]      |      97        |      11.6      |
| (5, 8]      |      69        |       6.5      |
| (8, 10]     |      36        |       1.12     |
| (10, 15]    |      31        |       1.0      |
| (15, 20]    |      13        |       0.22     |

Correlations between social posts & funds raised is very weak at 0.032, and is still weak when isolating to posts > 0 at .09. The data is very much all over the place.

![social_posts_count_to_funds_raised.png](../../resources/social_posts_count_to_funds_raised.png)

Correlation between social posts and badges however proves to be quite strong, and is yet another indicator that badges is a solid metric for overall participant performance.

![social_posts_count_to_badges.png](../../resources/social_posts_count_to_badges.png)

| badge count | posts count | welcomequest count | amount      |
|-------------|-------------|--------------------|-------------|
| (0, 1]      | 0.156767    | 1.781013           | 253.861047  |
| (1, 2]      | 0.225513    | 1.904779           | 201.520672  |
| (2, 3]      | 0.356863    | 2.191721           | 329.371137  |
| (3, 5]      | 0.420557    | 2.388616           | 406.804378  |
| (5, 8]      | 0.546584    | 2.761646           | 566.266545  |
| (8, 10]     | 0.594595    | 3.279279           | 976.914459  |
| (10, 15]    | 0.552764    | 3.211055           | 1091.153216 |
| (15, 20]    | 0.840909    | 3.272727           | 1204.627955 |
