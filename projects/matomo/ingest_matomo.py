from s3_support import *

# retrieve bucket list of files to ingest
files = list_files("matomo-records")

# ingest files
for f in files:     
    # load to redshift
    q = '''copy matomo_traffic
        from 's3://matomo-records/{}'
        iam_role 'arn:aws:iam::637885584661:role/AWSRoleForRedshift'
        emptyasnull
        blanksasnull
        fillrecord
        delimiter ','
        ignoreheader 1
        region 'us-east-1';'''.format(f)

    try:
        redshift_query_write(q, schema='production')
        
        # if successful, delete files from bucket
        delete_s3_file("matomo-records", f)
    except Exception as e:
        print("error ingesting matomo-records/{}".format(f))
        print(e)

print("DONE")