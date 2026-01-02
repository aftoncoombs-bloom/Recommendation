import pandas as pd
from db import update_rows, insert_rows

df = pd.read_csv("/home/jeremy/form_paths.csv")

print("Updates for {} forms".format(len(df)))

for index, row in df.iterrows():
    form_key = row[2].strip()
    query_where = "path LIKE '%%event/{}/%%' or path LIKE '%%for/{}/%%'".format(form_key, form_key)

    update_rows('ga_form', data=[[row[1]]], columns=['form'], where=query_where)
    update_rows('ga_accounts', data=[[row[1]]], columns=['form'], where=query_where)

    if index % 1000 == 0:
        print("Done with {} forms".format(index))