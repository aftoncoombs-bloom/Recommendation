# Log

## Implementation notes

- likely data sources
    - most likely going to derive primarily from analytics and system logs to gauge activity
    - possible success metrics:
        1. feature implementations verified from analytics
        2. processing volume from transactions
- tag logs and analytics with org lifetime milestones
    - ie, 1 week, 4 weeks, 12 weeks, 24 weeks, 52 weeks
    - this will allow for aggregating normal lifecycle events and compare feature adoption to transaction events by relative lifetime

## Update log

- Exploring and transforming the data
    - Need logs tagged with org lifetime, script taking too long, need to re-evaluate or explore alternative means of updating the data
    - Done, exploring
    - Need analytics tagged with org lifetime, running build script
    - Done, exploring
- 12/12/2019
    - it has become clear to me that without more granular activity data (client page views, control panel interactions, etc.) it is not possibe to truly refine a product understanding metric at this point
    - giving up on product understanding, focusing efforts on product adoption
    - @TODO
        1. write product adoption queries for production
        2. develop dashboard to analyze product adoption export data
