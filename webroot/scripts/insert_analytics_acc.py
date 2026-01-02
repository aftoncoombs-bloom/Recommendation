import pandas as pd
from db import insert_dataframe

counter = 1

for chunk in pd.read_csv("/home/jeremy/analytics_qgiv.csv", chunksize=10000):
    for c in chunk.columns:
        if 'Unnamed' in c:
            chunk.drop(c, axis=1, inplace=True)
    chunk.drop('new_rec_volume.1', axis=1, inplace=True)
    
    chunk.fillna('', inplace=True)

    insert_dataframe('analytics_qgiv', chunk)
    print("Qgiv: Inserted "+str(counter*10000))
    counter = counter + 1

counter = 1

for chunk in pd.read_csv("/home/jeremy/analytics_p2p.csv", chunksize=10000):
    for c in chunk.columns:
        if 'Unnamed' in c:
            chunk.drop(c, axis=1, inplace=True)
    
    chunk.fillna('', inplace=True)

    insert_dataframe('analytics_p2p', chunk)
    print("P2P: Inserted "+str(counter*10000))
    counter = counter + 1