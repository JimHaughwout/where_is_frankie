# Prep for Lambda stuff
from mac_os_airport import mac_os_location_scan
import json
import requests
from time import sleep

def get_location(scan_payload):
    API_KEY = 'AIzaSyDcv-DsSncE_0J70_bf8DAXBfT887fsWXs'
    RESULT_AVAILABLE = 'GeolocationUpdate'
    NO_RESULT_AVAILABLE = 'NoLocationAvailable'

    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=%s' % API_KEY
    payload = {'wifiAccessPoints' : scan_payload['wifiAccessPoints']}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
    	results = json.loads(r.text)
    	scan_payload['event'] = RESULT_AVAILABLE
    	scan_payload['location'] = results['location']
    	scan_payload['accuracy'] = results['accuracy']
    else:
        scan_payload['event'] = NO_RESULT_AVAILABLE
        scan_payload['location'] = None
        scan_payload['accuracy'] = None
    return scan_payload


def log_results(log_file, location_results):
	with open(log_file, "a") as logger:
		logger.write(json.dumps(location_results) + '\n')
	return

LOG_FILE = 'HAUGHWOUT_MAC_BELLFOREST'
INTERVAL = 900 # Seconds
READ_CNT = 40

for i in range(1, READ_CNT + 1):
	print "Scan: %s..." % str(i).zfill(4),
	scan = mac_os_location_scan()
	print "Getting location for scan results...",
	location = get_location(scan)
	log_results(LOG_FILE, location)
	print "Logged results. Waiting %d seconds" % INTERVAL
	sleep(INTERVAL)