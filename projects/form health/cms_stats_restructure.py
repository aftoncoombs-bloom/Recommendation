import pandas as pd

df = pd.read_csv("~/Repositories/datasets/cmsdata/cms_data.visited.csv")
df.type.unique()

df['24'] = 0
df['22'] = 0
df['15'] = 0
df['14'] = 0
df['54'] = 0
df['21'] = 0
df['25'] = 0
df['17'] = 0
df['18'] = 0
df['19'] = 0
df['23'] = 0
df['20'] = 0

unique_stats = df.stats.unique()
stats_len = len(unique_stats)
counter = 0

for s in unique_stats:
    counter = counter + 1
    for widget in ['24', '22', '15', '14', '54', '21', '25', '17', '18', '19', '23', '20']:
        df.loc[df.stats==s, str(widget)] = df[(df.stats==s) & (df.type==int(widget))].weight
    print("Done with "+str(counter)+" stats entry out of "+str(stats_len))
df = df.groupby('stats').max()

df.to_csv("~/Repositories/datasets/cms_data.restructured.csv")