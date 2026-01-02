# Amounts recommendation

## Concept

The principal concept is to recommend amounts to users based upon various factors that match a constituency. For example, an iPhone user loads a donation form in Philadelphia should be recommended amounts that align with giving patterns of iPhone users in Philadelphia.

### Build

Features used:

1. Location
2. Platform

The features will be used to calculate a median donation amount to be used by production to produce recommended amounts to be presented to the potential donor.

### Operation

#### Training

Transactions will be grouped by platform, state, and zip to calculate the median donation amount for each pairing of platform and state or zip code. These values will be stored in a CSV to be held in memory as a dataframe for immediate access by the API.

**Target URL:***

- (POST) https://52.2.34.90:8891/amounts_recom/

#### Input

__Prototype__

- state: (required) str; two character abbreviation of US state
- zip: (required) str; zip code
- useragent: (required) str; browser user agent string

```
$params = array(
    'state' => 'FL',
    'zip' => '33801',
    'useragent' => 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
);
```

The prototype build will rely upon direct input of state and zip code. This is to provide demo functionality until the external service API becomes available for retrieving state and zip code by IP address.

__Production__

- ip: (required) str; IP address of device
- useragent: (required) str; browser user agent string

```
$params = array(
    'ip' => '192.0.2.1',
    'useragent' => 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
);
```

The _IP address_ will be used to identify a zip code and state. This will allow for failover groups such that when there are insufficient samples for a given zip code, we can use the state.

The _user agent_ will be parsed to identify platforms (iPhone, Android, iPad, Windows, or Mac).

**Target URL:***

- (POST) https://52.2.34.90:8891/amounts_rec_data/

This API endpoint will deliver the median amount data set for complete export. This requires loading a lot of data from the database so it will not return quickly.

#### Input

- key: (required) str; really lazy security measure

As literally the least we can do, a validation key is required in order to process the request and return the requested data.

```
$params = array(
    'key' => '[key value]'
);
```

#### Output

The output data is provided as an array of objects specifying state, zip code, platform, is christmas, is new years, the given median amount and sample size (count). There are additional entries with null values to account for state wide medians (ignoring zip code) for all or no specific platforms.

```
{
    "status": 1,
    "data": [
        {
            'state': 'FL',
            'zip': '33801',
            'platform': 'iPhone',
            'is_christmas': 'False',
            'is_newyears': 'False',
            'median': 98.45,
            'count': 489
        },
        ...
    ]
}
```

## API

__Files__

1. api.amounts_recom.py: Flask app file to run the API endpoints
2. train.amounts_recom.py: Compiles reference median amounts data and stores the data locally to CSV

__Prototype__

The API is set up as a Flask app that loads the precalculated amount medians on application launch and queries by the provided input by those values (useragent, state, zip code).

__Production__

The API is set up as a Flask app that loads the precalculated amount medians on application launch and queries for state and zip code by IP address dynamically from an external service API.