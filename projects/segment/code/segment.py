import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import sys
sys.path.insert(1, '../../../scripts/')
from s3_support import *
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

def get_user_page():
    # retrieve data
    q = "select id, uuid, org, name, timestamp 'epoch' + created_at * interval '1 second' as created_at, user_type, total_forms, donation_forms, status, p2p_events, political_forms from users order by created_at desc"
    df_users = redshift_query_read(q, schema='secure')
    
    # format and aggregate
    df_users['created_at_month'] = pd.to_datetime(df_users['created_at']).dt.to_period('M')
    
    created_monthly = df_users.groupby('created_at_month')['id'].count().reset_index().tail(12)
    created_monthly.columns = ['month', 'users_created']
    created_monthly['diff'] = created_monthly['users_created'].diff() / created_monthly['users_created']
    
    mean_user_monthly_growth = created_monthly['diff'].mean() * 100.
    mean_users_per_org = df_users[['id', 'org']].groupby('org')['id'].count().mean()
    
    perc_admin = float(len(df_users[df_users['user_type']=='Admin'])) / float(len(df_users))
    perc_user = float(len(df_users[df_users['user_type']=='User'])) / float(len(df_users))
    
    # build UI
    # bar chart for last 12 months users created
    monthly_users_graph = dcc.Graph(
        id='users-created-monthly',
        figure={
            'data': [{
                'x': [str(m) for m in created_monthly['month'].tolist()],
                'y': created_monthly['users_created'].tolist(),
                'type': 'bar',
                'name': 'Users created'
            }],
            'layout': {
                'title': 'Users Created'
            }
        }
    )
    
    # text display for users per org
    users_per_org_div = html.Div([
        html.Span("Users per Org"),
        html.H3("{:.2f}".format(mean_users_per_org))
    ])
    # text display for monthly user growth
    users_growth_per_month_div = html.Div([
        html.Span("Monthly user growth"),
        html.H3("{:.2f}%".format(mean_user_monthly_growth))
    ])
    # text display user type percentages
    user_type_admin_div = html.Div([
        html.Span("Admin type users"),
        html.H3("{:.2f}%".format(perc_admin * 100.))
    ])
    user_type_user_div = html.Div([
        html.Span("User type users"),
        html.H3("{:.2f}%".format(perc_user * 100.))
    ])
    
    return [
        html.Div([
            users_per_org_div,
            users_growth_per_month_div,
            user_type_admin_div,
            user_type_user_div
        ], className="columns two"),
        html.Div(monthly_users_graph, className="columns ten")
    ]


def get_logins_page():
    # retrieve data
    q = '''select 
                user_id,
                users.org, 
                date_trunc('day', original_timestamp) as date 
            from login 
                left join users on login.user_id=users._id
            order by date desc'''
    df_logins = redshift_query_read(q, schema='secure')
    
    df_logins['month'] = pd.to_datetime(df_logins['date']).dt.to_period('M')
    
    # aggregate logins by month for the last 12 months
    logins_monthly_last_year = df_logins.groupby('month')['user_id'].count().reset_index().head(12)
    logins_monthly_last_year.columns = ['month', 'logins']
    
    logins_daily_last_60_days = df_logins.groupby('date')['user_id'].count().reset_index().tail(60)
    logins_daily_last_60_days['trailing'] = logins_daily_last_60_days['user_id'].rolling(window=7).mean()
    
    org_monthly = df_logins.groupby(['month'])['org'].nunique().reset_index().tail(12)
    mean_login_per_user = df_logins.groupby('user_id')['user_id'].count().mean()
    
    # build UI
    # daily logins chart 
    daily_logins_graph = dcc.Graph(
        id='logins-daily',
        figure={
            'data': [{
                    'x': logins_daily_last_60_days['date'].tolist(),
                    'y': logins_daily_last_60_days['user_id'].tolist(),
                    'mode': 'line',
                    'name': 'daily logins'
                },{
                    'x': logins_daily_last_60_days['date'].tolist(),
                    'y': logins_daily_last_60_days['trailing'].tolist(),
                    'mode': 'line',
                    'name': '7 day rolling mean'
                }
            ],
            'layout': {
                'title': 'Daily logins',
                'height': 300
            }
        }
    )
    # monthly logins chart
    monthly_logins_graph = dcc.Graph(
        id='logins-monthly',
        figure={
            'data': [{
                'x': [str(m) for m in logins_monthly_last_year['month'].tolist()],
                'y': logins_monthly_last_year['logins'].tolist(),
                'type': 'bar',
                'name': 'Monthly logins'
            },{
                'x': [str(m) for m in org_monthly['month'].tolist()],
                'y': org_monthly['org'].tolist(),
                'type': 'bar',
                'name': 'Monthly orgs'
            }],
            'layout': {
                'title': 'Monthly logins',
                'height': 300
            }
        }
    )
    
    return [
        html.Div([
            html.Div([
                html.Span("Average logins per user"),
                html.H3("{:.2f}".format(mean_login_per_user))
            ])
        ], className="columns two"),
        html.Div([
            html.Div(daily_logins_graph),
            html.Div(monthly_logins_graph),
        ], className="columns ten")
    ]

