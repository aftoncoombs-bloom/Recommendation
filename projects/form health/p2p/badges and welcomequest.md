# Correlations

| feature      | corr to welcome quest | corr to badges |
| ------------ | --------------------- | -------------- |
| amount_mean  | 0.006                 | 0.001          |
| amount_count | 0.353                 | 0.019          |
| amount_sum   | 0.231                 | 0.011          |
| pcnt_raised  | 0.157                 | 0.012          |

# Welcome quest

The most obvious point of interest here is how do registrants who complete the welcome quest steps perform in comparison to those who do not.

## By steps completed

Donation averages grouped by welcome steps completed:

| steps completed | mean sum | mean count | mean percent of total event funds raised |
| --------------- | -------- | ---------- | ---------------------------------------- |
| 0               | 148.775  | 1.539      | 0.018                                    |
| 1               | 126.577  | 1.764      | 0.012                                    |
| 2               | 226.512  | 3.127      | 0.021                                    |
| 3               | 475.501  | 5.753      | 0.037                                    |
| 4               | 522.409  | 6.676      | 0.039                                    |
| 5               | 580.113  | 7.727      | 0.053                                    |
| 6               | 525.519  | 7.826      | 0.041                                    |
|                 |          |            |                                          |

_The observation count for each of these was significant except for 7, which after all of the filters this passed through the resulting observation count was 2 so these were omitted._

At this point, it cannot be said that completing the welcome quest results in greater funds raised as the causation cannot be determined. We do not know if the successful users are successful due in some way to completing the welcome quest, or if they are completing the welcome quest because they are high performers. 

## By how long it took to complete the steps

Looking at the time it takes to complete the welcome may give us some insight into this. My advance assumption would be that users who take a long time to complete welcome quest steps are doing so nonpurposefully in the process of engaging with the event, whereas users that complete the welcome quest quickly are doing so as a result of a specific desire to accomplish these steps.

Looking at the average time between accomplishing steps, we get the following:

| task           | mean time difference   | std time difference     |
| -------------- | ---------------------- | ----------------------- |
| time_to_step_2 | 6 days 05:00:58.911868 | 20 days 18:30:14.149986 |
| time_to_step_3 | 7 days 01:04:54.346459 | 22 days 21:51:14.726604 |
| time_to_step_4 | 6 days 20:07:38.041972 | 17 days 23:23:45.318451 |
| time_to_step_5 | 8 days 05:38:02.512310 | 19 days 18:18:36.346963 |
| time_to_step_6 | 9 days 07:21:14.348684 | 17 days 15:29:23.563463 |

Looking at these grouped by time difference:

Average value for total time to completion of any number of steps: 117 hours (nearly 5 days)

| Steps completed |          total | under 6 hours | under 12 hours | under 24 hours |
| --------------: | -------------: | ------------: | -------------: | -------------: |
|          0 or 1 | 29494 (60.84%) |               |                |                |
|               2 | 18983 (39.16%) |          7345 |           7798 |           8791 |
|               3 |  9548 (19.70%) |          2687 |           2955 |           3513 |
|               4 |   4503 (9.29%) |          1073 |           1191 |           1452 |
|               5 |   1909 (3.94%) |           387 |            438 |            552 |
|               6 |    456 (0.94%) |            64 |             79 |            105 |

It does appear that in every subset, 20% to 40% of the users are completing whatever number of steps they're going to accomplish within 24 hours. Based upon the correlation between completing steps in the welcome quest and funds raised, there doesn't appear to be a critical time for completing the welcome quest but still need to look at whether completing these quickly correlates to funds raised as opposed to just completing them _at any point during the event_.


| welcomequest_under_24 | amount_mean | amount_count | pcnt_raised | amount_sum |
| --------------------- | ----------- | ------------ | ----------- | ---------- |
| False                 | 80.914      | 4.970        | 0.032       | 403.294    |
| True                  | 75.722      | 2.423        | 0.016       | 172.796    |

| welcomequest_under_48 | amount_mean | amount_count | pcnt_raised | amount_sum |
| --------------------- | ----------- | ------------ | ----------- | ---------- |
| False                 | 81.794      | 4.899        | 0.031       | 401.946    |
| True                  | 75.575      | 2.525        | 0.017       | 180.304    |

| welcomequest_under_72 | amount_mean | amount_count | pcnt_raised | amount_sum |
| --------------------- | ----------- | ------------ | ----------- | ---------- |
| False                 | 82.255      | 4.798        | 0.031       | 397.893    |
| True                  | 75.557      | 2.607        | 0.018       | 186.189    |

