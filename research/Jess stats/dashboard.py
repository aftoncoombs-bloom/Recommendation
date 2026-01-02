import sys
sys.path.insert(1, '../../scripts/')
from s3_support import *

import pandas as pd

from dash import Dash, dcc, html, Input, Output, callback
from dash.dash_table import DataTable, FormatTemplate


# load org data
q = '''select month from production.stats where month>=dateadd(year, -1, current_date)'''
#months = redshift_query_read(q, schema='production')['month'].tolist()

#from dash_extensions.snippets import send_data_frame


# load monthly system data
df = pd.read_csv("dashboard.stats.csv").sort_values('month', ascending=True)
months = df['month'].tolist()

df['conversion_onetime'] = (df['trans_onetime'] / df['pageviews'])
df['conversion_recurring'] = (df['trans_rec_origin'] / df['pageviews'])
df['conversion'] = df['conversion_onetime'] + df['conversion_recurring']

df['conversion_desktop'] = (df['trans_count_desktop'] / df['pageviews_desktop'])
df['conversion_mobile'] = (df['trans_count_mobile'] / df['pageviews_mobile'])

columns = df.columns

# load form data
df_forms = pd.read_csv("dashboard.stats_forms.csv")

df_forms['conversion_onetime'] = (df_forms['trans_onetime_count'] / df_forms['pageviews'])
df_forms['conversion_recurring'] = (df_forms['trans_rec_origin_count'] / df_forms['pageviews'])
df_forms['conversion'] = df_forms['conversion_onetime'] + df_forms['conversion_recurring']
df_forms['conversion_desktop'] = (df_forms['trans_count_desktop'] / df_forms['pageviews_desktop'])
df_forms['conversion_mobile'] = (df_forms['trans_count_mobile'] / df_forms['pageviews_mobile'])

columns_forms = df_forms.columns

# load cool stuff data
df_cool_stuff_daily = pd.read_csv("cool.daily.csv")
cool_stuff_monthly = pd.read_csv("cool.monthly.csv")
cool_stuff_monthly['dt.month'] = pd.to_datetime(cool_stuff_monthly['month']).dt.month
cool_stuff_monthly.sort_values('month', ascending=True, inplace=True)
yoy = cool_stuff_monthly.drop('month', axis=1).groupby('dt.month').pct_change()
yoy['month'] = cool_stuff_monthly['month']
cool_stuff_monthly.drop('dt.month', axis=1, inplace=True)

cool_monthly_data = []
for month in yoy['month'].to_list():
    entry = {'month': month}
    
    for c in yoy.columns:
        if c != 'month':
            val = cool_stuff_monthly[cool_stuff_monthly['month']==month][c].iloc[0]
            change = yoy[yoy['month']==month][c].iloc[0]
            if 'vol' in c:
                entry[c] = "${:,.2f} ({:.2f}%)".format(val, change * 100.)
            else:
                entry[c] = "{:,} ({:.2f}%)".format(val, change * 100.)
    
    cool_monthly_data.append(entry)
df_cool_monthly = pd.DataFrame(cool_monthly_data).tail(12)
df_cool_monthly_cols = ['month'] + [c for c in df_cool_monthly.columns if c != 'month']


app = Dash(__name__, 
           assets_external_path='https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css')
           
features_used = ['Express Donate', 'Gift Assist', 'CTA Before', 'CTA After', 'Conditional Fields']
products_used = ['Year Round', 'P2P', 'Auction']
segments = df_forms['ntee'].unique().tolist()

formatter_money = FormatTemplate.money(2)
formatter_percentage = FormatTemplate.percentage(2)

'''
base layout
'''

