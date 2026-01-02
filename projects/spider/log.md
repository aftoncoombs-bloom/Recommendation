# Log

## Implementation notes

- pull client website data from organization table for all active organizations, update list on each run
- crawl home page logging the various stats, iterate through links checking internal links and logging for crawling later if they have not yet been crawled
- using Requests module to manage networking, BeautifulSoup to process HTML
- need to scan javascript sources, contents in the case of raw javascript code, and A link HREF's to check for Qgiv and competitor references and social media 
- _warning system_ should monitor for changes in references to Qgiv or competitors, highlight recent changes by email or log; example scenarios that should be highlighted:
    - when the last crawl of the client site shows 2 Qgiv links and the current crawl shows 0
    - when the last crawl of the client site shows 1 Qgiv link and the current crawl shows 1 Qgiv link and 1 link to a competitor
- considering running the script every 2 weeks, so it needs to complete in less than 2 or 3 days in order to maintain scalability as our client base grows
- not sure how to manage emails from notebooks server running the crawler; ec2 is going to block emails so system needs to be managed some other way

## Update log

- Spider done
- Run & optimize
    - Taking too long; cut short to 100 pages per org
    - Taking too long; cut short to first level linked pages
- Warning system
    - sticking to log output of orgs with changing links/scripts to Qgiv or competitors; easier than trying to deal with emails from the notebooks server

# Code

## Execution

Execute spider_orgs.py

- No data requirements; imports s3_support
- will download the org data and store locally and push to S3
- builds org website data and stores locally and pushes to S3

## Files

- __spider.py__: request a page, process the data, and continue crawling internal pages
- __spider_orgs.py__: request updated org data with URL, filter to active orgs, then iterate through URL's calling the spider on each

## Data structure

- __org__: int
- __date__: date
- __url__: string
- __outbound_links__: int 
- __internal_links__: int
- __calls_to_action__: int
- __word_count__: int
- __image_count__: int
- __link_target_SITE__: [int], column for each competitor, Qgiv and social site
- __script_sources_SITE__: [int], column for each competitor, Qgiv and social site