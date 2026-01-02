import argparse

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from datetime import datetime, timedelta

import time


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
KEY_FILE_LOCATION = 'MyProject-2aca093c2c0c.p12'
SERVICE_ACCOUNT_EMAIL = 'qgiv-analytics@mindful-accord-151619.iam.gserviceaccount.com'

# VIEW_ID = '109204515'  # original
VIEW_ID = '135749429'  # new as of 1/16/17


def initialize_analyticsreporting():
	"""Initializes an analyticsreporting service object.

	Returns:
	analytics an authorized analyticsreporting service object.
	"""

	credentials = ServiceAccountCredentials.from_p12_keyfile(SERVICE_ACCOUNT_EMAIL, KEY_FILE_LOCATION, scopes=SCOPES)

	http = credentials.authorize(httplib2.Http())

	# Build the service object.
	analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=DISCOVERY_URI)

	return analytics


def get_report(analytics, daysAgo, add_account_ids=False):
	# Use the Analytics Service Object to query the Analytics Reporting API V4.
	startDate = str(daysAgo)+'daysAgo'
	endDate = str(daysAgo - 1)+'daysAgo'

	if add_account_ids:
		dimensions = [
			{'name': 'ga:pagePath'},
			{'name': 'ga:browser'},
			{'name': 'ga:dimension1'},  # global account ID - present in p2p2 page views
			{'name': 'ga:dimension2'}   # trans registration ID - present in p2p2 page views
		]
	else:
		dimensions = [
			{'name': 'ga:pagePath'},
			{'name': 'ga:browser'}
		]

	return analytics.reports().batchGet(
		body={
			'reportRequests': [
			{
				'viewId': VIEW_ID,
				'dateRanges': [{'startDate': startDate, 'endDate': endDate}],
				'metrics': [{'expression': 'ga:pageviews'}],
				'dimensions': dimensions,
				'dimensionFilterClauses': [{
				"filters": [{
					"dimension_name": "ga:pagePath",
					"not": "true",
					"operator": "PARTIAL",
					"expressions": [
						"control"
					],
					"caseSensitive": "false"
				}]
			}],
			'pageSize': 50000
			}]
		}
		).execute()


def build_response(response):
	"""Parses and prints the Analytics Reporting API V4 response"""

	report_arr = []

	for report in response.get('reports', []):
		columnHeader = report.get('columnHeader', {})
		dimensionHeaders = columnHeader.get('dimensions', [])
		metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
		rows = report.get('data', {}).get('rows', [])

	for row in rows:
		dimensions = row.get('dimensions', [])
		dateRangeValues = row.get('metrics', [])
		obj = {}
		for header, dimension in zip(dimensionHeaders, dimensions):
			obj[header] = dimension

		for i, values in enumerate(dateRangeValues):
			for metricHeader, value in zip(metricHeaders, values.get('values')):
				obj[metricHeader.get('name')] = value
		
		report_arr.append(obj)
		
	return report_arr


def load_analytics(days_to_pull=1, add_account_ids=False):
	analytics = initialize_analyticsreporting()

	data = []
	for daysAgo in range(1, days_to_pull+1):
		response = get_report(analytics, daysAgo, add_account_ids=add_account_ids)
		obj = build_response(response)
		adt = datetime.now() - timedelta(days=daysAgo)

		for r in obj:
			if add_account_ids:
				data.append({'date': adt.strftime("%Y-%m-%d"), 'views': r['ga:pageviews'].encode('utf-8'), 'path': r['ga:pagePath'].encode('utf-8'), 'browser': r['ga:browser'].encode('utf-8'), 'globalAccountID': r['ga:dimension1'].encode('utf-8'), 'transregistrationID': r['ga:dimension2'].encode('utf-8')})
			else:
				data.append({'date': adt.strftime("%Y-%m-%d"), 'views': r['ga:pageviews'].encode('utf-8'), 'path': r['ga:pagePath'].encode('utf-8'), 'browser': r['ga:browser'].encode('utf-8')})

		# API limits requests per second so we need to slow things down a bit
		time.sleep(1)
	
	return data