| welcomequest_under_week | amount_mean | amount_count | pcnt_raised | amount_sum |
| ----------------------- | ----------- | ------------ | ----------- | ---------- |
| False                   | 82.956      | 4.662        | 0.030       | 390.452    |
| True                    | 75.744      | 2.758        | 0.019       | 199.430    |

It definitely looks here like it doesn't matter at all whether or not the welcome quest is completed quickly. In fact, given the mean time taken to accomplish whatever steps will be completed is just shy of 5 days and we can see that the averages still have not tipped in favor of the time count up to a week, it very much looks like the majority of the imapctful fundraising is being done by those who take a long time to complete the welcome quest. 

The hypothesis that those who complete the welcome quest quickly are those doing so deliberately and those who take a long time are those who do so as a consequence of being otherwise engaged may be wrong, but either way it is certain that completing the welcome quest quickly does not lead to greater fundraising. Given the correlation between completing the welcome quest steps and greater fundraising, it may be said that monitoring the welcome quest completion rates would serve as a meaningful indicator of engagement and prediction of the performance of a given registrant.

# Badges

First note is that badge awards are not nearly as common as I would have assumed coming into this.

| badges range | form count |
|--------------|------------|
| (0, 10]      |    244     |
| (10, 25]     |    118     |
| (25, 100]    |    292     |
| (100, 250]   |    167     |
| (250, 500]   |     44     |
| (500, 4000]  |     26     |

As we can see, the vast majority have fewer than 100 badges awarded.

| badges per reg | form count |
|----------------|------------|
| (0.0, 0.5]     |      69    |
| (0.5, 1.0]     |     106    |
| (1.0, 2.0]     |     164    |
| (2.0, 3.0]     |     107    |
| (3.0, 4.0]     |      58    |
| (4.0, 5.0]     |      22    |
| (5.0, 10.0]    |      58    |

Most forms do appear to be awarding more than one badge per registrant. If gamifying the event system is indeed our goal, the client organizations do appear to be doing a decent job of this by not making it too difficult to earn some reward for desired behavior. I'm certain some of these are distributed unequally, with individual users earning several badges and others earning 1 or 0, but so long as the average ratio is greater than 1 per participant, it is probably in a good place.

## How do badges relate to funds raised?


| badges range | mean amount | mean count | mean percent | mean sum | % observations |
| ------------ | ----------- | ---------- | ------------ | -------- | -------------- |
| (0, 1]       | 85.811      | 3.226      | 0.015        | 253.861  | 26.63%         |
| (1, 3]       | 87.374      | 3.041      | 0.024        | 239.148  | 26.64%         |
| (3, 5]       | 95.591      | 5.312      | 0.042        | 406.804  | 8.34%          |
| (5, 7]       | 97.135      | 6.110      | 0.051        | 500.658  | 3.59%          |
| (7, 10]      | 95.646      | 10.289     | 0.086        | 914.207  | 1.57%          |
| (10, +]      | 85.226      | 9.566      | 0.073        | 901.207  |                |

_* observations greater than 10 badges are extremely sparse and exhibit a great deal of variance_

There is clearly a correlation between badge awards on an individual basis and funds raised. Here we can see that winning 5 to 7 badges correlates to doubling the mean sum of funds raised from no badges. This fundamentally makes sense as the best performers are going to be winning more badges. What cannot be determined here is the motivation. The best performers would obviously be earning the most badges, but we cannot say that they are earning more in an effort to win more badges.

## Does the timing of badge activity relate to transactions?

Examining the time distributions for the badges yielded little information. These assignments were sufficiently evenly distributed around fundraising that drawing any conclusion from the relationship between the badges and transactions would be impossible without further information such as social activity or emails sent out to act as a bridge between approaching a badge threshold or losing a badge and subsequent fundraising.

Information that might prove useful in further exploring this is general user activity logs such as login times, as well as the aforementioned outreach activities.

# Interpretation

Both welcome quest steps completed and badge activity show similar patterns in that there is an apparent threshold that must be crossed before any effect can be seen. A given user must earn more than 3 badges  or complete 2 or more welcome quest steps before their contributions begin to increase. This could be interpreted as an indication that these users are influenced by these systems but I do not believe this could be confidently claimed based upon the data examined here. 

What is clear, however, is that both badges and the welcome quest appear to be excellent metrics for engagement and could prove quite useful as a sort of runway for otherwise disengaged users just to get them started in the process. Completing the welcome quest steps may not necessarily motivate a user to raise more money but there is a clear relationship between greater funds raised and completing these steps.

---

Notebooks:

- [syslog exploration](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/syslog%20exploration.ipynb)