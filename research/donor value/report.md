The objective of this research was to examine upselling a donor from a single, one time donation to further engagement and more giving. We already know that donors with greater engagement deliver and drive more giving. Ideally we could identify key escalation conversion activities to drive greater engagement by the donor.

## About the data

The dataset is a sampling of the last 1 million unique donors. For each donor, their full giving history within the system was retrieved. Transactions were segmented only by donor without consideration for form or organization, so a repeated donor as represented here is not necessarily a repeat donor to the same organization. The donors represented in the dataset have first transactions spanning the following years:

| First Year |   Donor Count     |
|------------|-------------------|
|    2017    |    69,449         | 
|    2018    |    67,849         | 
|    2019    |    96,529         | 
|    2020    |   766,173         |

# Overlap

Here we can see transaction count correlations which indicate the relationships between a donor's chosen transaction source or type to the others. The strongest relationships we see here are negative correlations primarily between events, P2P, and generally one time sources and positive relationships between related sources. This is most likely a selection bias of the most common use cases for the different types of giving. For instance, we see a negative correlation between P2P transaction count and Qgiv donation form transaction count and a positive correlation between registrations and P2P transaction count.

|                      | don_form_count  | donations_count | fb_count | givi_count | kiosk_count | mobile_count | mobilevt_count | p2p_count | purchases_count | registrations_count | sms_count | recurring |
|---------------------|-----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| don_form_count      |    1.00         |   0.14   |   0.09     |  0.003      |    0.09      |   0.03         |     1.00  |      -0.025     |        -0.004       |  -0.016   | 0.09   | 0.306  |
| donations_count     |    0.14         |   1.00   |   0.998    |  0.006      |    0.997     |   0.068        |     0.14  |       0.117     |         0.0009      |  0.0296   | 0.997  | 0.976  |
| fb_count            |    0.092        |   0.998  |   1.00     | -0.00002    |    0.998     |   0.055        |     0.092 |       0.117     |         0.001       |  0.03     | 0.998  |  0.967 |
| givi_count          |    0.003        |   0.006  |  -0.00002  |  1.00       |    0.005     |   0.013        |     0.003 |      -0.003     |         0.0006      |  -0.001   | 0.0006 | 0.0006 |
| kiosk_count         |    0.092        |   0.997  |   0.998    |  0.005      |    1.00      |   0.0568       |     0.092 |       0.117     |         0.001       |  0.03     | 0.997  | 0.966  |
| mobile_count        |    0.029        |   0.068  |   0.055    |  0.013      |    0.057     |   1.00         |     0.029 |      -0.03      |        -0.004       |  -0.016   | 0.057  | 0.0598 |
| mobilevt_count      |    1.00         |   0.14   |   0.092    |  0.003      |    0.09      |   0.029        |     1.00  |      -0.025     |        -0.004       |  -0.017   | 0.09   | 0.307  |
| p2p_count           |    -0.025       |   0.117  |   0.117    | -0.003      |    0.117     |   -0.03        |    -0.025 |       1.00      |         0.085       |  0.515    | 0.12   | 0.11   |
| purchases_count     |    -0.004       |   0.0009 |   0.001    |  0.0006     |    0.001     |   -0.004       |    -0.004 |       0.085     |         1.00        |  0.0667   | 0.001  | 0.0009 | 
| registrations_count |    -0.0165      |   0.03   |   0.03     | -0.001      |    0.03      |   -0.016       |    -0.02  |       0.515     |         0.0668      |  1.00     | 0.03   | 0.029  |
| sms_count           |    0.091468     |   0.997  |   0.998    |  0.0006     |    0.997     |   0.057        |     0.092 |       0.116     |         0.001       |  0.03     | 1.00   | 0.965  |
| recurring           |    0.306601     |   0.976  |   0.967    |  0.0006     |    0.966     |   0.06         |     0.307 |       0.113     |         0.0009      |  0.03     | 0.965  | 1.00   |

# Progression

If we assume that donors will generally progress down the path of least resistance or greatest organizational support, it follows that the most likely path of engagement escalation will reveal itself by strongest overlaps between giving cohorts.

One time overlap:
- events: 4.41%
- recurring: 10.27%
- p2p: 28.85%

Events overlap:
- onetime: 23.73%
- recurring: 3.44%
- p2p: 6.98%

Recurring overlap:
- onetime: 95.17%
- events: 5.93%
- p2p: 4.19%

P2P overlap:
- onetime: 82.94%
- events: 3.73%
- recurring: 1.30%

Judging by these overlap percentages, it appears that the escalation progression is one time > p2p > events > recurring. Event participation, in P2P or Qgiv events, is the next step for a one time donor but this unfortunately does not translate directly to greater fundraising for the organization given the time restricted nature of the engagement. Participants of any form of events are likely to give directly around half as much as one time donors and both are most likely to engage only once. Recurring donors, on the other hand, are most likely to remain engaged for a year and a half and give a total of 4 times the amount of a one time donor and nearly 9 times the amount of an event participant.  

## Key indicator

