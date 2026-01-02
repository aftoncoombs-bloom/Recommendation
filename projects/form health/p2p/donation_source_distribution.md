Looking at the relationship between the registrant count and team count to donations. We're looking here to discover underlying relationships between registrant counts and funds raised, and team counts and funds raised. The observations used to collect this data are primarily in aggregate to total funds raised in order to get a complete picture of the performance of the event based upon their final numbers rather than attempting to correlate one day's numbers to the following day's donations.

# Aggregate relationships

Aggregating by form and looking at total registrants and teams counts, we see a strong relationship between teams and donations, which makes sense. The relationship between registrations and donations is much weaker, but stronger than most of the relationships we've seen in other event factors. The most important factor here, however, is to determine whether or not the relationships can inform greater fundraising. Ie, what is the average donation per team when there are 5 teams as opposed to when there are 10 teams? Does greater competition inspire greater fundraising?

## Teams

Grouping by team counts, it is apparent that there is an obvious trend between team counts and average donation. While there are observations beyond 200 teams, the data becomes extremely sparse, so those were omitted.

| team count range | mean donation count |
| ---------------- | ------------------- |
| (0, 50]          | 74.12               |
| (50, 100]        | 729.79              |
| (100, 150]       | 1334.71             |
| (150, 200]       | 1507.00             |

This all holds up to common sense, but looking at the per team average donation value shows there's really very little useful information here. There is a lot of noise, but a smoothed trend of team count to per team donation count proves consistent across the board, vascillating consistently around 13.47 donations per team.

![teams_norm_don_amount.png](../../resources/teams_norm_don_amount.png)

When removing a few scarce outliers, the normalized per teams funds raised remains stable and consistent, regardless of the number of teams present. In other words, whether there are 4 teams or 400, the amount raised per team remains approximately the same.

## Registrants

Registrants have a less clear relationship. The average donation count peaks between 400 and 500 registrants, after which the mean donation count decreases.

| reg count range | mean donation count |
| --------------- | ------------------- |
| (-0.748, 93.5]  | 8.123393            |
| (93.5, 187.0]   | 116.951724          |
| (187.0, 280.5]  | 301.428571          |
| (280.5, 374.0]  | 817.578125          |
| (374.0, 467.5]  | 2096.948718         |
| (467.5, 561.0]  | 1692.500000         |
| (561.0, 654.5]  | 691.333333          |
| (654.5, 748.0]  | 596.000000          |

The per registrant donation counts, on the other hand, holds a clear upwards trend. In other words, the more registrants an event has, the more each registrant is raising.

![regs_norm_don_amount.png](../../resources/regs_norm_don_amount.png)

When normalized per registrant, there does exist an upward trend such that the funds raised per registrant is positively correlated to the number of registrants engaged in the event.

_Interpretation_: my guess here is that this is a consequence of a few possible scenarios:

1. More registrants will result in the greater incidence of competition between the participants.
2. More registrants within a given event increases the visibility of individuals, possibly motivating them to raise more money in an effort to avoid the shame of being seen _not_ raising money.
3. With an increase in participants comes the increased likelihood of participants who interact outside of the event thus increasing the possibility of the participants encouraging and helping each other to raise more money for the event.

__What is most interesting to me here is the per team donation numbers and the per registrant donation numbers do not align. This view of the data appears to suggest that independent fundraisers raise more than team members do but we will have to look at the team member data in order to determine that.__

## Team members vs independent participants

| status      | % transactions | mean amount | funds raised | mean count |
| ----------- | -------------- | ----------- | ------------ | ---------- |
| team        | 45%            | 69.23       | 177.79       | 2.57       |
| independent | 55%            | 77.51       | 310.58       | 4.00       |

The team member to independent split appears fairly even in terms of transactions generated, with slight favor to independents. **The independent registrants are clearly doing better across the board, generating more donations of higher values than team members. That being said, the difference here is meaningful but not so significant that I would claim they were reliably superior performers but rather that team membership is irrelevant to fundraising outcomes.**

# Source distributions

Looking at transactions grouped by target type.

| entity | mean amount | count   | sum per   | uniques |
| ------ | ----------- | ------- | --------- | ------- |
| event  | 131.572732  | 1920517 | 274660.51 | 920     |
| team   | 81.015110   | 37596   | 401.61    | 7584    |
| reg    | 73.752294   | 140398  | 235.62    | 43947   |

_Things getting a little weird with the transaction.transDonationEntityType==0 filter so I'm suspect some qgiv donations are being counted in the event stats here, so the 'event' row is suspect._ 

## How many participants are responsible for raising most of the funds?

My first thought in these scenarios is the pareto principle of social networks which colloquially states that 90% of the content in any network is created by 10% of the users. Social networks have historically been broken down into 3 groups of 90% (consumers), 9% (casual users), and 1% (power users). One would expect to see little to no activity from the _consumer_ group, rare activity from the _casual_ group, and the vast majority of the activity from the _power user_ group. While this pattern has been seen in all major online services, it is not present in our fundraising events.

90% proved too high a threshold for our data so I lowered the bar to 80% and looked at how many registrants on average were necessary to reach each 80% of funds raised for the given event. Ie, 23% of the registrants were responsible for raising 80% of the funds. Looking at the data accumulated, the distribution is fairly even around the middle telling us that most events raise 80% of their funds from around half of their participants.

| percent range   | reg count |
| --------------- | --------- |
| (0.0824, 0.175] | 9         |
| (0.175, 0.267]  | 35        |
| (0.267, 0.358]  | 104       |
| (0.358, 0.45]   | 201       |
| (0.45, 0.542]   | 228       |
| (0.542, 0.633]  | 123       |
| (0.633, 0.725]  | 52        |
| (0.725, 0.817]  | 35        |
| (0.817, 0.908]  | 1         |
| (0.908, 1.0]    | 132       |

It appears to be a normal distribution with a peak at the end (90%+ of registrants were responsible for 80% of the funds raised) rather than a Pareto distribution. __This indicates a much broader engagement and participation within the fundraising events than one would expect to see in online groups or collective actions.__ 

___

Notebooks:

- [registrant and team counts to donation](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/registrant%20and%20team%20counts%20to%20donation.ipynb)
- [source distribution modeling](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/source%20distribution%20exploration.ipynb)