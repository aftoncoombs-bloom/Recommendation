# Log

## Implementation notes

- potential data sources:
    - Salesforce annual revenue of leads (1719 or 4.13% of leads have annual revenue values, might be sufficiently late set data points to provide valid information); Lead.csv:AnnualRevenue
    - Salesforce current provider of leads (10411 or 24.99% of leads have current provider values); Lead.csv:Current_Vendor__c
    - Salesforce - Opportunity.csv - What_feature__c, What_integration__c
    - Salesforce - Account.csv - AnnualRevenue
    - [ProPublica](https://projects.propublica.org/nonprofits/api) has an API to research nonprofit filings by EIN (and other parameters)
        - easy, clean interface; tried 3 orgs and only one had data
        - [notebook](notebooks/propublica.ipynb)
    - [OpenData 990s](https://docs.opendata.aws/irs-990/readme.html) is a dataset of "certain" publicly available 990's. Need to explore, "certain" is not described or defined so this may be a limited dataset
        - not as clean an interface but perfectly usable; coverage does seem spotty but from the limited test, I can't say at this point it's better or worse than propublica
        - [notebook](notebooks/opendata.ipynb)
    - [IRS](https://www.irs.gov/statistics/soi-tax-stats-annual-extract-of-tax-exempt-organization-financial-data)
        - extract documentation, 990 extract, 990-EZ extract, and 990-PF extract
        
## Update Log

- 1/2/2020
    - ProPublica turns out to be rate limited; references to bullk download are shown in the block message but that did not lead to a download so far as I found; building a staged scrape script and still looking for that bulk download
    - standardizing IRS and OpenData source outputs
- 12/26/2019
    - Found several open API’s that provide historical 990’s so created script to collect historical 990 from and piece it all together from all datasources; will be running that early in the week to generate history and check for missing data
