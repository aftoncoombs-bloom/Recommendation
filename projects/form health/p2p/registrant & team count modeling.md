Looking at the relationship between the registrant count and team count to donations. Not sure if this is really going to go anywhere given these values are current to the time slice, rather than current total count. More practically, the values in any given observation are derived from that period when the most likely relationship here is that donations related to registrations are going to be most strongly related to registrations in the past rather than those that happened within the past few hours. But we'll take a run at it anyway because we got it.

# Registration & Teams count as related to donations

```python
df_reg = pd.read_csv("~/Repositories/datasets/analytics_p2p_registrations.csv")

cols = ['reg_count', 'don_count', 'reg_conversion', 'teams_count']
df_reg[cols].corr()
```

Observation based registrant count correlation to donation count: 0.00064
Observation based team count correlation to donation count: 0.377

The correlation between registrant count and donations is pretty weak, but the teams correlation to donations is very promising. As stated earlier, it is unlikely that looking at these values will reveal much, but looking at the data in aggregate will most likely show the relationship I'm looking for.

# Aggregate based relationships

Aggregating by form and looking at total registrants and teams counts makes these relationships much more visible.

```python
f = {'reg_count':['sum'], 'teams_count':['sum'], 'don_count':['sum']}
df_agg = df_reg.groupby('form').agg(f)
df_agg.corr()
```

|             | reg_count | teams_count | don_count |
| ----------- | --------- | ----------- | --------- |
| reg_count   | 1.0       | 0.255665    | 0.350512  |
| teams_count | 0.255665  | 1.0         | 0.854641  |
| don_count   | 0.350512  | 0.854641    | 1.0       |

Here we're clearly seeing a strong relationship between teams and donations, which makes sense. The relationship between registrations and donations is much weaker, but stronger than most of the relationships we've seen thus far in other factors. The most important factor here, however, is to determine whether or not the relationships can inform greater fundraising. Ie, what is the average donation per team when there are 5 teams as opposed to when there are 10 teams? Does greater competition inspire greater fundraising?

_These evaluations are based upon totals present within the data set rather than looking at any given observation._

## Teams

Grouping by team counts, it is apparent that there is an obvious trend between team counts and average donation. It appears that beyond 200 teams, the data becomes extremely sparse but under 200 it is well populated.

| team count range | mean donation count |
| ---------------- | ------------------- |
| (0, 24.75]       | 61.42               |
| (24.75, 49.5]    | 338.67              |
| (49.5, 74.25]    | 735.10              |
| (74.25, 99.0]    | 723.07              |
| (99.0, 123.75]   | 1540.65             |
| (123.75, 148.5]  | 1084.64             |
| (148.5, 173.25]  | 954.20              |
| (173.25, 198.0]  | 2059.80             |

There is clearly an upward trend here, but it is not perfectly linear. Perhaps more simply represented when binned into 4 groups:

| team count range | mean donation count |
| ---------------- | ------------------- |
| (0, 50]          | 74.12               |
| (50, 100]        | 729.79              |
| (100, 150]       | 1334.71             |
| (150, 200]       | 1507.00             |

This all holds up to common sense, but looking at the per team average donation value shows really very little information here. There is a lot of noise, but a smoothed trend of team count to per team donation count proves consistent across the board, vascillating consistently around 13.47 donations per team.

![teams_norm_don_amount.png](../../resources/teams_norm_don_amount.png)

When removing a few scarce outliers, the normalized per teams funds raised remains fairly stable regardless of the number of teams present.

## Registrants

Registrants have a less clear relationship. There's an apparent rise from 0, but it does appear to peak between 400 and 600 registrants, after which the mean donation count appears to decrease.

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

The per registrant donation counts, on the other hand, hold a clear upwards trend. In other words, the more registrants an event has, the more each registrant will raise.

| reg count range  | mean per reg donation count |
| ---------------- | --------------------------- |
| (-0.0306, 3.819] | 0.609260                    |
| (3.819, 7.639]   | 5.384977                    |
| (7.639, 11.458]  | 8.659826                    |
| (11.458, 15.278] | 13.334884                   |
| (15.278, 19.097] | 18.964891                   |
| (19.097, 22.916] | 20.736842                   |
| (22.916, 26.736] | NaN                         |
| (26.736, 30.555] | 30.555035                   |

![regs_norm_don_amount.png](../../resources/regs_norm_don_amount.png)

When normalized per registrant, there does exist an upward trend such that the funds raised per registrant is positively correlated to the number of registrants engaged in the event.

