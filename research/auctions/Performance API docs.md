# Auction Item Score

## Concept

To assign a performance score to an auction item based upon settings and bidding performance.

### Operation

#### Training

Requires pre-calculating the median bids per auction item. This will be done inside the script automatically, sunsetting the value and re-calculating when the script revognizes that the value is more than 1 week old.

**Target URL:***

- (POST) https://52.2.34.90:8899/auctionitemscore/

#### Input

- value: (float) value of the given item provided by the admin
- bid_increment: (float)
- reserve: (float)
- bids: (int) total number of bids placed on the item
- winning_bid: (float) value of the winning bid

```
$params = array(
    'value' => 100.00,
    'bid_increment' => 10.00,
    'reserve' => 25.00,
    'bids' => 37,
    'winning_bid' => 75.00
);
```

#### Output

```
{
    "status": 1,
    "data": 0.75
}
```

## API

__Files__

1. api.performance_score.py: Flask app file to run the API endpoint