app.layout = html.Div([
    dcc.Tabs(id='tabs', value='system', children=[
        dcc.Tab(label='System Wide', value='system'),
        dcc.Tab(label='Forms Averages', value='forms'),
        dcc.Tab(label='Mini Cool Stuff', value='cool')
    ]),
    html.Div(id='tabs-content', children=[
        # org tab
        html.Div(id='tab-system', children=[
            html.Div([
                html.Div([
                    html.Label('Start Date'),
                    dcc.Dropdown(months, months[-6], id='system-start-date'),
                ], style={'flex': 1, 'padding': '10px'}),
                html.Div([
                    html.Label('End Date'),
                    dcc.Dropdown(months, months[-1], id='system-end-date')
                ], style={'flex': 1, 'padding': '10px'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'padding-bottom': '10px'}),

            html.Div([
                DataTable(
                    id='table-system',
                    fixed_rows={'headers': True},
                    fixed_columns={'headers': True, 'data': 1},
                    style_table={'minWidth': '100%', 'height': '100%'},
                    style_cell={'padding': '10px'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f2f2f2',
                        },
                        {
                            'if': {'column_id': 'index'},
                            'backgroundColor': '#f2f2f2'
                        }
                    ],
                )
            ]),

            html.Div([
                html.Div([
                    html.Label('Table Columns'),
                    dcc.Checklist(columns[1:], columns, id='system-fields', style={'column-count': '3'})
                ])
            ], style={'display': 'flex', 'flexDirection': 'row', 'padding': '10px'})
        ]),
        # forms tab
        html.Div(id='tab-forms', children=[
            html.Div([
                html.Div([
                    html.Label('Dataset'),
                    dcc.RadioItems(['All', 'Representative Forms'], 'All', id='rep-filter')
                ], style={'padding': '10px'}),
                html.Div([
                    html.Label('Start Date'),
                    dcc.Dropdown(months, months[-6], id='forms-start-date'),
                ], style={'flex': 1, 'padding': '10px'}),
                html.Div([
                    html.Label('End Date'),
                    dcc.Dropdown(months, months[-1], id='forms-end-date')
                ], style={'flex': 1, 'padding': '10px'}),
                '''
                html.Div([
                    html.Button("Download CSV", id="btn_csv"),
                    dcc.Download(id="download-csv")
                ])
                '''
            ], style={'display': 'flex', 'flexDirection': 'row', 'padding-bottom': '10px'}),

            html.Div([
                DataTable(
                    id='table-forms',
                    fixed_rows={'headers': True},
                    fixed_columns={'headers': True, 'data': 1},
                    style_table={'minWidth': '100%'},
                    style_cell={'padding': '10px'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f2f2f2',
                        },
                        {
                            'if': {'column_id': 'index'},
                            'backgroundColor': '#f2f2f2'
                        }
                    ],
                )
            ], style={'padding': '10px'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label('Table Columns'),
                        dcc.Checklist(columns_forms[1:], columns_forms, id='forms-fields', style={'column-count': '3'})
                    ])
                ], style={'padding': '10px'}),
                html.Div([
                    html.Div([
                        html.Label('Filter to only forms using the features:'),
                        dcc.Dropdown(features_used, [], id='forms-features-used', multi=True)
                    ], style={'flex': 1, 'padding': '10px'}),
                    html.Div([
                        html.Label('Include products:'),
                        dcc.Dropdown(products_used, products_used, id='forms-products-used', multi=True)
                    ], style={'flex': 1, 'padding': '10px'}),
                    html.Div([
                        html.Label('Include NTEE:'),
                        dcc.Dropdown(["All"] + segments, ["All"], id='forms-ntee', multi=True)
                    ], style={'flex': 1, 'padding': '10px'})
                ], style={'flex': 1, 'padding': '10px'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'padding': '10px'})
        ]),
        # cool stuff tab
        html.Div(id='tab-cool', children=[
            html.Div([
                DataTable(
                    id='table-cool-daily',
                    fixed_rows={'headers': True},
                    fixed_columns={'headers': True, 'data': 1},
                    style_table={'minWidth': '100%'},
                    style_cell={'padding': '10px'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f2f2f2',
                        },
                        {
                            'if': {'column_id': 'index'},
                            'backgroundColor': '#f2f2f2'
                        }
                    ],
                    columns=[{'name': c.replace("_", ' '), 
                              'id': c.lower().replace(" ", '_')} for c in df_cool_stuff_daily.columns],
                    data=df_cool_stuff_daily.to_dict('records')
                )
            ], style={'padding': '10px'}),
            html.Div([
                DataTable(
                    id='table-cool-monthly',
                    fixed_rows={'headers': True},
                    fixed_columns={'headers': True, 'data': 1},
                    style_table={'minWidth': '100%'},
                    style_cell={'padding': '10px'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f2f2f2',
                        },
                        {
                            'if': {'column_id': 'index'},
                            'backgroundColor': '#f2f2f2'
                        }
                    ],
                    columns=[{'name': c.replace("_", ' '), 
                              'id': c.lower().replace(" ", '_')} for c in df_cool_monthly_cols],
                    data=df_cool_monthly[df_cool_monthly_cols].to_dict('records')
                )
            ], style={'padding': '10px'}),
        ])
    ]),

    html.Div(id='explanations-content', children=[
        dcc.Markdown('''
            - list items including the term _new_ are to indicate the exclusion of past recurring transactions; ie, both __trans count__ and __trans new count__ will include one time transactions, but __trans count__ will include transactions for recurring that were created prior to the given month whereas __trans new count__ will only include recurring that were created during the given month
            - __trans rec origin__ is a reference to recurring that is created during the given month; ie, this is the number of recurring that _originated_ during the given month
        ''')
    ])
])


