import pandas as pd

import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *


print("loading 2020 data")
# 2020 data
gt_2020 = '2020-12-01'
q = "select sum(amount), count(id), count(distinct(id)) from transactions where (date='{}' or (date='{}' and hour<=3)) and (status='A' or status='P')".format(gt_2020, '2020-12-02')
q = "select sum(amount), count(id), count(distinct(id)) from transactions where date='{}' and status='A'".format(gt_2020)
df_2020 = redshift_query_read(q, schema='production')

print("loading 2021 data")
# 2021 data
gt_2021 = '2021-11-30'
q = "select sum(amount), max(amount), avg(amount), count(id), count(distinct(id)) as count_distinct from transactions where (date='{}' or (date='{}' and hour<=3)) and (status='A' or status='P')".format(gt_2021, '2021-12-01')
q = "select sum(amount), max(amount), avg(amount), count(id), count(distinct(id)) as count_distinct from transactions where date='{}' and status='A'".format(gt_2021)
df_2021 = redshift_query_read(q, schema='production')

# calculations
perc_of_2020 = df_2021['sum'].iloc[0] / df_2020['sum'].iloc[0]
largest_donation = df_2021['max'].iloc[0]
avg_donation = df_2021['avg'].iloc[0]
count_donations = df_2021['count_distinct'].iloc[0]

# counting acceptiva
acceptiva = pd.read_csv("trans_440.csv")
total_count = df_2021['count_distinct'].iloc[0] + len(acceptiva)
total_sum = df_2021['sum'].iloc[0] + acceptiva['total'].sum()

print()
print("Report:")
print("Sum: ${:,.2f}".format(df_2021['sum'].iloc[0]))
print("% of 2020: {:.2f}%".format(perc_of_2020 * 100.))
print("Largest donation: ${:,.2f}".format(largest_donation))
print("Average donation: ${:,.2f}".format(avg_donation))
print("Total number of donations: {:,}".format(count_donations))

print()
print("Including Acceptiva")
print("Sum: ${:,.2f}".format(total_sum))
print("% of 2020 (qgiv only): {:.2f}%".format((total_sum / df_2020['sum'].iloc[0]) * 100.))
print("% of 2020 (qgiv & acceptiva): {:.2f}%".format((total_sum / (df_2020['sum'].iloc[0] + 1445407.86)) * 100.))
print("Average donation: ${:,.2f}".format(total_sum / total_count))
print("Total number of donations: {:,}".format(total_count))
