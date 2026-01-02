# Bids

Unique counts:

- bids: 86889
- forms: 96
- bidders: 6215
- products: 2878

Groups:

- bidders per form: 64.73
- products per form: 29.98
- bids per bidder: 10.78
- bidders per product: 9.11
- bids per product: 30.19

## Multiple bid time differences

The time differences here are the differences between the bid times of multiple bids per bidder with single bid bidders excluded. For example, if a bidder places 3 bids with 3 hours between the first and second bids and 1 hour between the second and third bids, the date diff will be 1.5 hours.

- Bidders: 5441
- Single bidders: 773 (8.05 per form)
- Mean percentage single bidder: 12.44%
- Mean bid date diff: 12 days 19:57:38.430699
- Unique date diffs: 173

Bids are logging in batches. Not sure if that's intentional but we can see here that there are only 173 unique date diffs from first bid while there are 5441 unique bidders. Clearly we're losing a lot of time data here so I cannot say how reliable this data is.

# TransAuction

Data generated from transaction.date joined on transauction tables, alternating from purchases only to purchases and donations.

Including _purchases and donations_, mean times (excluding 2030 starts):

- time_since_beginning     2 days 05:49:36
- time_since_end          -3 days +18:10:23

Including _only purchases_, mean times (excluding 2030 starts):

- time_since_beginning     2 days 12:18:36
- time_since_end          -3 days +11:41:23

Percentage complete within intervals from settings end date including _only purchases_ and _purchases and donations_ (excluding 2030 starts):

- 1 hour: 45.45%
- 12 hour: 51.52%
- 24 hour: 81.82%

Percentage complete within intervals from settings start date including _purchases and donations_ (excluding 2030 starts):

- 1 hour: 50.00%
- 12 hour: 56.67%
- 24 hour: 90.00%