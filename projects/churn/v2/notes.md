# Churn warnings v2

## Goals

Issues to overcome compared to the first iteration:

1. __Interpretability__: we were able to provide the indicators that lead to the given prediction but these were not very informative, simply identifying the outlying features of the model that did not consistently or readily explain the reasons the algorithm might have predicted a likelihood of churn
2. __Probability__: the current delivery pattern does not provide the probability of churn but just identifies the most likely that have not been previously identified; the second version might be better delivered as a rolling output, perhaps as tag in production with a search mechanism to identify the top X probable churn organizations
3. __Time sensitivity__: we presently have no sense of time sensitivity in our predictions; assuming an accurate prediction, the algorithm gives no indication of an imminent churn within the coming week or 6 months

## Data sources

This project relies upon time series so we will only be able to utilize those data sources that provide data over time. We will primarily rely upon __transactions__ and __analytics__ but we will also look at the __Segment__ data for the available time periods. _Tables and feature adoption will also be adapted for time series collection but we do not yet have an adequate backlog so this should be revisited in the near future._

_4/25/2020: no churned orgs have logged into the system according to Segment_


# Additonal features

- Mean volume growth > mean growth for churned orgs: _91% of churned and 84% of nonchurned orgs have mean volume growth rates beneath the mean churned org growth rate (source: transactions)_
- Months since last login: _no churned orgs have logged into the system according to Segment (past 3 months as time of writing), but 35% of active organizations meet this criteria as well (source: segment)_
- Integrations: _no churned organizations have activated integrations (source: segment)_