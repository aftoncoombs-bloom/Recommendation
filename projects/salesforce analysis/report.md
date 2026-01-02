# Summary

In general, there is a notable decrease in activity and time between losses and wins. Winners require far fewer calls, emails, and meetings than losers, and they transition to the next stage much faster. The composition of actions (ie, proportion of calls to emails or meetings) between winners and losers is not markedly different. Additionally, we can see that 72.87% of losses do not reach the stage of demo scheduled. Of those that will reach a given stage, a large proportion tend to reach it rather quickly. For instance, 93% of wins and 85% of losses that will complete a demo will do so in less than 1 week of initial contact.

Based upon the data reviewed, it seems clear to me that the type or amount of activity is not an influential factor in the sales process. The most likely influencing factors is (1) communications prior to entering the sales lifecycle and/or (2) the quality of the communication within the sales lifecycle. The strongest statistical observation of this dataset is that the greater the volume and frequency of the communication, the greater the likelihood of loss.

# Activity per stage of the sales life cycle

For this review, stages and activities were normalized to the following:

_Stages_:

- Initial contact
- Demo scheduled
- Demo completed
- Signup
- Onboarding
- Closed won
- Closed lost
- Unknown

_Activities_:

- call
- demo completed
- demo scheduled
- email
- initial contact
- interest shown
- lead qualification
- lead submitted form
- meeting
- none
- one pager campaign
- post-demo follow up
- pre-demo follow up
- prepared materials

## Activity per stage

Here we're seeing generally less of everything across the board losers to winners. It would seem that the winners take less effort and less time in order to complete each stage. I cannot account for cold calling/outbound being overly represented in the losses, which I am sure heavily influences these numbers.

### Losses

| Activity | Initial Contact | Demo Scheduled | Demo Completed | Signup | Closed Lost | Unknown |
|---|---|---|---|---|---|---|
| call | 10.431034 | 8.189655 | 59.568966 | 1.689655 | 4.327586 | 43.655172 |
| email |	28.741379 |	4.775862 |	44.448276 |	5.948276 |	3.948276 |	100.103448 |
| lead qualification |	0.068966 |	0.086207 |	0.344828 |	NaN |	0.017241 |	0.568966 |
| lead submitted form |	NaN |	NaN |	NaN |	NaN |	NaN |	0.965517 |
| meeting |	0.120690 |	0.017241 |	0.137931 |	NaN |	0.017241 |	0.896552 |
| not interested |	0.172414 |	NaN |	0.051724 |	NaN |	NaN |	0.017241 |

### Wins

| Activity | Initial Contact | Demo Scheduled | Demo Completed | Signup | Closed Lost | Closed Won | Unknown |
|---|---|---|---|---|---|---|---|
| call | 7.873016 | 2.253968 | 39.587302 | 3.873016 | 1.079365 | 0.126984 | 33.873016 |
| email | 20.666667 | 2.841270 | 43.523810 | 15.968254 | 1.539683 | 0.063492 | 86.238095 |
| lead qualification | 0.031746 | NaN | 0.079365 | NaN | NaN | NaN | 0.412698 |
| lead submitted form | NaN | NaN | NaN | NaN | NaN | NaN | 0.460317 |
| meeting | 0.111111 | 0.015873 | 0.126984 | 0.031746 | NaN | NaN | 0.634921 |
| not interested | NaN | NaN | NaN | NaN | NaN | NaN | 0.015873 |

## Time between stages

Below is the average time it takes to get to a given stage from the start for both wins and losses. Continuing the trend of activity per stage, the amount of time it takes to close a winner is much lower than for losses. 

For example, winning sales close on average 68% faster than losing sales.

### Close status average days per stage

We see here that the time taken for a winning sale to go from initial contact to demo scheduled is on average 2 days, and from demo scheduled to demo completed is on average 4.62. The standard deviations are rather skewed in this dataset and very steep. The numbers are the following:

- 90% of winning sales that will complete a demo have completed a demo within 2 days from initial contact
- 93% of winning sales that will complete a demo have completed a demo within 4 days from initial contact
- 85% of losing sales that will complete a demo have completed a demo within 2 days from initial contact
- 88% of losing sales that will complete a demo have completed a demo within 4 days from initial contact

_Caveats regarding bad data_:

- 0.8% Initial contact date is the same as demo scheduled date
- 3.0% Initial contact date is the same as demo completed date
- 0% Demo scheduled date is the same as demo completed date

### Average days between stages

| Close Status | Initial Contact to Demo Scheduled | Demo Scheduled to Demo Completed | Demo Completed to Signup | Signup to Onboarding | Initial Contact to Close |
|---|---|---|---|---|---|
| Lost | 2.69 | 15.21 | 23.91 | 15.0 | 88.05 |
| Unknown | 0.13 | 156.88 | 103.50 | NaN | NaN |
| Won | 2.07 | 4.62 | 29.82 | 5.50 | 32.70 |