def get_integrations_page():
    # load data
    q = "select count(id) as activations, date_trunc('month', original_timestamp) as month from activated_integration group by month order by month desc"
    df_integrations_monthly = redshift_query_read(q, schema='secure')
    
    q = "select count(id) as activations, integration from activated_integration group by integration"
    df_integrations_distribution = redshift_query_read(q, schema='secure')
    df_integrations_distribution['percentage'] = df_integrations_distribution['activations'] / df_integrations_distribution['activations'].sum()
    df_integrations_distribution['percentage'] = df_integrations_distribution['percentage'].apply(lambda x: "{:.2f}%".format(x * 100.))
    
    # build UI
    # monthly activations
    monthly_activations_graph = dcc.Graph(
        id='activations-monthly',
        figure={
            'data': [{
                'x': [str(m) for m in df_integrations_monthly['month'].tolist()],
                'y': df_integrations_monthly['activations'].tolist(),
                'type': 'bar'
            }],
            'layout': {
                'title': 'Monthly activations',
                'height': 300
            }
        }
    )
    
    # integration activations distribution
    distribution_table = dataframe_to_table(df_integrations_distribution)
    
    return [
        html.Div(distribution_table, className="columns three"),
        html.Div(monthly_activations_graph, className="columns nine")
    ]

def get_page_views_page():
    # load data
    q = "select count(id) as pageviews, date_trunc('day', original_timestamp) as date from pages group by date order by date desc"
    df_pageviews = redshift_query_read(q, schema='secure').head(60)
    df_pageviews['trailing'] = df_pageviews['pageviews'].rolling(window=7).mean()
    
    # build UI
    daily_pageviews_graph = dcc.Graph(
        id='pageviews-daily',
        figure={
            'data': [{
                    'x': df_pageviews['date'].tolist(),
                    'y': df_pageviews['pageviews'].tolist(),
                    'mode': 'line',
                    'name': 'daily pageviews'
                },{
                    'x': df_pageviews['date'].tolist(),
                    'y': df_pageviews['trailing'].tolist(),
                    'mode': 'line',
                    'name': '7 day rolling mean'
                }
            ],
            'layout': {
                'title': 'Daily pageviews',
                'height': 300
            }
        }
    )
    daily_mean = df_pageviews['pageviews'].mean()
    
    return [
        html.Div([
            html.Span("Average Daily Pageviews"),
            html.H3("{:.2f}".format(daily_mean))
        ], className="columns two"),
        html.Div(daily_pageviews_graph, className="columns ten")
    ]

def get_cms_page():
    # load data
    q = "select count(id) as page_updates, date_trunc('month', original_timestamp) as month from saved_page group by month order by month desc"
    df_cms_saves = redshift_query_read(q, schema='secure')
    
    q = '''select
                count(distinct(users.org)) as orgs,
                date_trunc('month', original_timestamp) as month
            from saved_page
                left join users on saved_page.uuid=users.uuid
            group by month
            order by month desc'''
    df_cms_orgs_saves = redshift_query_read(q, schema='secure') 
    
    # build UI
    # bar chart of cms saves
    monthly_cms_saves_graph = dcc.Graph(
        id='cms-updates-monthly',
        figure={
            'data': [{
                'x': [str(m) for m in df_cms_saves['month'].tolist()],
                'y': df_cms_saves['page_updates'].tolist(),
                'type': 'bar',
                'name': 'CMS page updates'
            },{
                'x': [str(m) for m in df_cms_orgs_saves['month'].tolist()],
                'y': df_cms_orgs_saves['orgs'].tolist(),
                'type': 'bar',
                'name': 'Orgs CMS page updates'
            }],
            'layout': {
                'title': 'Monthly activations',
                'height': 300
            }
        }
    )
    
    return [
        html.Div([html.H1(children="CMS Page Updates")]),
        html.Div([monthly_cms_saves_graph], className="columns ten")
    ]