_Interpretation_: my guess here is that this is a consequence of a few possible scenarios:

1. More registrants will result in the greater incidence of competition between the participants.
2. More registrants within a given event increases the visibility of individuals, possibly motivating them to raise more money in an effort to avoid the shame of being seen _not_ raising more money.
3. With an increase in participants comes the increased likelihood of participants who interact outside of the event thus increasing the possibility of the participants encouraging and helping each other to raise more money for the event.

__What is most interesting to me here is the per team donation numbers and the per registrant donation numbers don't align. I would be very interested to see what the correlation is between participant fundraising when independent and when on a team. This view of the data appears to suggest that independent fundraisers raise more than team members do.__

| status      | % transactions | mean amount | funds raised | mean count |
| ----------- | -------------- | ----------- | ------------ | ---------- |
| team        | 45%            | 69.23       | 177.79       | 2.57       |
| independent | 55%            | 77.51       | 310.58       | 4.00       |

The team member to independent split appears fairly even in terms of transactions generated with slight favor to independents. The independent registrants are clearly doing better across the board, generating more donations of higher values than team members.

# Source distributions

Looking at transactions grouped by target type.

| entity | mean amount | count   | sum per   | uniques |
| ------ | ----------- | ------- | --------- | ------- |
| event  | 131.572732  | 1920517 | 274660.51 | 920     |
| team   | 81.015110   | 37596   | 401.61    | 7584    |
| reg    | 73.752294   | 140398  | 235.62    | 43947   |

_Things getting a little weird with the transaction.transDonationEntityType==0 filter so I'm pretty sure some qgiv donations are being counted in the event stats here, so the 'event' row is suspect._ 

My first thought in these scenarios is the pareto principle of social networks which colloquially states that 90% of the content in any network is created by 10% of the users, or more generally the 80/20 rule. This has not held up by investigation. I first set the percentage of total funds raised for the event by each participant.

```python
reg_donations['pcnt_raised'] = reg_donations.apply(
    lambda x: x.amount_sum / reg_donations[reg_donations.form_first==x.form_first].amount_sum.sum(), axis=1)
```

Then, for lack of better method, I iterated through each event, isolated the dataframe view to that events participants, sorted the dataframe view by percentage of total funds raised in descending order, and counted for each event how many registrants it took to reach 80% of funds raised by percentage of the total registrants. Ie, 23% of the registrants were responsible for raising 80% of the funds.

```python
d = []
for f in reg_donations.form_first.unique():
    temp_df = reg_donations[reg_donations.form_first==f].sort_values('pcnt_raised', ascending=False)
    funds_pcnt = 0.
    reg_count = 0
    for _, r in temp_df.iterrows():
        funds_pcnt += r.pcnt_raised
        reg_count += 1
        if funds_pcnt > .8:
            d.append({'form': f, 'reg_count': reg_count, 'prcnt_regs': float(reg_count) / float(len(temp_df))})
            break

```

Looking at the data accumulated here, we get the following:

```python
reg_count_to_80prcnt_funds = pd.DataFrame(d)
pd.cut(reg_count_to_80prcnt_funds['prcnt_regs'], bins=10).value_counts().sort_index()
```

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

It certainly appears that the standard application of the pareto principle to social networks does not hold up within our system. It appears to be much closer to a normal distribution with a peak at the end (90%+ of registrants were responsible for 80% of the funds raised). Not quite what I was hoping for but not necessarily bad news. __This does indicate a broader engagement and participation within the fundraising events than one would expect to see in any group or collective action.__ 


Notebooks:
- [registrant and team counts to donation](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/registrant%20and%20team%20counts%20to%20donation.ipynb)
- [source distribution modeling](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/source%20distribution%20exploration.ipynb)

References:
- [Do You Know Who’s Lurking?  90% of Social Media Users don't publicly interact.](https://www.linkedin.com/pulse/do-you-know-whos-lurking-90-social-media-users-lurkers-joey-little/)
- [1% rule](https://en.wikipedia.org/wiki/1%25_rule_(Internet_culture))
- [90-9-1 Rule of Thumb: Fact or Fiction?](https://www.linkedin.com/pulse/90-9-1-rule-thumb-fact-fiction-stan-garfield/)
- [Community Management: The 90-9-1 Rule is Dead](https://senseimarketing.com/community-management-the-90-9-1-rule-is-dead/)
- [The 90-9-1 Rule in Reality](https://community.lithium.com/t5/Science-of-Social-Blog/The-90-9-1-Rule-in-Reality/ba-p/5463)