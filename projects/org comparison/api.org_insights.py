from flask import Flask, jsonify, request, g
import datetime, os
from s3_support import *


app = Flask(__name__)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


@app.route('/test/', methods=['GET'])
def test():
    rsp = {'success': '0'}

    try:
        # query db
        q = "select id from transactions order by id desc limit 10"
        df = redshift_query_read(q, schema='production')

        if len(df) == 10:
            rsp = {
                'success': '1',
                'message': "{} entries retreived".format(len(df))
            }
    except:
        rsp['message'] = 'DB connect failed'

    # respond
    return jsonify(rsp)


@app.route('/orginsights/', methods=['POST'])
def org_insights(testing=False):
    key = 'tIHLM2vNlBwvlZlqdKy8'
    # localize params
    _input = request.form.to_dict()
    
    if 'key' not in _input or _input['key'] != key:
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        try:
            # isolate requested insights
            insights = _input['insights'].split(",")
            del(_input['insights'])

            # translate filters to sql
            filters, joins_clauses = get_sql_for_filters(_input)

            # get requested stats
            stats = []
            default_filters = ["t.status='A'", "(t.recurring=0 or t.recurring_origin=1)"]
            for insight in insights:
                if insight == 'contribution_total':
                    select = 'select sum(t.amount) / count(distinct t.org) as stat from transactions as t'
                    stats.append({
                        'insight': insight,
                        'stat': str(get_stat(select, filters + default_filters, joins=joins_clauses))
                    })
                elif insight == 'contribution_count':
                    select = 'select count(t.id) / count(distinct t.org) as stat from transactions as t'
                    stats.append({
                        'insight': insight,
                        'stat': str(get_stat(select, filters + default_filters, joins=joins_clauses, group=group_clause))
                    })
                elif insight == 'average_contribution_amount':
                    select = 'select avg(t.amount) as stat from transactions as t'
                    stats.append({
                        'insight': insight,
                        'stat': str(get_stat(select, filters + default_filters, joins=joins_clauses))
                    })
                elif insight == 'median_contribution_amount':
                    select = 'select median(t.amount) as stat from transactions as t'
                    stats.append({
                        'insight': insight,
                        'stat': str(get_stat(select, filters + default_filters, joins=joins_clauses))
                    })

            rsp = {
                'success': 1,
                'stats': stats
            }
        except Exception as e:
            rsp = {
                'success': 0,
                'error': "Error attempting to calculate insight; {}".format(e)
            }
        
    return jsonify(rsp)


def get_stat(select, where_statements, joins=None, group=None):
    q = select
    
    if joins:
        q += ' left join ' + ' left join '.join(joins)
        
    q += ' where ' + " and ".join(where_statements)
    
    if group:
        q += ' group by ' + ", ".join(group)
    
    df = redshift_query_read(q, schema='production')
    return df['stat'].iloc[0]


def get_sql_for_filters(filters):
    filters_sql = []
    joins_clauses = []
    
    for f in filters:
        if f.lower() == 'ntee':
            param = filters[f]
            filters_sql.append("o.ntee='{}'".format(param))
            joins_clauses.append("organization as o on t.org=o.id")
        elif f.lower() == 'segment':
            param = filters[f]
            filters_sql.append("o.segment ilike '%{}%'".format(param))
            joins_clauses.append("organization as o on t.org=o.id")
        elif f.lower() == 'tag':
            param = filters[f]
            filters_sql.append("o.tag ilike '%{}%'".format(param))
            joins_clauses.append("organization as o on t.org=o.id")
        elif f.lower() == 'timeframe':
            if filters[f] == '1week':
                min_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
            elif filters[f] == '1month':
                min_date = datetime.datetime.now() - datetime.timedelta(weeks=4)
            elif filters[f] == '3months':
                min_date = datetime.datetime.now() - datetime.timedelta(weeks=12)
            elif filters[f] == '6months':
                min_date = datetime.datetime.now() - datetime.timedelta(weeks=24)
            elif filters[f] == '1year':
                min_date = datetime.datetime.now() - datetime.timedelta(weeks=52)
            
            filters_sql.append("t.date>='{}'".format(min_date))
            
    return filters_sql, set(joins_clauses)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8900")