def get_widgets_page():
    # load data
    q = "select count(id) as widgets_created, date_trunc('month', original_timestamp) as month from created_widget group by month order by month desc"
    widgets = redshift_query_read(q, schema='secure')

    q = "select count(id) as widgets_updated, date_trunc('month', original_timestamp) as month from updated_widget group by month order by month desc;"
    widgets_upd = redshift_query_read(q, schema="secure")

    df_widgets = widgets.merge(widgets_del, on='month').merge(widgets_upd, on="month")
    non_date_cols = [c for c in df_widgets.columns if c != 'month']
    df_widgets = df_widgets[['month'] + non_date_cols]
    
    q = '''select
                count(distinct(users.org)) as orgs,
                date_trunc('month', original_timestamp) as month
            from created_widget
                left join users on created_widget.uuid=users.uuid
            group by month
            order by month desc'''
    df_orgs_widgets = redshift_query_read(q, schema='secure')
    
    # build UI
    # bar chart of widget create
    monthly_widgets_graph = dcc.Graph(
        id='widgets-monthly',
        figure={
            'data': [{
                'x': [str(m) for m in df_widgets['month'].tolist()],
                'y': df_widgets['widgets_created'].tolist(),
                'type': 'bar',
                'name': 'Widgets created'
            },{
                'x': [str(m) for m in df_orgs_widgets['month'].tolist()],
                'y': df_orgs_widgets['orgs'].tolist(),
                'type': 'bar',
                'name': 'Orgs creating widgets'
            }],
            'layout': {
                'title': 'Monthly widgets',
                'height': 300
            }
        }
    )
    
    return [
        html.Div([html.H1(children="Widgets")]),
        html.Div([monthly_widgets_graph], className="columns ten"),
        html.Div([dataframe_to_table(df_widgets)], className="columns ten")
    ]

def get_integrations_interest_page():
    tables = [
        'interested_in_blackbaud_crm_ja_integration',
        'interested_in_bloomerang_integration',
        'interested_in_campaign_monitor_integration',
        'interested_in_church_community_builder_integration',
        'interested_in_clear_view_crm_integration',
        'interested_in_constant_contact_integration',
        'interested_in_donor_perfect_integration',
        'interested_in_emma_integration',
        'interested_in_fellowship_one_integration',
        'interested_in_kindful_integration',
        'interested_in_mailchimp_integration',
        'interested_in_match_maker_integration',
        'interested_in_neon_crm_integration',
        'interested_in_offline_for_qgiv_vt',
        'interested_in_quick_books_online_integration',
        'interested_in_raiser_s_edge_import_omatic_integration',
        'interested_in_raiser_s_edge_importacular_integration',
        'interested_in_salesforce_integration',
        'interested_in_zapier_integration'
    ]
    q = "select count(id) as {}, date_trunc('month', original_timestamp) as month from {} group by month order by month desc"
    
    df = None

    for t in tables:
        t_name = t.replace('interested_in_', '').replace('_integration', '')
        if df is None:
            df = redshift_query_read(q.format(t_name, t), schema="secure")
        else:
            new_df = redshift_query_read(q.format(t_name, t), schema="secure")
            df = df.merge(new_df, on="month", how="outer")
            
    df['month'] = pd.to_datetime(df['month'])
    df.sort_values('month', ascending=False, inplace=True)
    df = df.fillna(0)
    
    non_date_cols = [c for c in df.columns if c != 'month']
    df = df[['month'] + non_date_cols]
    
    return [
        html.Div([html.H1(children="Integrations interest")]),
        html.Div([dataframe_to_table(df)])
    ]