### Standard deviation

| Close Status | Initial Contact to Demo Scheduled | Demo Scheduled to Demo Completed | Demo Completed to Signup | Signup to Onboarding | Initial Contact to Close |
|---|---|---|---|---|---|
| Lost | 32.00 | 73.66 | 48.08 | NaN | 107.58 |
| Unknown | 0.89 | 222.40 | 17.68 | NaN | NaN |
| Won | 17.49 | 20.46 | 53.53 | 9.52 | 55.99 |


### Losses

| Stage | Days from Start Losses | Count Losses |
|---|---|---|
| Closed Lost from Start | 88.0 | 2596 |
| Closed Won from Start | NaN | 0 |
| Demo Completed from Start | 13.0 | 2056 |
| Demo Scheduled from Start | 2.0 | 794 |
| Initial Contact from Start | 0.0 | 2750 |
| Onboarding from Start | 0.0 | 1 |
| Signup from Start | 9.0 | 93 |
| Start from Start | 0.0 | 2974 |

72.87% of losses do not reach the stage of demo scheduled.

The following shows the percentage of total losses that achieve a given stage:

| Stage | % |
|---|---|
| Demo Scheduled  |  27.13% |
| Demo Completed  |  20.52% |
| Signup          |   2.19% |
| Onboarding      |   0.03% |

### Wins

| Stage | Days from Start Wins | Count Wins |
|---|---|---|
| Closed Lost from Start | NaN | 0 |
| Closed Won from Start | 28.0 | 2853 |
| Demo Completed from Start | 7.0 | 1782 |
| Demo Scheduled from Start | 1.0 | 594 |
| Initial Contact from Start | 0.0 | 2731 |
| Onboarding from Start | 38.0 | 115 |
| Signup from Start | 18.0 | 1411 |
| Start from Start | 0.0 | 3231 |

### Combined

| Stage | Days from Start All | Count All | Days from Start Wins | Count Wins | Days from Start Losses | Count Losses |
|---| ---| ---| ---| ---|---| ---|
| Closed Lost from Start | 87 | 3163 | NaN | 0 | 88.0 | 2596 |
| Closed Won from Start | 28 | 3420 | 28.0 | 2853 | NaN | 0 |
| Demo Completed from Start | 9 | 3799 | 7.0 | 1782 | 13.0 | 2056 |
| Demo Scheduled from Start | 2 | 1453 | 1.0 | 594 | 2.0 | 794 |
| Initial Contact from Start | 0 | 5682 | 0.0 | 2731 | 0.0 | 2750 |
| Onboarding from Start | 40 | 123 | 38.0 | 115 | 0.0 | 1 |
| Signup from Start | 20 | 1668 | 18.0 | 1411 | 9.0 | 93 |
| Start from Start | 0 | 6394 | 0.0 | 3231 | 0.0 | 2974 |


# Win rate

| Status | Count |
|---|---|
| Lost    |   28936 |
| Won     |   23347 |
| Unknown  |   3760 |

## Global per person average

| State | Rate |
|---|---|
| Lost | 61.91% |
| Won  | 45.16% |

## Per person win rates

| Rep | username | % Won | % Lost | 
|---|---|---|---|
| 00531000006kRT2AAM | operations@qgiv.com | 40.51% | 59.49% |
| 00531000007YpsBAAS | chris.mauk@qgiv.com | 42.60% | 57.40% |
| 00531000007gwftAAA | chris.polizzi@qgiv.com | 44.74% | 55.26% |
| 00531000008TfLhAAK | jenny.kastancuk@qgiv.com | 47.05% | 52.95% |
| 0055A000006JxseQAC | cassandra.toner@qgiv.com | 29.20% | 70.80% |
| 0055A000008YAu0QAG | michael.montgomery@qgiv.com | 44.68% | 55.32% |
| 0055A000008p6HDQAY | donald.dial@qgiv.com | 43.40% | 56.60% |
| 0055A000008pdP0QAI | ammon.lowman@qgiv.com | 49.16% | 50.84% |
| 0055A000009U9pGQAS | brandon.jones@qgiv.com | 30.39% | 69.61% |
| 005i0000001hjDIAAY | brendan.smith@qgiv.com | 83.09% | 16.91% |
| 005i0000001iPsDAAU | andrew.denniger@qgiv.com | 38.39% | 61.61% |
| 005i0000001iPy1AAE | aaron.liford@qgiv.com | 54.04% | 45.96% |
| 005i0000001iY5MAAU | jack.nelson@qgiv.com | 39.81% | 60.19% |