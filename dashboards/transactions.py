import sys
sys.path.append('../scripts/')
from s3_support import *

import dash, datetime
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_auth
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def dataframe_to_table(dataframe, max_rows=50, string_formatter=None):
    if string_formatter is None:
        string_formatter = "{}"
        
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def get_all_transaction_data():
    mean_trans_vol = "select avg(amount) from transactions where status='A'"
    mean_trans_vol_onetime = "select avg(amount) from transactions where status='A' and recurring=0"
    mean_trans_vol_recurring = "select avg(amount) from transactions where status='A' and recurring<>0"

    mean_trans_vol_source = "select source, avg(amount) from transactions where status='A' group by source"
    mean_trans_vol_source_onetime = "select source, avg(amount) from transactions where status='A' and recurring=0 group by source"
    mean_trans_vol_source_recurring = "select source, avg(amount) from transactions where status='A' and recurring<>0 group by source"

    return_data = {
        'mean_trans_vol': redshift_query_read(mean_trans_vol),
        'mean_trans_vol_onetime': redshift_query_read(mean_trans_vol_onetime),
        'mean_trans_vol_recurring': redshift_query_read(mean_trans_vol_recurring),
        'mean_trans_vol_source': redshift_query_read(mean_trans_vol_source),
        'mean_trans_vol_source_onetime': redshift_query_read(mean_trans_vol_source_onetime),
        'mean_trans_vol_source_recurring': redshift_query_read(mean_trans_vol_source_recurring),
    }
    
    return_data['mean_trans_vol_source']['avg'] = return_data['mean_trans_vol_source']['avg'].apply(lambda x: "${:.2f}".format(x))
    return_data['mean_trans_vol_source_onetime']['avg'] = return_data['mean_trans_vol_source_onetime']['avg'].apply(lambda x: "${:.2f}".format(x))
    return_data['mean_trans_vol_source_recurring']['avg'] = return_data['mean_trans_vol_source_recurring']['avg'].apply(lambda x: "${:.2f}".format(x))
    
    return_data['mean_trans_vol_source'] = return_data['mean_trans_vol_source'].merge(return_data['mean_trans_vol_source_onetime'], on="source").merge(return_data['mean_trans_vol_source_recurring'], on="source")
    return_data['mean_trans_vol_source'].columns = ['source', 'all', 'one time', 'recurring']
    
    return return_data


def get_volume_projection():
    q = '''select
                date_trunc('month', date) as month,
                count(id) as count,
                sum(amount) as volume,
                count(distinct org) as orgs
            from transactions
                where status='A'
                group by date_trunc('month', date)'''
    df = redshift_query_read(q)
    
    # prep & transform data
    df_all['month'] = pd.to_datetime(df_all['month'])
    df_all.sort_values('month', ascending=True, inplace=True)
    df_all = df_all[df_all['volume']>0.]

    df_all['cat_month'] = df_all['month'].dt.month
    df_all['count_growth'] = df_all['count'].diff() / df_all['count'].shift()
    df_all['volume_growth'] = df_all['volume'].diff() / df_all['volume'].shift()
    df_all['orgs_growth'] = df_all['orgs'].diff() / df_all['orgs'].shift()
    
    grpd = df_all.groupby('cat_month')[['count_growth', 'volume_growth', 'orgs_growth']].agg(['std', 'mean'])
    
    means = grpd['volume_growth']['mean']
    error = grpd['volume_growth']['std']
    
    current_volume = df_all['volume'].iloc[-1]
    projected_volume = last_volume + (last_volume * means[current_month])

    projected_high = projected_volume + (projected_volume * error[current_month])
    projected_low = projected_volume - (projected_volume * error[current_month])
    
    return {
        "current_volume": current_volume,
        "projected_volume": projected_volume,
        "projected_high": projected_high,
        "projected_low": projected_low
    }


