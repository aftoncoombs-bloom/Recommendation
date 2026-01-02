```{r}
source('~/Repositories/git.recommendation/notebooksconversion-load-n-cleanup.R')
analytic_data[is.na(analytic_data$don_form_trans_vol),]$don_form_trans_vol = 0

agg.trans_vol = aggregate(don_form_trans_vol ~ amounts_system, data=analytic_data, FUN=mean)

agg.trans_vol
  multirestriction_system don_form_trans_vol
1                       0           15.08958
2                       1          196.83888

agg.trans_count = aggregate(don_form_trans_count ~ amounts_system, data=analytic_data, FUN=mean)

agg.trans_count
  multirestriction_system don_form_trans_count
1                       0           0.07535433
2                       1           1.05733773

agg.conversion = aggregate(conversion ~ multirestriction_system, data=analytic_data, FUN=mean)

agg.conversion
  multirestriction_system conversion
1                       0   1.929562
2                       1   7.260923



# mean transaction value for multirestriction
196.83888/1.05733773
[1] 186.1646
# mean transaction value for amounts
15.08958/0.07535433
[1] 200.2483
# percentage funds raised amounts vs multirestriction
15.08958/196.83888
[1] 0.07665955
```

Looks like multirestriction forms are raising, on average, much more per 6 hours than amounts forms, but the average transaction value for amounts system is slightly higher.

----------------------------------------------------------  
|                         | **Amounts**    | **Multirestriction** |
|--------------------------|:--------------:|-----------------:|
| **Mean Transaction Count**  | 0.07535433 | 1.05733773       |
| **Mean Funding Volume**     | 15.08958  | 196.83888       |
| **Mean Transaction Volume** | 200.2483  | 186.1646        |
| **Mean Conversion**         | 1.929562%  | 7.260923%        |