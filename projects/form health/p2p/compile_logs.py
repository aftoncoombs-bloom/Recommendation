import pandas as pd
import pickle, os
from StringIO import StringIO

os.chdir("/Users/jeremyvanvalkenburg/Repositories/datasets/logs/")

filename = "logs_{}.csv"
i = 1
df = None

while True:
    try:
        print("Working on file {}".format(i))
        if df is None:
            df = pd.read_csv(filename.format(i))
        else:
            new_df = pd.read_csv(filename.format(i), error_bad_lines=False)
            df = df.append(new_df)
            
        i += 1
    except:
        print("Writing df to csv")
        df.to_csv(filename.format("all"))
        break