def get_report_filtering_page():
    q = "select count(id) as advanced_filtering, date_trunc('month', original_timestamp) as month from applied_advanced_reporting_filter group by month order by month desc"
    adv_filtering = redshift_query_read(q, schema="secure")

    q = "select count(id) as basic_filtering, date_trunc('month', original_timestamp) as month from applied_basic_reporting_filter group by month order by month desc"
    basic_filtering = redshift_query_read(q, schema="secure")
    
    q = "select count(id) as report_downloads, date_trunc('month', original_timestamp) as month from downloaded_report group by month order by month desc"
    report_downloads = redshift_query_read(q, schema="secure")
    
    df = adv_filtering.merge(basic_filtering, on="month").merge(report_downloads)
    df = df[['month', 'basic_filtering', 'advanced_filtering', 'report_downloads']]
    
    return [
        html.Div([html.H1(children="Reports")]),
        html.Div([dataframe_to_table(df)])
    ]

def get_goals_page():
    q = "select count(id) as goals_deleted, date_trunc('month', original_timestamp) as month from goals_deleted_item group by month order by month desc"
    goals_deleted = redshift_query_read(q, schema="secure")
    q = "select count(id) as goals_saved, date_trunc('month', original_timestamp) as month from goals_saved_item_settings group by month order by month desc"
    goals_saved = redshift_query_read(q, schema="secure")
    
    df = goals_saved.merge(goals_deleted, on="month", how="outer").fillna(0)
    df = df[['month', 'goals_saved', 'goals_deleted']]
    
    return [
        html.Div([html.H1(children="Goals")]),
        html.Div([dataframe_to_table(df)])
    ]

