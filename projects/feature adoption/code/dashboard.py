import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pickle as pkl
import numpy as np


# LOCAL DATA LOAD
DATA_PATH = "adoption_data.pkl"
data = pkl.load(open(DATA_PATH, "rb"))

# @TODO retrieve actual org & form counts
len_orgs = data['meta']['len_orgs']
len_forms = data['meta']['len_forms']
del(data['meta'])
# REMOTE DATA LOAD

adoption_types = list(data.keys())
all_keys = []
for adoption_type in adoption_types:
    all_keys += data[adoption_type].keys()
all_keys = sorted(list(set(all_keys)), reverse=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

dropdown_options = [{'label': 'All', 'value': 'all'}]
for k in all_keys:
    dropdown_options.append({'label': k, 'value': k})


app.layout = html.Div([
    html.Div([
        html.H1(children="Feature Adoption", className="columns six"),

        dcc.Dropdown(
            id='adoption_filter',
            options=dropdown_options,
            value='all',
            className="columns six"
        ),
    ], style={"clear": "both"}),
    html.Div(id="content_container", children=[], style={"clear": "both"})
])


def get_detail_data(selected_feature):
    data_point = {}
    for adoption_type in adoption_types:
        if selected_feature in data[adoption_type]:
            data_point[adoption_type] = data[adoption_type][selected_feature]

            if 'meta' in data[adoption_type][selected_feature]: 
                _meta = data[adoption_type][selected_feature]['meta']

                if 'per_form' in _meta:
                    _meta['per_form ({})'.format(adoption_type.replace('_data', ''))] = "{:.2f}".format(_meta['per_form'])
                    del(_meta['per_form'])
                
                if 'per_org' in _meta:
                    _meta['per_org ({})'.format(adoption_type.replace('_data', ''))] = "{:.2f}".format(_meta['per_org'])
                    del(_meta['per_org'])

                if 'meta' in data_point:
                    data_point['meta'] = {**data_point['meta'], **_meta}
                else:
                    data_point['meta'] = _meta
                    
        else:
            data_point[adoption_type] = {}

    header_children = []
    detail_children = []
    for t in adoption_types:
        adoption_rate = 'N/A'
        if 'adoption_rate' in data_point[t] and data_point[t]['adoption_rate'] is not None:
            adoption_rate = "{:.2f}%".format(data_point[t]['adoption_rate'] * 100.)

        header_children.append(html.Div([
            html.Span(t.replace('_data', '').upper().replace('_', ' ')),
            html.H3(adoption_rate)
        ], className="columns four", style={"padding": "1em"}))
        
    if 'meta' in data_point:
        meta = data_point['meta'].copy()
        for k in meta:
            if '_gt_' not in k:
                if 'count' in k and 'average' not in k:
                    meta[k] = int(meta[k])
                elif 'average_count' in k or k == 'per_form' or k == 'per_org':
                    meta[k] = "{:.2f}".format(meta[k])
                elif 'adoption_rate' in k:
                    meta[k] = "{:.2f}%".format(meta[k] * 100.)
                elif 'percentage' in k:
                    meta[k] = "{:.2f}%".format(meta[k])
                elif 'value' in k:
                    meta[k] = "${:.2f}".format(meta[k])
        detail_children.append(html.Div(
            [html.Div([
                html.Span(e.replace('_', ' ').replace("percentage", "%")),
                html.H5(meta[e])
            ], className="columns two", style={"padding": "1em"}) for e in meta if '_gt_' not in e and e not in adoption_types + ['count_orgs', 'count_forms']]
        ))

        gt_keys = [k for k in meta if '_gt_' in k]
        if len(gt_keys) > 0:
            detail_children.append(html.Div([
                dash_table.DataTable(
                    id='intervals',
                    style_cell={'textAlign': 'center'},
                    columns=[{"name": "threshold", "id": "threshold"}, {"name": "orgs", "id": "orgs"}, {"name": "forms", "id": "forms"}],
                    data=[
                        {
                            "threshold": "> 0 trans", 
                            "orgs": "{} ({:.2f}%)".format(meta['orgs_gt_0.0'], (meta['orgs_gt_0.0'] / len_orgs) * 100.), 
                            "forms": "{} ({:.2f}%)".format(meta['forms_gt_0.0'], (meta['forms_gt_0.0'] / len_forms) * 100.)
                        }, {
                            "threshold": "> 10% trans", 
                            "orgs": "{} ({:.2f}%)".format(meta['orgs_gt_10.0'], (meta['orgs_gt_10.0'] / len_orgs) * 100.), 
                            "forms": "{} ({:.2f}%)".format(meta['forms_gt_10.0'], (meta['forms_gt_10.0'] / len_forms) * 100.)
                        }, {
                            "threshold": "> 25% trans", 
                            "orgs": "{} ({:.2f}%)".format(meta['orgs_gt_25.0'], (meta['orgs_gt_25.0'] / len_orgs) * 100.), 
                            "forms": "{} ({:.2f}%)".format(meta['forms_gt_25.0'], (meta['forms_gt_25.0'] / len_forms) * 100.)
                        }, {
                            "threshold": "> 50% trans", 
                            "orgs": "{} ({:.2f}%)".format(meta['orgs_gt_50.0'], (meta['orgs_gt_50.0'] / len_orgs) * 100.), 
                            "forms": "{} ({:.2f}%)".format(meta['forms_gt_50.0'], (meta['forms_gt_50.0'] / len_forms) * 100.)
                        }, {
                            "threshold": "> 75% trans", 
                            "orgs": "{} ({:.2f}%)".format(meta['orgs_gt_75.0'], (meta['orgs_gt_75.0'] / len_orgs) * 100.), 
                            "forms": "{} ({:.2f}%)".format(meta['forms_gt_75.0'], (meta['forms_gt_75.0'] / len_forms) * 100.)
                        }, {
                            "threshold": "> 90% trans", 
                            "orgs": "{} ({:.2f}%)".format(meta['orgs_gt_90.0'], (meta['orgs_gt_90.0'] / len_orgs) * 100.), 
                            "forms": "{} ({:.2f}%)".format(meta['forms_gt_90.0'], (meta['forms_gt_90.0'] / len_forms) * 100.)
                        }
                    ]
                )
            ]))
    
    return [
        html.Div(header_children, style={"clear": "both"}),
        html.Div(detail_children)
    ]


def get_all_graph():
    return dcc.Graph(
        id="feature-adoption",
        figure={
            'data': [
                {
                    'x': ["{:.2f}".format(data['implementation_data'][e]['adoption_rate'] * 100.) if e in data['implementation_data'] and'adoption_rate' in data['implementation_data'][e] else 0 for e in all_keys], 
                    'y': all_keys, 
                    'type': 'bar', 
                    'name': 'implemented', 
                    'orientation': 'h'
                },
                {
                    'x': ["{:.2f}".format(data['bidirectional_adoption_data'][e]['adoption_rate'] * 100.) if e in data['bidirectional_adoption_data'] and 'adoption_rate' in data['bidirectional_adoption_data'][e] else 0 for e in all_keys], 
                    'y': all_keys, 
                    'type': 'bar', 
                    'name': 'bidirectional', 
                    'orientation': 'h'
                },
                {
                    'x': ["{:.2f}".format(data['institutional_adoption_data'][e]['adoption_rate'] * 100.) if e in data['institutional_adoption_data'] and 'adoption_rate' in data['institutional_adoption_data'][e] else 0 for e in all_keys], 
                    'y': all_keys, 
                    'type': 'bar', 
                    'name': 'institutional', 
                    'orientation': 'h'
                }
            ],
            'layout': {
                "xaxis": {
                    "range": (0, 100)
                },
                "margin": dict(l=200, r=10, t=25, b=25)
            }
        },
        style={"height": "150vh"},
        config={'displayModeBar': False}
    )


@app.callback(
    Output(component_id="content_container", component_property="children"),
    [Input(component_id="adoption_filter", component_property="value")]
)
def handle_adoption_filter_change(filter_input):
    if filter_input == 'all':
        return html.Div(children=[
            get_all_graph(),
            html.Div(children=[
                html.Div("All stats are percentages of organizations"),
                html.Div("Implemented means the organization has implemented or enabled the given feature"),
                html.Div("Bidirectional means the organization has processed transactions that can be associated with the given feature"),
                html.Div("Institutional means the given feature can be associated with more then 15% of the organizations transactions")
            ], style={"margin": "2em"})
        ])
    else:
        return get_detail_data(filter_input)


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port="8050")