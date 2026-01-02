import pandas as pd
from db import insert_dataframe

counter = 1

for chunk in pd.read_csv("/home/jeremy/a_base.csv", chunksize=1000):
    for c in chunk.columns:
        if 'Unnamed' in c:
            chunk.drop(c, axis=1, inplace=True)
    
    chunk.fillna('', inplace=True)

    insert_dataframe('analytics_base', chunk)
    print("Inserted "+str(counter*1000))
    counter = counter + 1