def get_monthly_growth():
    query = '''select
                   date_trunc('month', date) as month,
                   100.0 * ((sum(amount) - lag(sum(amount), 1) over (order by date_trunc('month', date)  asc)) / lag(sum(amount), 1) over (order by date_trunc('month', date)  asc)) as sum_growth,
                   100.0 * ((cast(count(id) as float) - lag(cast(count(id) as float), 1) over (order by date_trunc('month', date)  asc)) / lag(cast(count(id) as float), 1) over (order by date_trunc('month', date)  asc)) as count_growth
            from transactions
            where status='A' and date_trunc('year', date)>=(extract(year from current_date) - 5)
            group by date_trunc('month', date)
            order by month asc'''
    df = redshift_query_read(query)
    
    df = df.iloc[-12:]
    df['sum_growth'] = df['sum_growth'].apply(lambda x: "{:.2f}%".format(x))
    df['count_growth'] = df['count_growth'].apply(lambda x: "{:.2f}%".format(x))
    
    return dcc.Graph(
            figure={
                'data': [
                    {
                        'x': df['month'].tolist(),
                        'y': df['sum_growth'].tolist(),
                        'name': '% Volume Growth',
                        'mode': 'line',
                        'marker': {'size': 2}
                    },
                    {
                        'x': df['month'].tolist(),
                        'y': df['count_growth'].tolist(),
                        'name': '% Count Growth',
                        'mode': 'line',
                        'marker': {'size': 2},
                    }
                ]
            }
        )
    

def get_yoy_data():
    yoy_vol_source = '''select
        source,
        sum(amount) as total_volume,
        sum(amount) / count(distinct form) as per_form_volume,
        sum(amount) / count(distinct org) as per_org_volume,
        count(distinct form) as form_count,
        count(distinct org) as org_count,
        extract(year from date) as year
    from transactions
    where status='A' group by extract(year from date), source order by year'''
    
    yoy = redshift_query_read(yoy_vol_source)
        
    return_div_children = []
    for source in yoy['source'].unique():
        _df = yoy[yoy['source']==source].copy()
    
        _df.sort_values('year', ascending=True, inplace=True)
        for c in _df.columns:
            if c != 'source' and c != 'year':
                _df["{}_growth".format(c)] = _df[c].diff() / _df[c].shift(1)
        for c in _df.columns:
            if 'growth' in c:
                _df[c] = (_df[c] * 100.).apply(lambda x: "{:.2f}%".format(x))
            elif 'volume' in c:
                _df[c] = _df[c].apply(lambda x: "${:,.2f}".format(x))
                
        text_cols = ['year'] + [c for c in _df.columns if 'growth' not in c and c != 'source' and c != 'year']
        
        if len(_df) > 2:
            _df = _df[_df['year']>=2010].iloc[2:]
        return_div_children.append(html.Div([
            html.H3(source),
            html.Div([
                html.Div(dataframe_to_table(_df[text_cols].tail(7)), className="six columns"),
                html.Div([dcc.Graph(
                    figure={
                        'data': [
                            {
                                'x': _df['year'].tolist(),
                                'y': _df['total_volume_growth'].tolist(),
                                'name': 'Total % Growth',
                                'mode': 'line',
                                'marker': {'size': 2}
                            },
                            {
                                'x': _df['year'].tolist(),
                                'y': _df['per_form_volume_growth'].tolist(),
                                'name': 'Per Form % Growth',
                                'mode': 'line',
                                'marker': {'size': 2}
                            },
                            {
                                'x': _df['year'].tolist(),
                                'y': _df['per_org_volume_growth'].tolist(),
                                'name': 'Per Org % Growth',
                                'mode': 'line',
                                'marker': {'size': 2}
                            },
                            {
                                'x': _df['year'].tolist(),
                                'y': _df['form_count_growth'].tolist(),
                                'name': 'Form Count % Growth',
                                'mode': 'line',
                                'marker': {'size': 2}
                            },
                            {
                                'x': _df['year'].tolist(),
                                'y': _df['org_count_growth'].tolist(),
                                'name': 'Org Count % Growth',
                                'mode': 'line',
                                'marker': {'size': 2}
                            }
                        ]
                    })], className="six columns"),
            ], className="row", style={'margin': '2em 1em'})
        ], className="row", style={'margin': '2em 1em'}))
    
    return return_div_children


