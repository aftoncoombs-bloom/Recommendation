# Client webpage stats analysis

## Business objective

Develop ability to collect data relating to client websites in an automated, ongoing manner.

## Completion

- Develop spider to crawl client sites looking for (1) outbound links, (2) calls to action, (3) social links, (4) and page structure.
- Create an automated warning system (email or log?) that will identify outbound links to competitors on active client sites.
- Examine common attributes of successful sites by available data points discovered by the spider.
- Cache data for use in other projects and models.

## Milestones

- Develop spider (2 weeks)
- Run & optimize spider (4 weeks)
- Implement warning system (1 week)
- Explore & verify data (1 week)

# Procedures

1. Confirm data from the last run is in Redshift by querying for the maximum date
2. Delete org_website_data.csv file if it is still present
3. Run spider script - "python spider_orgs.py"
4. Process org website data and upload to Redshift - redshift_prep.ipynb
5. Evaluate link count changes - link count change.ipynb