import csv
import pandas as pd
import os.path


def compile_analytics(prefix):
	ga_data_obj = []
	daysAgo = 1
	path = '/Users/vsquared/Repositories/git.recommendation/tests/'
    
	while os.path.isfile(path+prefix+str(daysAgo)+'.csv'):
		print("opening "+str(daysAgo)+" file")
		with open(path+prefix+str(daysAgo)+'.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				ga_data_obj.append(row)
		print(str(len(ga_data_obj))+" rows read")
		daysAgo = daysAgo + 1
	
	ga_df = pd.DataFrame(data=ga_data_obj, columns=['date', 'views', 'path', 'browser', 'globalAccountID', 'transregistrationID'])
	ga_df.to_csv(path+prefix+'.csv', sep=',')
	

def isolate_keys(path):
	new_csv_data = []

	with open(path) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if '/for/' in row['path']:
				# looking for /for/[key]/...
				split_path = row['path'].split('/')
				if split_path[1] == 'for':
					row['key'] = split_path[2]
			elif '/event/' in row['path']:
				# looking for /event/[ID or alias]/...
				split_path = row['path'].split('/')
				if split_path[1] == 'event':
					if split_path[2] == 'account' or split_path[2] == 'team':
						# need to query for event ID for this account or team
						row['key'] = ''
					else:
						row['key'] = split_path[2]
			
			if 'key' not in row:
				row['key'] = ''
			new_csv_data.append(row)

	df = pd.DataFrame(data=new_csv_data, columns=['date', 'views', 'path', 'browser', 'key'])
	df.to_csv(path, sep=',')