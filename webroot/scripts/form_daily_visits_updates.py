from db import update_rows, get_db
import pandas as pd

query = 'select form, date, sum(views) as views from ga_form where form > 0 group by form, date'

db = get_db()
forms = pd.read_sql(query, con=db)

print("Updating for {} form entries".format(len(forms)))

    if i > 73000:
    # update_rows(table, data=[], columns=[], where=None)
    if f['views'] is None or f['form'] == 0 or f['form'] is None:
        continue

    update_rows('form_daily', 
        data=[[f['views']]],
        columns=['visits'], 
        where="form={} and date={}".format(f['form'], str(f['date'])))

    if i % 1000 == 0:
        print("done with {} entries".format(i))