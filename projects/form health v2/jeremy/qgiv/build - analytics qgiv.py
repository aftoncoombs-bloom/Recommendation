import pandas as pd
import numpy as np
import time

import sys
sys.path.insert(1, '../../../../scripts/')
from s3_support import *


print("Pulling form subset")
q = "select distinct form from analyticsqgiv_weekly"
forms = redshift_query_read(q)
sample_forms = forms.sample(frac=.5)['form'].tolist()
# test with all forms
sample_forms = forms['form'].tolist()

print("\tall forms: {}; subset forms: {}".format(len(forms), len(sample_forms)))


print("Pulling base analytics")
start_time = time.time()

q = '''select * from analyticsqgiv_weekly where date>2018'''
df_qgiv = redshift_query_read(q)
df_qgiv = df_qgiv[df_qgiv['form'].isin(sample_forms)]

end_time = time.time()
print("\t{} rows; query took {:.2f} seconds".format(len(df_qgiv), end_time - start_time))


print("Pulling qgiv analytics")
start_time = time.time()

q = '''select * from analytics_weekly where date>2018'''
df_base = redshift_query_read(q)
df_base = df_base[df_base['form'].isin(sample_forms)]

end_time = time.time()
print("\t{} rows; query took {:.2f} seconds".format(len(df_base), end_time - start_time))


print("Merging base & qgiv analytics")
qgiv_data = df_qgiv.merge(df_base, on=["date", "form", "org"])

print("\t{} base rows; {} qgiv rows; {} merged rows".format(len(df_base), len(df_qgiv), len(qgiv_data)))


print("Storing to S3")
save_dataframe_to_file("qgivmodelsdata", "analytics_qgiv.2019.csv", qgiv_data)