'''
callbacks
'''


@callback([Output('tab-system', 'style'), Output('tab-forms', 'style'), Output('tab-cool', 'style')], Input('tabs', 'value'))
def render_tab_content(tab='system'):
    on = {'display': 'block'}
    off = {'display': 'none'}

    if tab == 'system':
        return on, off, off
    elif tab == 'forms':
        return off, on, off
    elif tab == 'cool':
        return off, off, on
    

@callback([Output('table-system', 'columns'), Output('table-system', 'data')], 
          [Input('system-fields', 'value'), Input('system-start-date', 'value'), 
           Input('system-end-date', 'value')])
def temp_update_system_table(column_filter, start_date, end_date):
    new_cols = [c for c in df.columns if c in column_filter]
    # isolate dataset to checked columns
    data = df[(df['month']>=start_date)&(df['month']<=end_date)][new_cols]
    
    # string formatting values
    for c in data.columns:
        if c not in ['month']:
            formatter = column_formatter(c)
            data[c] = data[c].apply(lambda x: formatter.format(x))
    
    # transpose & index fix
    data = data.transpose()
    data.columns = data.loc['month']
    data = data.drop(index='month').reset_index()

    cols = [{'name': str(c).replace("_", ' '),
            'id': str(c).lower().replace(" ", '_')} for c in data.columns]
    
    data['index'] = data['index'].apply(lambda x: x.replace('_', ' '))
    
    return cols, data.reset_index().to_dict('records')


#@callback(Output('table-system', 'data'), [Input('form-filter', 'value'), Input('table-fields', 'value')])
def update_system_table(form_filter, column_filter, start_date, end_date):
    # @TODO address filter of representative forms
    # filter start/end dates in query
    q = "select * from production.stats where month>='{}' and month<='{}'".format(start_date, end_date)
    df = redshift_query_read(q, schema='production')

    data = df[column_filter].to_dict('records')

    return df.to_dict('records')


@callback([Output('table-forms', 'columns'), Output('table-forms', 'data')], 
          [Input('rep-filter', 'value'), Input('forms-start-date', 'value'), 
           Input('forms-end-date', 'value'), Input('forms-fields', 'value'),
           Input('forms-features-used', 'value'), Input('forms-products-used', 'value'),
           Input('forms-ntee', 'value')])
