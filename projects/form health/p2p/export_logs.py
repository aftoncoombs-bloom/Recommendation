import os, pickle
from urllib import urlencode
from httplib2 import Http


os.chdir("/Users/jeremyvanvalkenburg/Repositories/datasets/logs/")

key = "DSQR59VwyFhw21PKDF4K"
limit = "100000"
offset = "1"
url = "https://secure.qgiv.com/admin/qgivadmin/statistics/log_export.php?output=csv"

keep_going = True
while keep_going:
    print("requesting...")
    h = Http()
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    rsp, content = h.request(url, "POST", urlencode({'key': key, 'limit': limit, 'offset': offset, 'output': 'csv'}), headers=headers)

    if len(content) < 1000:
        keep_going = False
    
    offset = int(offset)
    limit = int(limit)

    if offset == 1:
        offset = 0

    file_name = "logs_"+str(int(float(offset) / float(limit)) + 1)+".pkl"
    print("\tdumping {}".format(file_name))
    with open(file_name, "w") as f:
        pickle.dump(content, f)

    offset += limit