def get_retention_data():
    ret = get_dataframe_from_file("qgiv-stats-data", "annual_retention.csv")
    ret['returning_donors'] = ret['annual_retention'].apply(lambda x: "{:.2f}%".format(x))
    
    table_el = dataframe_to_table(ret[['year', 'unique_donors', 'returning_donors']])
    
    return html.Div([
        html.Div(table_el, className="three columns"),
        html.Div([dcc.Graph(
            figure={
                'data': [
                    {
                        'x': ret['year'].tolist(),
                        'y': ret['unique_donors'].tolist(),
                        'name': 'Unique Donors',
                        'mode': 'line',
                        'marker': {'size': 2}
                    },
                    {
                        'x': ret['year'].tolist(),
                        'y': ret['annual_retention'].tolist(),
                        'name': '% Returning Donors',
                        'mode': 'line',
                        'marker': {'size': 2},
                        'yaxis': 'y2'
                    }
                ],
                'layout': go.Layout(
                    yaxis=dict(
                        title='Unique Donors'
                    ),
                    yaxis2=dict(
                        title='% Returning Donors',
                        overlaying='y',
                        side='right'
                    )
                )
            }
        ),  html.Span("* values calculated by averaging the values by individual organization")], className="nine columns"),
       
    ])
    
    
def get_donor_data():
    query = "select source, sum(amount) / cast(count(distinct email) as float) as volume, count(id) / cast(count(distinct email) as float) as count from transactions where status='A' group by source"
    ret = redshift_query_read(query)
    
    avg_trans_count = "{:.2f}".format(ret['count'].mean())
    avg_trans_value = "${:.2f}".format(ret['volume'].mean())
    
    ret['mean lifetime donor value'] = ret['volume'].apply(lambda x: "${:.2f}".format(x))
    ret['mean lifetime donor transactions'] = ret['count'].apply(lambda x: "{:.2f}".format(x))
    
    return html.Div([
        html.Div([
                html.Div([
                    html.Span('Avergae Lifetime Transaction Count Per Donor'), 
                    html.H3(avg_trans_count)
                ], className="six columns"),
                html.Div([
                    html.Span('Average Lifetime Value Per Donor'), 
                    html.H3(avg_trans_value)
                ], className="six columns")
        ], className="row", style={'margin': '2em 1em'}),
        html.Div([
            dataframe_to_table(ret.drop(['count', 'volume'], axis=1)),
            html.Span("* values calculated based upon all transactions without regard for transaction purpose or quality", style={'margin': '2em 0', 'display': 'block'})
        ], className="row", style={'margin': '2em 1em'})
    ])


