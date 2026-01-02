# Org Comparison in Dashboard

## Parameters:
- Volume
- Tags
- NTEE
- EIN
- Form composition (year round + auction, year round + P2P, etc.)
- Form type
- Time frame (YTD, past 3 months, past 6 months, 12 months, etc.)

## Insights:
- Amount raised
- Contribution total
- Contribution count
- Average contribution amount
- Churn rate
- Gift assist success rate
- Contributions by amount segment
- Contributions by source
- Contributions by form type
- Contributions by payment method (? Is this useful?)
- Contributions by type
- New vs repeat donors
- One time vs recurring
- Registration count
- Registration total
- Retention rate

## API:

- Can return requested insight data point given parameters, let production/frontend decide how to deal with it; ie, present the data for the requested group as is, present difference, etc.
- We don’t want to delay response by processing lots of stats that will not be presented to the user, so the most performant structure is (1) to provide a list of insights from production in the request and compute all necessary data points for the dashboard at once or (2) compute by individual insight.
- If this is to become a a default presentation in dashboard insights, will need to include Nick for backend assistance. The current standard for API’s will not be able to keep up with dashboard requests with fast responses. We can check current dashboard traffic to load test and create aggregate tables to speed up calculations.
