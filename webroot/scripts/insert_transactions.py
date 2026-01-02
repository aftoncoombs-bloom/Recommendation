import pandas as pd
from db import insert_dataframe

for chunk in pd.read_csv("/home/jeremy/trans.csv", chunksize=100):
    for c in chunk.columns:
        if 'Unnamed' in c:
            chunk.drop(c, axis=1, inplace=True)
    
    chunk.fillna('', inplace=True)

    insert_dataframe('transactions', chunk)

'''
3674853 rows inserted into table

3675346
'''