def get_website_data():
    df = redshift_query_read("select * from org_websites")
    sources = [c.replace('iframe_source_', '') for c in df.columns if 'iframe' in c]
    
    source_presence_data = []
    for source in sources:
        rel_cols = [c for c in df.columns if source in c]
        presence = df[rel_cols].sum().sum() / float(len(df))
        source_presence_data.append({
            'source': source,
            'presence': presence * 100.
        })
    sp_df = pd.DataFrame(source_presence_data)[['source', 'presence']]
    sp_df['presence_raw'] = sp_df['presence']
    sp_df['presence'] = sp_df['presence_raw'].apply(lambda x: "{:.2f}%".format(x))
    
    social_sources = ['facebook', 'twitter', 'instagram']
    
    gen_stats_cols = ['calls_to_action', 'internal_links', 'outbound_links', 'word_count', 'image_count']

    gen_stats_df = df[gen_stats_cols].mean().reset_index()
    gen_stats_df.columns = ['stat', 'mean']
    gen_stats_df['stat'] = gen_stats_df['stat'].apply(lambda x: x.replace('_', ' '))
    gen_stats_df['mean'] = gen_stats_df['mean'].apply(lambda x: "{:,.2f}".format(x))
    
    competitor_presence = sp_df[(~sp_df['source'].isin(social_sources)&(sp_df['source']!='qgiv'))][['source', 'presence']]
    competitor_presence_all = sp_df[(~sp_df['source'].isin(social_sources)&(sp_df['source']!='qgiv'))]['presence_raw'].sum()
    social_presence = sp_df[sp_df['source'].isin(social_sources)]
    
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span('Our Presence per Page'), 
                html.H3(sp_df[sp_df['source']=='qgiv']['presence'])
            ], className="three columns"),
            html.Div([
                html.Span('Competitor Presence per Page'), 
                html.H3("{:.2f}%".format(competitor_presence_all))
            ], className="three columns"),
            html.Div([
                html.Span('Mean Social Presence per Page'), 
                html.H3("{:.2f}%".format(social_presence['presence_raw'].mean()))
            ], className="three columns"),
            html.Div([
                html.Span('Mean Calls to Action per Page'), 
                html.H3(gen_stats_df[gen_stats_df['stat']=='calls to action']['mean'])
            ], className="three columns")
        ], className="row"),
        html.Div([
            html.Div([
                html.Div([
                    dataframe_to_table(competitor_presence)
                ], className="four columns"),
                html.Div([
                    dataframe_to_table(social_presence[['source', 'presence']])
                ], className="four columns"),
                html.Div([
                    dataframe_to_table(gen_stats_df)
                ], className="four columns")
            ], className="row", style={'margin': '2em 1em'}),
            html.Span("* presence is calculated as a percentage of first level linked pages from active client websites with links, iframes, or javascripts included to or from the given domain")
        ], className="row")
    ], style={"margin": "2em 1em"})


def get_general_processing_data():
    # query data
    data = get_all_transaction_data()

    return html.Div([
        html.Div([
            html.Div([
                html.Span('Mean Transaction Value'), 
                html.H3("${:.2f}".format(data['mean_trans_vol']['avg'].iloc[0]))
            ], className="four columns"),
            html.Div([
                html.Span('Mean One Time Transaction Value'), 
                html.H3("${:.2f}".format(data['mean_trans_vol_onetime']['avg'].iloc[0]))
            ], className="four columns"),
            html.Div([
                html.Span('Mean Recurring Transaction Value'), 
                html.H3("${:.2f}".format(data['mean_trans_vol_recurring']['avg'].iloc[0]))
            ], className="four columns"),
        ], className="row", style={'margin': '2em 1em'}),
        html.Div([
            html.Div([
                html.H5("Mean Transaction Value by Source"),
                dataframe_to_table(data['mean_trans_vol_source'])
            ], className="four columns"),
            html.Div([
                html.H5("Monthly YoY Transaction Growth"),
                get_monthly_growth()
            ], className="eight columns")
        ], className="row", style={'margin': '2em 1em'})
    ])

app.layout = html.Div([
    dcc.Tabs(id='tabs-select', value="tab-general", children=[
        dcc.Tab(label='General Transactions (All)', value="tab-general"),
        dcc.Tab(label="YoY By Source", value="tab-yoy-source"),
        dcc.Tab(label="Retention", value="tab-retention"),
        dcc.Tab(label="Donors", value="tab-donor"),
        dcc.Tab(label="Client Websites", value="tab-website")
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'), [Input('tabs-select', 'value')])
def render_content(tab):
    if tab == 'tab-general':
        return get_general_processing_data()
    elif tab == 'tab-yoy-source':
        return get_yoy_data()
    elif tab == 'tab-retention':
        return get_retention_data()
    elif tab == 'tab-donor':
        return get_donor_data()
    elif tab == 'tab-website':
        return get_website_data()


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port="8040")
    
    
