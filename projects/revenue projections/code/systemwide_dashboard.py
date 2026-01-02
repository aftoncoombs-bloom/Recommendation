import dash, dash_table, sys
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(1, '../../../scripts/')
from s3_support import *


# load data
q = '''select
            count(id) as count,
            sum(amount) as volume,
            date_trunc('month', date) as month,
            count(distinct org) as orgs
        from transactions
            where status='A'
            group by date_trunc('month', date)'''
df_all = redshift_query_read(q)

# prep & transform data
df_all['month'] = pd.to_datetime(df_all['month'])
df_all.sort_values('month', ascending=True, inplace=True)
df_all = df_all[df_all['volume']>0.]

df_all['cat_month'] = df_all['month'].dt.month
df_all['count_growth'] = df_all['count'].diff() / df_all['count'].shift()
df_all['volume_growth'] = df_all['volume'].diff() / df_all['volume'].shift()
df_all['orgs_growth'] = df_all['orgs'].diff() / df_all['orgs'].shift()

grpd = df_all.groupby('cat_month')[['count_growth', 'volume_growth', 'orgs_growth']].agg(['std', 'mean'])

fig_vol = go.Figure()
fig_vol.add_trace(go.Scatter(
    x=grpd.index,
    y=grpd['volume_growth']['mean'],
    name="Current"
))
fig_vol.update_traces(mode="lines")


# start building dashboard
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children="System Wide Expected growth"),
    
    html.H2(children="Transaction Volume"),
    html.Div([dcc.Graph(figure=fig_vol)]),
    
    html.H2(children="Transaction Count"),
    
    html.H2(children="Active Organizations")
])

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port="8060")