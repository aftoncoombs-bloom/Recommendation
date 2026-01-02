from analytics_update import run_updates
import pickle, datetime, os, sys

print("Prepping...")
log_path = "analytics_update.log"
log_obj = []

print("checking file for log")
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        log_obj = pickle.load(f)
        print("\topening preexisting log")
else:
    print("\tno preexisting log, creating new")
    log_obj = []

print("starting updates...")
this_log = {'update_start': datetime.datetime.now()}

try:
    print("\trunning updates")

    run_log = run_updates()
    this_log['success'] = True

    print("\tcompleted updates")
except:
    this_log['success'] = False
    print("\tanalytics udpate failed")
    
    this_log['error'] = str(sys.exc_info()[0]) + ' : ' + str(sys.exc_info()[1])
    print("\t{}".format(sys.exc_info()[0]))
    print("\t{}".format(sys.exc_info()[1]))

this_log['update_end'] = datetime.datetime.now()

print("saving to log")

log_obj.append(this_log)
with open(log_path, "w") as f:
    pickle.dump(log_obj, f)