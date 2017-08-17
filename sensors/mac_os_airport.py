from subprocess import check_output
from time import time

def _scan_wifis():
    CMD = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    OPT = "-s"
    results = check_output([CMD, OPT]).split('\n')
    return results

def _parse_scan_results(results):
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


def _get_mac_addr():
    CMD = "/sbin/ifconfig"
    raw = check_output([CMD])
    results = raw.replace('\t', '').split('\n')
    ether = None
    status = None
    for item in results:
        if not ether:
            if item[:2] == 'en':
                ether = item[:3]
        if ether and item[:6] == 'status':
            if item.split(' ')[-1] == 'active':
                status = 'active'
            else:
                ether = None
        if ether and status and item[:5] == 'ether':
            return item.strip().split(' ')[-1].strip()
    return "NotAvailable"


def mac_os_location_scan():
    unix_time = int(time())
    mac_os_addr = _get_mac_addr()
    raw_scan_results = _scan_wifis()
    stations = _parse_scan_results(raw_scan_results)

    payload = {}
    payload['sensorId'] = mac_os_addr
    payload['asOfTimestamp'] = unix_time
    payload['wifiAccessPoints'] = stations
    return payload



