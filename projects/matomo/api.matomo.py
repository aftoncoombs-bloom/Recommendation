from flask import Flask, jsonify, request
import os
from s3_support import *

# init flask app
app = Flask(__name__)
# change working directory to files directory for load_model()
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


@app.route('/test/', methods=['GET'])
def test():
    rsp = {'success': '0'}

    try:
        # query db
        q = "select id from matomo_traffic order by id desc limit 10"
        df = redshift_query_read(q, schema='production')

        if len(df) == 10:
            rsp = {
                'success': '1',
                'entries': len(df)
            }
    except:
        rsp['message'] = 'DB connect failed'

    # respond
    return jsonify(rsp)


@app.route('/matomo_traffic/', methods=['POST'])
def get_matomo_traffic():
    key = 'tIHLM2vNlBwvlZlqdKy8'
    _input = request.get_json()

    # params: org, form, date, agg by device
    validate_key = 'key' in _input and _input['key'] == key
    validate_org = 'org' in _input
    if not validate_key or not validate_org:
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        try:
            q = '''select
                        devicetype,
                        date_trunc('day', timestamp) as date,
                        count(id) as pageviews,
                        avg(visitduration) as avg_visitduration,
                        avg(actions) as avg_actions,
                        avg(timespent) as avg_timespent
                    from matomo_traffic'''

            grp = '''group by devicetype, date_trunc('day', timestamp)
                    order by date_trunc('day', timestamp) desc'''

            where = ["org={}".format(_input['org'])]

            # handle form inputs, comma separated list
            if 'forms' in _input:
                where.append("form in ({})".format(_input['forms']))

            # handle date range inputs
            if 'start_date' in _input and 'end_date' in _input:
                where.append("timestamp between '{}' and '{}'".format(_input['start_date'], _input['end_date']))
            elif 'start_date' in _input:
                where.append("timestamp > '{}'".format(_input['start_date']))
            elif 'end_date' in _input:
                where.append("timestamp < '{}'".format(_input['end_date']))

            # build full query by joining base, joins, where and group clauses
            q = q + " and ".join(where) + grp

            data = redshift_query_read(q, schema='production')

            rsp = {
                'success': '1',
                'data': data
            }
        except Exception as e:
            rsp = {
                'success': '0',
                'errors': str(e)
            }

    return jsonify(rsp)


@app.route('/matomo_traffic_system/', methods=['POST'])
def get_matomo_traffic_system():
    key = "Hr3Gogvjnu2RZKJVwWTh"
    _input = request.get_json()

    if 'key' not in _input or _input['key'] != key:
        rsp = {
            'success': '0',
            'errrors': 'Invalid input'
        }
    else:
        try:
            # params: org segment, pricing package, form type, date, agg by device
            q = '''select
                        m.devicetype,
                        date_trunc('day', m.timestamp) as date,
                        count(m.id) as pageviews,
                        avg(m.visitduration) as avg_visitduration,
                        avg(m.actions) as avg_actions,
                        avg(m.timespent) as avg_timespent
                    from matomo_traffic as m'''

            grp = '''group by m.devicetype, date_trunc('day', m.timestamp)
                    order by date_trunc('day', m.timestamp) desc'''

            where = []
            joins = []

            # handle date range inputs
            if 'start_date' in _input and 'end_date' in _input:
                where.append("m.timestamp between '{}' and '{}'".format(_input['start_date'], _input['end_date']))
            elif 'start_date' in _input:
                where.append("m.timestamp > '{}'".format(_input['start_date']))
            elif 'end_date' in _input:
                where.append("m.timestamp < '{}'".format(_input['end_date']))

            # handle form type input
            if 'form_type' in _input:
                where.append("f.type={}".format(_input['form_type']))
                joins.append("left join form as f on m.form=f.id")

            # handle org segment
            if 'segment' in _input:
                where.append("o.segment like '%{}%'".format(_input['segment']))
                joins.append("left join organization as o on o.id=m.org")

            # handle pricing package
            if 'pricing_package' in _input:
                where.append("o.pricing_package like '%{}%'".format(_input['pricing_package']))
                joins.append("left join organization as o on o.id=m.org")

            # build full query by joining base, joins, where and group clauses
            q = q + " ".join(set(joins)) + " and ".join(where) + grp

            data = redshift_query_read(q, schema='production')

            rsp = {
                'success': '1',
                'data': data
            }
        except Exception as e:
            rsp = {
                'success': '0',
                'errors': 'Processing error: {}'.format(e)
            }

    return jsonify(rsp)


