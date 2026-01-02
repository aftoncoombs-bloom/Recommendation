Looking at the relationship between P2P event fields & amount counts to donation & registration counts.

Value counts

| Count | Amounts | Fields |
|-------|---------|--------|
| 0     |   2311  | 94115  |
| 1     |    453  | 59935  |
| 2     |      6  | 39650  |
| 3     |   8858  | 24811  |
| 4     | 127571  | 13617  |
| 5     |  70206  | 12575  |
| 6     |  34186  |  6173  |
| 7     |  10965  |  1032  |
| 8     |   5489  |  2475  |
| 9     |   1765  |  2778  |
| 10    |   3701  |  2713  |
| 11    |   1338  |   787  |
| 12    |    851  |  1914  |
| 13    |      0  |  3442  |
| 16    |      0  |   402  |
| 21    |      0  |  1070  |
| 26    |    396  |     0  |
| 27    |      0  |   607  |

# Relationships to registration data

Correlations

| feature | corr reg count | corr reg amount |
|---------|----------------|-----------------|
| amounts |   -0.001331    |    0.003110     |
| fields  |   -0.000994    |    0.002158     |


Random forest feature importance modeling against registration count

| Feature | Importance |
|---------|------------|
| amount  | 0.1114771  |
| fields  | 0.0968182  |

The correlations are weak, the value counts fairly evenly distributed, and the feature importances are not significant. The amount & fields counts certainly contribute something slightly meaningful to the prediction but there is no relationship making itself evident in the other metrics. Additionally, I'm not convinced that these values would have any real-world impact on registration counts as they seem a very low bar given the effort required to throughout the rest of the process.

# Relationships to donation data

Correlations

| feature | correlation |
|---------|-------------|
| fields  | -0.026774   |
| amount  | -0.029991   |

Random forest feature importance to donation count

| Feature | Importance |
|---------|------------|
| amount  | 0.0440238  |
| fields  | 0.0250377  |

Here we again see fairly weak relationships and, in this case, the feature importances are even weaker. My assumption would be that the amount & field counts would impact the donations far more than registrations but the relationship appears to be even weaker here than with registrations.

The metrics are not revealing anything interesting and reviewing the illustrations paints a picture of these values being randomly distributed with little to no indication of a predictive relationship. Not really seeing anything significant here, so moving along, nothing to see.

Notebooks:
- [donation count modeling](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/Donation%20Count%20Modeling.ipynb)
- [registation data exploration](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/registation%20data%20exploration.ipynb)
- [amounts and fields explortion](https://github.com/Qgiv/Recommendation/blob/master/notes/form%20health/p2p/amounts%20and%20fields%20exploration.ipynb)