def update_forms_table(rep_filter, start_date, end_date, column_filter, features_used, products_used, ntee_filter):
    new_cols = [c for c in df_forms.columns if c in column_filter]
    
    # date filter & representative forms filter
    data = df_forms[(df_forms['month']>=start_date)&(df_forms['month']<=end_date)]
        
    if rep_filter != 'All':
        data = data[data['rep_forms']==1]
        
    if "All" not in ntee_filter:
        data = data[data['ntee'].isin(ntee_filter)]
    
    # products used filter
    if 'Year Round' not in products_used or 'P2P' not in products_used or 'Auction' not in products_used:
        print("filtering product type")
        product_params = []
        for f in products_used:
            if f == 'Year Round':
                product_params.append(1)
            elif f == 'P2P':
                product_params.append(3)
            elif f == 'Auction':
                product_params.append(5)
        data = data[data['product'].isin(product_params)]
    
    # express donate filter
    if 'Express Donate' in features_used:
        ep_forms = data[data['expressdonate_count']>0]['form'].unique().tolist()
        data = data[data['form'].isin(ep_forms)]
    
    # gift assist filter
    if 'Gift Assist' in features_used:
        ga_forms = data[data['giftassist_count']>0]['form'].unique().tolist()
        data = data[data['form'].isin(ga_forms)]
        
    # CTA filter
    if 'CTA Before' in features_used:
        data = data[data['cta_before']==1]
    if 'CTA After' in features_used:
        data = data[data['cta_after']==1]
        
    # conditional fields filter
    if 'Conditional Fields' in features_used:
        data = data[data['conditional_fields']>0]
        
    agg_rule = {}
    for c in data.columns:
        if c not in ['month', 'product', 'frontend_template', 'rep_forms', 'ntee']:
            if c in ['form']:
                agg_rule[c] = 'nunique'
            else:
                agg_rule[c] = 'mean'
    
    # group by month and average values
    grpd = data.groupby('month').agg(agg_rule).reset_index()

    # gift assist adoption rate
    data_ga = data[data['giftassist_count']>0]
    data_ga['giftassist_adoption'] = data_ga['giftassist_count'] / (data_ga['trans_onetime_count'] + data_ga['trans_rec_origin_count'])
    grpd_ga = data_ga.groupby('month')['giftassist_adoption'].mean().reset_index()
    grpd = grpd.merge(grpd_ga, on='month')

    # forms using conditional fields
    data_cf = data[data['conditional_fields']>0]
    grpd_cf = data_cf.groupby('month')['form'].nunique().reset_index()
    grpd_cf.columns = ['month', 'forms_using_conditional_fields']
    grpd = grpd.merge(grpd_cf, on='month')
    grpd_cf = data_cf.groupby('month')['trans_vol'].agg(['sum', 'mean']).reset_index()
    grpd_cf.columns = ['month', 'conditional_fields_vol', 'conditional_fields_vol_mean']
    grpd = grpd.merge(grpd_cf, on='month')
    
    # converstion fix to filter >100% entries & entries with page views
    conv_cols = ['conversion', 'conversion_onetime', 'conversion_recurring', 'conversion_desktop', 'conversion_mobile']
    grpd.drop(conv_cols, axis=1, inplace=True)
    grpd_conv = data[(data['conversion']<1.)&(data['pageviews']>0)].groupby('month')[conv_cols].mean().reset_index()
    grpd = grpd.merge(grpd_conv, on='month')

    # embeds data points
    grpd_embeds = data.groupby(['month', 'is_embed'])['trans_vol'].agg(['sum', 'mean', 'median']).reset_index()
    pvt_embeds = grpd_embeds.pivot(index='month', columns='is_embed', values=['sum', 'mean', 'median']).reset_index()
    cols = ['month', 
            'nonembed_vol', 'embed_vol',
            'nonembed_vol_mean', 'embed_vol_mean',
            'nonembed_vol_median', 'embed_vol_median']
    pvt_embeds.columns = cols
    grpd = grpd.merge(pvt_embeds, on='month')
    
    # string formatting values
    for c in grpd.columns:
        if c not in ['month']:
            formatter = column_formatter(c)
            grpd[c] = grpd[c].apply(lambda x: formatter.format(x))
    
    # transpose and format fix
    data = grpd.transpose()
    data.columns = data.loc['month']
    data = data.drop(index='month').reset_index()
    data['index'] = data['index'].apply(lambda x: x.replace('_', ' ').replace('mdn', 'median'))

    # month columns list
    cols = [{'name': c.replace("_", ' '), 
            'id': c.lower().replace(" ", '_')} for c in data.columns]

    return cols, data.reset_index().to_dict('records')


'''
@callback(
    Output("download-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    return dcc.send_data_frame(df.to_csv, "dashboard.stats.csv")
'''

def column_formatter(column_name: str) -> dict:
    if 'vol' in column_name or 'trans_avg' in column_name:
        # currency format
        return "${:,.2f}"
    elif 'conversion' in column_name:
        # percentage format
        return "{:,.2%}"
    elif column_name in ['forms', 'form', 'orgs']:
        return "{:,.0f}"
    else:
        # float format
        return "{:,.2f}"


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port="8050", debug=True)