@app.route('matomo_referrer/', methods=['POST'])
def get_matomo_referrer():
    key = 'tIHLM2vNlBwvlZlqdKy8'
    _input = request.get_json()

    # params: org, form, date, agg by device
    validate_key = 'key' in _input and _input['key'] == key
    validate_org = 'org' in _input
    if not validate_key or not validate_org:
        rsp = {
            'success': '0',
            'errors': 'Incorrect input'
        }
    else:
        try:
            q = '''select
                        referrertype,
                        referrername,
                        count(id) as pageviews
                    from matomo_traffic'''

            grp = '''group by referrertype, referrername
                    order by count(id) desc
                    limit 20'''

            where = ["org={}".format(_input['org'])]

            # handle form inputs, comma separated list
            if 'forms' in _input:
                where.append("form in ({})".format(_input['forms']))

            # handle date range inputs
            if 'start_date' in _input and 'end_date' in _input:
                where.append("timestamp between '{}' and '{}'".format(_input['start_date'], _input['end_date']))
            elif 'start_date' in _input:
                where.append("timestamp > '{}'".format(_input['start_date']))
            elif 'end_date' in _input:
                where.append("timestamp < '{}'".format(_input['end_date']))

            # build full query by joining base, joins, where and group clauses
            q = q + " and ".join(where) + grp

            data = redshift_query_read(q, schema='production')

            rsp = {
                'success': '1',
                'data': data
            }
        except Exception as e:
            rsp = {
                'success': '0',
                'errors': str(e)
            }

    return jsonify(rsp)


@app.route('matomo_referrer_system/', methods=['POST'])
def get_matomo_referrer_system():
    key = "Hr3Gogvjnu2RZKJVwWTh"
    _input = request.get_json()

    if 'key' not in _input or _input['key'] != key:
        rsp = {
            'success': '0',
            'errrors': 'Invalid input'
        }
    else:
        try:
            q = '''select
                        m.referrertype,
                        m.referrername,
                        count(m.id) as pageviews
                    from matomo_traffic as m'''

            grp = '''group by m.referrertype, m.referrername
                    order by count(m.id) desc
                    limit 20'''

            where = []
            joins = []

            # handle date range inputs
            if 'start_date' in _input and 'end_date' in _input:
                where.append("m.timestamp between '{}' and '{}'".format(_input['start_date'], _input['end_date']))
            elif 'start_date' in _input:
                where.append("m.timestamp > '{}'".format(_input['start_date']))
            elif 'end_date' in _input:
                where.append("m.timestamp < '{}'".format(_input['end_date']))

            # handle form type input
            if 'form_type' in _input:
                where.append("f.type={}".format(_input['form_type']))
                joins.append("left join form as f on m.form=f.id")

            # handle org segment
            if 'segment' in _input:
                where.append("o.segment like '%{}%'".format(_input['segment']))
                joins.append("left join organization as o on o.id=m.org")

            # handle pricing package
            if 'pricing_package' in _input:
                where.append("o.pricing_package like '%{}%'".format(_input['pricing_package']))
                joins.append("left join organization as o on o.id=m.org")

            # build full query by joining base, joins, where and group clauses
            q = q + " ".join(set(joins)) + " and ".join(where) + grp

            data = redshift_query_read(q, schema='production')

            rsp = {
                'success': '1',
                'data': data
            }
        except Exception as e:
            rsp = {
                'success': '0',
                'errors': 'Processing error: {}'.format(e)
            }

    return jsonify(rsp)


if __name__ == "__main__":
    app.run(host='0.0.0.0')