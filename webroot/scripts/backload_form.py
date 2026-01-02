import pandas as pd
from db import get_db, insert_rows

db = get_db()
forms = pd.read_sql(query_forms, con=db)

for i, f in forms.iterrows():
    trans_avg_query = "SELECT form as id, org, AVG(amount) as trans_amount_mean, STD(amount) as trans_amount_std, AVG(hour) as trans_hour_mean, STD(hour) as trans_hour_std, AVG(day) as trans_day_mean, STD(day) as trans_day_std FROM transactions WHERE form={}".format(f['form'])
    trans_avg_data = pd.read_sql(trans_avg_query, con=db)
    print("row {}".format(i))
    print(trans_avg_data.values)
    insert_rows('form', data=trans_avg_data.values, columns=trans_avg_data.columns)
    print("\t\ttransaction averages updated")
