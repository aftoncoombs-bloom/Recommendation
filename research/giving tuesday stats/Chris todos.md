# Chris request

- express donate, recurring nudges
- talk to sandra re: tracking gift reminders functionality, frontend; we care about whether or not the original donation was executed

Data points for GiveCon:
- Impact of recurring nudges and recurring modals on conversion rate
    - /research/new forms/build/report - new settings.ipynb
- ~~Impact of conversion rate for forms using express donate~~
    - /research/mobile/expresscheckout research.ipynb
    - notebook run, need to build report
- Smart amounts - I think I can use your data from Giving Tuesday
    - /research/giving tuesday stats/smart amounts.ipynb
- Abandoned gift reminders - not sure we will have enough data by the time GiveCon rolls around at the end of February but if there is reliable data available I'd like to incorporate

# Giving Tuesday 2024

- Representative forms
    - ~~avg gift size, conversion, etc., from form report~~
    - YoY, conversion rate
- Digital wallet
    - ~~% of participating orgs donor's adoption~~
    - avg gift size, conversion, etc., for digital wallet donors
    - YoY
- Smart Amounts
    - ~~avg transaction~~

## GT $/org YoY

2023:
----------------------------------------
1,786 orgs
$3,798.49/org mean
$669.65/org median

2024:
----------------------------------------
1,314 orgs, 73.57% retained from 2023
$5,119.92/org
$1,099.10/org median

## Smart amounts

### GT 2024

|    | ('smart_amounts', '')   |   ('count', 'mean') |   ('count', 'median') |   ('volume', 'mean') |   ('volume', 'median') |   ('mean_trans_amount', 'mean') |   ('mean_trans_amount', 'median') |
|---:|:------------------------|--------------------:|----------------------:|---------------------:|-----------------------:|--------------------------------:|----------------------------------:|
|  0 | False                   |             9.76825 |                     3 |              1839.42 |                 312.55 |                         234.079 |                           100.032 |
|  1 | True                    |             9.16554 |                     3 |              1914.54 |                 469    |                         185.247 |                           107.655 |


## Digital wallet

Qgiv forms:
- 599 (11.41%) forms used digital wallets
- among forms using digital wallet, 29.45% mean, 20.00% median of transactions were digital wallet transactionscoul

Bloomerang:
- 2023 5% (4067/81343) were digital wallet txns
- 2024 10.13% (9295/91798)
- MethodType IN ('PayPal', 'ApplePay', 'GooglePay', 'Venmo')

# Express checkout

_Data from the period 2023-04-01 to 2024-12-09_

Mean express checkout adoption: 35.12%
Median express checkout adoption: 23.73%

## Aggregate conversion

_Aggregate conversion_ is calculating the conversion rate per form, then averaging those values

### All

- Express checkout forms conversion: 17.87% mean; 11.08% median
    - mobile only: 25.12% mean; 13.82% median
- Non express checkout forms conversion: 13.69% mean; 7.45% median
    - mobile only: 17.41% mean; 7.50% median
    
### Only forms with > 400 pageviews

Mean express checkout adoption: 35.89%
Median express checkout adoption: 23.90%

- Express checkout forms conversion: 14.54% mean; 10.26% median
    - mobile: 16.44% mean; 10.24% median
- Non express checkout forms conversion: 9.35% mean; 5.34% median
    - mobile: 9.00% mean; 4.15% median
    
### Excluding top 10%

Mean express checkout adoption: 42.22%
Median express checkout adoption: 27.82%

- Express checkout forms conversion: 15.69% mean; 9.34% median
    - mobile: 25.18% mean; 14.19% median
- Non express checkout forms conversion: 12.08% mean; 6.17% median
    - mobile: 17.08% mean; 6.30% median