def get_builder_page():
    q = "select count(id) as fundhub_builder_accessed, date_trunc('month', original_timestamp) as month from accessed_fund_hub_builder group by month order by month desc"
    fundhub_accessed = redshift_query_read(q, schema="secure")
    q = "select count(id) as event_builder_accessed, date_trunc('month', original_timestamp) as month from accessed_event_builder group by month order by month desc"
    eventbuilder_accessed = redshift_query_read(q, schema="secure")
    q = "select count(id) as form_builder_accessed, date_trunc('month', original_timestamp) as month from accessed_form_builder group by month order by month desc"
    formbuilder_accessed = redshift_query_read(q, schema="secure")
    
    cols = ['month', 'fundhub_builder_accessed', 'event_builder_accessed', 'form_builder_accessed']
    mrgd = fundhub_accessed.merge(eventbuilder_accessed, on="month", how="outer").merge(formbuilder_accessed, on="month", how="outer")[cols].sort_values("month", ascending=True)
    
    return [
        html.Div([html.H1(children="Builder Pages")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_categories_page():
    q = "select count(id) as categories_deleted, date_trunc('month', original_timestamp) as month from categories_deleted_item group by month order by month desc"
    categories_deleted = redshift_query_read(q, schema="secure")
    q = "select count(id) as categories_saved, date_trunc('month', original_timestamp) as month from categories_saved_item_settings group by month order by month desc"
    categories_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as categories_started_edit, date_trunc('month', original_timestamp) as month from categories_started_item_edit group by month order by month desc"
    categories_started_edit = redshift_query_read(q, schema="secure")
    q = "select count(id) as categories_status_updated, date_trunc('month', original_timestamp) as month from categories_updated_item_status group by month order by month desc"
    categories_status_edit = redshift_query_read(q, schema="secure")
    
    cols = ['month', 'categories_started_edit', 'categories_saved', 'categories_status_updated', 'categories_deleted']
    mrgd = categories_deleted.merge(categories_saved, on='month', how="outer").merge(categories_started_edit, on='month', how="outer").merge(categories_status_edit, on='month', how="outer")[cols].sort_values('month', ascending=True)
    
    return [
        html.Div([html.H1(children="Categories")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_cloned_form_page():
    q = "select date_trunc('month', original_timestamp) as month, count(id) as forms_cloned from cloned_form group by month order by month desc"
    forms_cloned = redshift_query_read(q, schema="secure")
    
    return [
        html.Div([html.H1(children="Forms Cloned")]),
        html.Div([dataframe_to_table(forms_cloned)])
    ]

def get_badges_page():
    q = "select date_trunc('month', original_timestamp) as month, count(id) as custom_badges_created from created_custom_badge group by month order by month desc"
    badges_created = redshift_query_read(q, schema="secure")
    
    return [
        html.Div([html.H1(children="Badges")]),
        html.Div([dataframe_to_table(badges_created)])
    ]

def get_custom_fields_page():
    q = "select count(id) as custom_fields_deleted, date_trunc('month', original_timestamp) as month from custom_fields_deleted_item group by month order by month desc"
customfields_deleted = redshift_query_read(q, schema="secure")
    q = "select count(id) as custom_fields_saved, date_trunc('month', original_timestamp) as month from custom_fields_saved_item_settings group by month order by month desc"
    customfields_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as custom_fields_started_edit, date_trunc('month', original_timestamp) as month from custom_fields_started_item_edit group by month order by month desc"
    customfields_started_edit = redshift_query_read(q, schema="secure")
    q = "select count(id) as custom_fields_updated_status, date_trunc('month', original_timestamp) as month from custom_fields_updated_item_status group by month order by month desc"
    customfields_updated_status = redshift_query_read(q, schema="secure")
    
    cols = ["month", "custom_fields_deleted", "custom_fields_saved", "custom_fields_started_edit", "custom_fields_updated_status"]
    mrgd = customfields_deleted.merge(customfields_saved, on="month", how="outer").merge(customfields_started_edit, on="month", how="outer").merge(customfields_updated_status, on="month", how="outer")[cols].sort_values('month', ascending=True).fillna(0)
    
    return [
        html.Div([html.H1(children="Custom Fields")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_receipts_page():
    q = "select count(id) as custom_receipts_edited, date_trunc('month', original_timestamp) as month from edited_custom_receipt group by month order by month desc"
    custom_receipts_edited = redshift_query_read(q, schema="secure")
    q = "select count(id) as receipts_deleted, date_trunc('month', original_timestamp) as month from receipts_deleted_item group by month order by month desc"
    receipts_deleted = redshift_query_read(q, schema="secure")
    q = "select count(id) as receipts_saved, date_trunc('month', original_timestamp) as month from receipts_saved_item_settings group by month order by month desc"
    receipts_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as receipts_started_edit, date_trunc('month', original_timestamp) as month from receipts_started_item_edit group by month order by month desc"
    receipts_started_edit = redshift_query_read(q, schema="secure")
    q = "select count(id) as receipts_updated_status, date_trunc('month', original_timestamp) as month from receipts_updated_item_status group by month order by month desc"
    receipts_updated_status = redshift_query_read(q, schema="secure")
    
    cols = ["month", "custom_receipts_edited", "receipts_deleted", "receipts_saved", "receipts_started_edit", "receipts_updated_status"]
    mrgd = custom_receipts_edited.merge(receipts_deleted, on="month", how="outer").merge(receipts_saved, on="month", how="outer").merge(receipts_started_edit, on="month", how="outer").merge(receipts_updated_status, on="month", how="outer")[cols].sort_values('month', ascending=True).fillna(0)
    
    return [
        html.Div([html.H1(children="Receipts")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_pledges_page():
    q = "select count(id) as pledges_saved, date_trunc('month', original_timestamp) as month from pledges_saved_item_settings group by month order by month desc"
    pledges_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as pledges_started_edit, date_trunc('month', original_timestamp) as month from pledges_started_item_edit group by month order by month desc"
    pledges_started_edit = redshift_query_read(q, schema="secure")
    q = "select count(id) as pledges_updated_status, date_trunc('month', original_timestamp) as month from pledges_updated_item_status group by month order by month desc"
    pledges_updated_status = redshift_query_read(q, schema="secure")
    
    cols = ["month", "pledges_saved", "pledges_started_edit", "pledges_updated_status"]
    mrgd = pledges_saved.merge(pledges_started_edit, on="month", how="outer").merge(pledges_updated_status, on="month", how="outer")[cols].sort_values('month', ascending=True).fillna(0)
    
    return [
        html.Div([html.H1(children="Pledges")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_promo_page():
    q = "select count(id) as promo_deleted, date_trunc('month', original_timestamp) as month from promo_codes_deleted_item group by month order by month desc"
    promo_deleted = redshift_query_read(q, schema="secure")
    q = "select count(id) as promo_saved, date_trunc('month', original_timestamp) as month from promo_codes_saved_item_settings group by month order by month desc"
    promo_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as promo_started_edit, date_trunc('month', original_timestamp) as month from promo_codes_started_item_edit group by month order by month desc"
    promo_started_edit = redshift_query_read(q, schema="secure")
    q = "select count(id) as promo_status_updated, date_trunc('month', original_timestamp) as month from promo_codes_updated_item_status group by month order by month desc"
    promo_updated_status = redshift_query_read(q, schema="secure")
    
    cols = ["month", "promo_deleted", "promo_saved", "promo_started_edit", "promo_status_updated"]
    mrgd = promo_deleted.merge(promo_saved, on="month").merge(promo_started_edit, on="month").merge(promo_updated_status, on="month")[cols].sort_values('month', ascending=True).fillna(0)
    
    return [
        html.Div([html.H1(children="Promo Codes")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_sponsors_page():
    q = "select count(id) as sponsors_started_edit, date_trunc('month', original_timestamp) as month from sponsors_started_item_edit group by month order by month desc"
    sponsors_started_edit = redshift_query_read(q, schema="secure")
    q = "select count(id) as sponsors_updated_status, date_trunc('month', original_timestamp) as month from sponsors_updated_item_status group by month order by month desc"
    sponsors_updated_status = redshift_query_read(q, schema="secure")
    q = "select count(id) as sponsors_saved, date_trunc('month', original_timestamp) as month from sponsor_saved_item_settings group by month order by month desc"
    sponsors_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as sponsors_deleted, date_trunc('month', original_timestamp) as month from sponsor_deleted_item group by month order by month desc"
    sponsors_deleted = redshift_query_read(q, schema="secure")

    q = "select count(id) as sponsorscategory_deleted, date_trunc('month', original_timestamp) as month from sponsor_categories_deleted_item group by month order by month desc"
    sponsorscategory_deleted = redshift_query_read(q, schema="secure")
    q = "select count(id) as sponsorscategory_saved, date_trunc('month', original_timestamp) as month from sponsor_categories_saved_item_settings group by month order by month desc"
    sponsorscategory_saved = redshift_query_read(q, schema="secure")
    q = "select count(id) as sponsorscategory_started_edit, date_trunc('month', original_timestamp) as month from sponsor_categories_started_item_edit group by month order by month desc"
    sponsorscategory_started_edit = redshift_query_read(q, schema="secure")
    
    cols = ["month", "sponsors_started_edit", "sponsors_updated_status", "sponsors_saved",
            "sponsors_deleted", "sponsorscategory_deleted", "sponsorscategory_saved", 
            "sponsorscategory_started_edit"]
    mrgd = sponsors_started_edit.merge(sponsors_updated_status, on="month", how="outer").merge(sponsors_saved, on="month", how="outer").merge(sponsors_deleted, on="month", how="outer").merge(sponsorscategory_deleted, on="month", how="outer").merge(sponsorscategory_saved, on="month", how="outer").merge(sponsorscategory_started_edit, on="month", how="outer")[cols].sort_values('month', ascending=True).fillna(0)
    
    return [
        html.Div([html.H1(children="Sponsors")]),
        html.Div([dataframe_to_table(mrgd)])
    ]

def get_mappings_page():
    q = "select count(id) as mappings_created, date_trunc('month', original_timestamp) as month from created_data_mapping group by month order by month desc"
    mappings_created = redshift_query_read(q, schema="secure")
    q = "select count(id) as mappings_updated, date_trunc('month', original_timestamp) as month from updated_mappings group by month order by month desc"
    mappings_updated = redshift_query_read(q, schema="secure")
    
    cols = ["month", "mappings_created", "mappings_updated"]
    mrgd = mappings_created.merge(mappings_updated, on="month", how="outer")[cols].sort_values('month', ascending=True).fillna(0)
    
    return [
        html.Div([html.H1(children="Mappings")]),
        html.Div([dataframe_to_table(mrgd)])
    ]
    


app.layout = html.Div(children=[
    html.Div([
        html.Div([html.H1(children="Logins")]),
        html.Div(get_logins_page())
    ], style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div([
        html.Div([html.H1(children="Users")]),
        html.Div(get_user_page())
    ], style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div([
        html.Div([html.H1(children="Integrations Activations")]),
        html.Div(get_integrations_page())
    ], style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div([
        html.Div([html.H1(children="Control Panel Pageviews")]),
        html.Div(get_page_views_page())
    ], style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_cms_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_widgets_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_integrations_interest_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_report_filtering_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_goals_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_builder_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_categories_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_cloned_form_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_badges_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_custom_fields_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_receipts_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_pledges_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_promo_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_sponsors_page(), style={'clear': 'both', 'margin': '2em 1em'}),
    html.Div(get_mappings_page(), style={'clear': 'both', 'margin': '2em 1em'})
], style={'margin': '2em 1em'})


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8060)