# Average transaction value by dollar amount for one time donations

__Average one time donation value, all orgs, all time:__

Query: `select amount` from accepted (online) non-recurring transactions, mean and median calculated from all returned values

- mean: \$170.18
- median: \$50.00

__Average one time donation value, all orgs, 2023:__

Query: `select amount` from accepted (online) non-recurring transactions in the year 2023, mean and median calculated from all returned values

- mean: \$182.96
- median: \$50.00

__Average value per transaction by dollar value and transaction type counts, by segments, all years__

Values queried grouped by organization and year, the returned values were grouped into revenue segments and mean and median were calculated from those subsets

|    | key                           | mean onetime count   | median onetime count   | mean recurring count   | median recurring count   | mean avg onetime value   | median avg onetime value   |
|---:|:------------------------------|:---------------------|:-----------------------|:-----------------------|:-------------------------|:-------------------------|:---------------------------|
|  0 | \$0 to \$100k            | 119.17               | 39.00                  | 3.20                   | 0.00                     | \$210.53                | \$124.84            |
|  1 | \$100k to \$1M    | 1,137.70             | 712.00                 | 33.65                  | 12.00                    | \$340.64                | \$231.34            |
|  2 | \$1M to \$10M | 7,633.13             | 6,010.00               | 433.35                 | 218.00                   | \$276.80                | \$209.65            |
|  3 | \$10M+                 | 37,967.29            | 38,239.00              | 5,788.00               | 3,091.00                 | \$191.94                | \$172.96            |

__Average onetime/recurring for 2023:__

Values queried grouped by organization and year, the returned values were grouped into revenue segments and mean and median were calculated from those subsets for the year of 2023

|    | key                           | mean onetime count   | median onetime count   | mean recurring count   | median recurring count   | mean avg onetime value   | median onetime value   |
|---:|:------------------------------|:---------------------|:-----------------------|:-----------------------|:-------------------------|:-------------------------|:-----------------------|
|  0 | \$0 to \$100k            | 126.24               | 44.00                  | 2.02                   | 0.00                     | \$247.59                | \$143.96          |
|  1 | \$100k to \$1M    | 1,111.94             | 670.00                 | 28.66                  | 8.00                     | \$363.26                | \$263.81          |
|  2 | \$1M to \$10M | 7,059.37             | 5,535.00               | 230.47                 | 167.00                   | \$274.06                | \$205.84          |
|  3 | \$10M+                 | 33,848.60            | 31,531.00              | 5,634.20               | 2,867.00                 | \$198.14                | \$221.35          |

__Average onetime transaction value (2023), by org:__

Values queried grouped by organization and year, mean and median calculated from the returned values for the year 2023

|    | key                  | mean      | median    |
|---:|:---------------------|:----------|:----------|
|  0 | all orgs             | \$229.13 | \$139.92 |
|  1 | top 20% orgs         | \$288.13 | \$194.20 |
|  2 | representative forms | \$230.48 | \$165.52 |
