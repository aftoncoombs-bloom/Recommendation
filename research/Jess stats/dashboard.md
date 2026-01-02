# Tech

- likely easiest/fastest in plotly dash
- /research/Jess stats/dashboard.py

## Infrastructure

- aggregate tables updated every 24 hours
    - analytics: /research/Jess stats/analytics_resample.py
    - transactions: /research/Jess stats/aggregate_tables.py
- dashboard built in dash/plotly (/research/Jess states/dasboard.py)
- container packaged for deployment (/fargate/dashboard_stats/)


# datapoints

- 1. donation forms
    - Total active donation forms
    - Total amount raised
    - \# of one-time donations
    - Avg. one-time gift size
    - \# of recurring donations
    - Avg. recurring gift size
- 2. standard events
    - Total \# of standard events
    - Total amount raised (reg. + donations)
    - Total registrations
    - Total donations (online & offline)
- 3. text fundraising
    - Total \# of orgs using text fundraising
    - Total amount raised
    - Avg. gift size through text fundraising
- 4. P2P
    - Total \# of peer-to-peer events
    - Total amount raised (reg. + donations)
    - Total registrations
    - Total donations (online & offline)
- 5. auctions
    - Total \# of auction events
    - Total amount raised (reg. + donations)
    - Total registrations
    - Total donations (online & offline)
    - Total number of bids
    - Avg. \# of bids