The strongest indicator of donor engagement escalation is appears to be time. All factors seem to have weak relationships with escalation with the sole excception of repeat engagement. Unsurprisingly, donors that give multiple times are worth more than one time donors, however the degree of engagement also escalates with time. The longer a donor is engaged, the more engaged they become and the more likely they become to give again.

## Engagement lifetime

The median engagement lifetime of all cohorts is 0 days, which is to say that they give once and never return. The only exception to this is recurring with a median engagement of 418 days. There is an obvious tendency of events to drive engagement for a brief period of time, seemingly peaking between 1 and 10 days and falling below the single engagement overlap after 30 days, however this does not strongly transition donors to recurring. While this increased engagement is brief, it is meaningful as it appears that a donor that engages more than once will maintain their giving level over multiple transactions, thus doubling their value, even with only two engagements. The engagement with other channels (events or recurring) also increases sharply with only that second engagement.

### One time donors segmented by engagement lifetime by days:

| Days engaged | P2P overlap | Events overlap | Recurring overlap | Mean per transaction | Median per transaction | Mean total amount | Median total amount |
|----------|--------|--------|--------|----------|---------|------------|----------|
| 0        | 31.41% | 0.28%  | 1.01%  | \$144.71 | \$50.40 | \$149.54   | \$51.50  |
| (1, 10)  | 53.84% | 10.24% | 3.47%  | \$138.59 | \$50.00 | \$314.99   | \$100.00 |
| (10, 30) | 37.77% | 8.14%  | 3.64%  | \$143.76 | \$52.50 | \$479.31   | \$125.00 |
| (30, 60) | 21.62% | 6.90%  | 24.63% | \$129.32 | \$50.00 | \$342.46   | \$125.00 |
| (60, 90) | 17.92% | 8.38%  | 29.38% | \$141.80 | \$50.74 | \$388.50   | \$150.00 |
| 90+      | 23.49% | 11.89% | 27.46% | \$172.05 | \$62.88 | \$1,258.88 | \$307.50 |

It is noteworthy that the repeat donor segment represented in the table above overlaps with recurring by only 24% to 30% in the groups with greater than 30 days of engagement. This is to say that of donors engaging for more than 1 month, less than 30% of them have actually created a recurring transaction. While this could represent donors giving to mulitple organizations over time and the blame might not lay entirely on the individual organizations, it does clearly indicate that there is a segment of donors that should be easily convinced to more meaningfully engage to commit to recurring donations.

### P2P donors segmented by engagement lifetime by days:

| Days engaged | Onetime overlap | Events overlap | Recurring overlap | Mean per transaction | Median per transaction | Mean total amount | Median total amount |
|-------------|-------------|-------------|-------------|--------------|--------------|--------------|--------------|
| 0 | 80.44% | 0.04% | 0.07% | \$81.57 | \$40.00 | \$84.56 | \$41.98 |
| (1, 10) | 93.41% | 3.75% | 0.41% | \$84.53 | \$35.00 | \$195.64 | \$80.00 |
| (10, 30) | 94.46% | 5.41% | 0.52% | \$93.85 | \$42.50 | \$225.63 | \$100.00 |
| (30, 60) | 94.45% | 9.30% | 2.10% | \$116.59 | \$50.00 | \$303.30 | \$115.00 |
| (60, 90) | 94.28% | 13.99% | 5.44% | \$119.60 | \$52.47 | \$312.27 | \$130.00 |
| 90+ | 87.91% | 13.65% | 4.77% | \$131.64 | \$52.60 | \$1,085.52 | \$171.14 |

### Event donors segmented by engagement lifetime by days:

| Days engaged | Onetime overlap | P2P overlap | Recurring overlap | Mean per transaction | Median per transaction | Mean total amount | Median total amount |
|-------------|-------------|-------------|-------------|--------------|--------------|--------------|--------------|
| 0 | 1.60% | 0.10% | 0.02% | \$77.97 | \$13.65 | \$80.81 | \$15.00 |
| (1, 10) | 18.30% | 3.86% | 0.59% | \$114.23 | \$40.00 | \$247.56 | \$88.40 |
| (10, 30) | 24.27% | 6.45% | 0.33% | \$113.70 | \$37.50 | \$254.03 | \$80.00 |
| (30, 60) | 34.34% | 10.60% | 1.50% | \$106.81 | \$32.50 | \$256.41 | \$77.50 |
| (60, 90) | 42.76% | 13.57% | 2.32% | \$115.13 | \$38.22 | \$297.45 | \$98.50 |
| 90+ | 60.93% | 18.68% | 9.93% | \$186.51 | \$71.43 | \$1,959.87 | \$290.00 |

We see similar trends in events and P2P as we saw in one time. Increased engagement lifetime tracks with increased engagement, as well as generally increased value per transaction.

Unfortunately we are unable to capably track the followup efforts made by the organizations to maintain engagement with donors, so it is not possible presently to determine the most effective means of donor retention. It is however clear that however this is achieved, the continued value of each segment of donor should prove to be worth the effort. The monthly value for all cohorts is most commonly around \$65. While we can only speculate as to an average cost of any mass marketing or communication method, it seems reasonable to assume that a reasonable strategy would cost far less than \$65 per contact.