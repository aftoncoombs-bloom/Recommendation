# Org Insights Comparison (Prototype)

## Operation

Script filename: api.org_insights.py

**Test URL:**

- (GET) https://orginsights.qgiv.com/test/

Can be used to verify service availability. The test URL does not respond to input, but will import certain libraries and execute a database query to verify the basic requisite operations necessary to perform the intended service are functioning as expected.

### Output

```
{
  "message": "10 entries retreived",
  "success": "1"
}
```

**Target URL:**

- (POST) https://orginsights.qgiv.com/orginsights/

### Input

_Supported insights and filters are limited in the prototype_

POST

- insights: (str) comma separated list of insights to be calculated; currently supported values are 'contribution_total', 'contribution_count', 'average_contribution_amount', 'median_contribution_amount'
- timeframe: (str) optional timeframe within which to query; supported values are '1week', '1month', '3months', '6months', '1year'
- segment: (str) optional case insensitive substring of segment tag 

```
$params = array(
    'insights' => 'contribution_total,average_contribution_amount',
    'timeframe' => '3months',
    'segment' => 'youth'
);
```

### Output

JSON output

- success: (int)
- stats: (array)
    - insight: (str) the given insight calculated
    - stat: (float) the calculation given the provided filters
    
```
{
    'success': '1',
    'stats': [
        {'insight': 'contribution_total', 'stat': '16,078.56'},
        {'insight': 'average_contribution_amount', 'stat': '67.16'}
    ]
}
```

