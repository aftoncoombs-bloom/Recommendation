# Log

## Update Log

- Available data
    - Data structures review
    - Auth and API verification
- 12/06/2019
    - Tasks had a large number of unlabeled Task.type fields; reduced this from ~40k to ~2k
    - Events have 99% untagged Event.type fields; descriptions and titles are very noisy, not sure this needs to resolved
- 12/12/2019
    - talked with Mauk, found out that the most impactful data source is what is referred to as the "activity log" in the UI; this table doesn't exist and is a composite of Events and Tasks tables; this is the data that will lead to the true data goal of generating a time series of events to represent the sales lifecycle
    - need to generate a canonical type list, tag Event.type and Task.type with the canonical list, then merge list to recreate the "activity log" that should properly represent the history of a lead/opportunity
- 12/18/2019
    - unified types and tagged 99% of tasks and 85% of events that were untagged with a type
    - merged tasks and events to create a unified activity history
    - created lead to opportunity ID mapping with dates created, dates closed, and closed status
    - exploring and analyzing
- 12/26/2019
    - Continuing exploration; building report from data to deliver to Mauk
    - The data suggests a few optimizations that require further exploration to confirm, pursuing those ideas
- 1/02/2020
    - still pursuing confirmation of the data indicating that losses are doomed from the start, not worthy of additional effort