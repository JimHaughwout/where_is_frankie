from subprocess import check_output
import requests
import json

def scan_wifis():
    CMD = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    OPT = "-s"
    results = check_output([CMD, OPT]).split('\n')
    return results

def parse_wifi_scan_results(results):
    # Find delimiters
    bssid_start = results[0].find('BSSID')
    rssi_start = results[0].find('RSSI')
    channel_start = results[0].find('CHANNEL')
    ht_start = results[0].find('HT')
    
    # Build results
    parsed_results = []
    for station in results[1:-1]:
        #print station
        bssi = station[bssid_start:rssi_start].strip()
        rssi = int(station[rssi_start:channel_start].strip())
        channel = station[channel_start:ht_start].strip().split(',')[0]
        parsed_results.append({'macAddress': bssi, 'signalStrength': rssi, 'channel': channel})
        
    return sorted(parsed_results, key=lambda x: x['signalStrength'], reverse=True)


def get_location(parsed_results):
    API_KEY = 'AIzaSyDcv-DsSncE_0J70_bf8DAXBfT887fsWXs'
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=%s' % API_KEY
    payload = {'wifiAccessPoints' : parsed_results}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        print "Received Response Code %d" % r.status_code


print "Scanning Wifis..."
raw_scan = scan_wifis()
results = parse_wifi_scan_results(raw_scan)
print json.dumps(results, indent=2)
print "Getting location based on Wifis..."
print get_location(results)