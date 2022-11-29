#!/usr/bin/env python3

import requests
import json
import yaml
from yaml.loader import SafeLoader
import argparse

def get_arguments(): # Gets The IP Address to Analyze
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest='ip_address', help='Sets IP Address to fetch information.')
    (options) = parser.parse_args()
    if not options.ip_address:
        parser.error('[-] Please Specify an IP Address to fetch information.')
    return options

def check_key(): # Loads yaml file including enabled state and api keys
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=SafeLoader)
    if config['virustotal'] == 'your_api_key_goes_here':
        print('\n[-] VirusTotal is missing an API Key\n')
        exit()
    else:
        return config['virustotal']

def fetch_data(ip_address, api_key): # Requests data
    url = f'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}'

    headers = {
        'Accept': 'application/json',
        'x-apikey': api_key
    }

    response = requests.request(method='GET', url=url, headers=headers)
    decodedResponse = json.loads(response.text)
    return decodedResponse

def filter_data(data): # Filters data
    # Add: network, last_analysis_stats (malicious, suspicious),
    if 'error' in data:
        details = f"Details: {data['error']['message']}"
        output = f"\n[-] VirusTotal\n{details}\n"
    elif 'private' in data['data']['attributes']['tags']:
        ip_address = data['data']['id']
        output = f"\n[-] VirusTotal\nIP Address {ip_address} is not a public IP Address\n"
    else:
        if 'network' in data['data']['attributes']:
            network = f"Network: {data['data']['attributes']['network']}"
        else:
            network = "Network: N/A"
        harmless_report = f" - Harmless: {data['data']['attributes']['last_analysis_stats']['harmless']}"
        malicious_report = f" - Malicious: {data['data']['attributes']['last_analysis_stats']['malicious']}"
        suspicious_report = f" - Suspicious: {data['data']['attributes']['last_analysis_stats']['suspicious']}"
        output = f"\n[+] VirusTotal\nSecurity Vendors' Analysis\n{harmless_report}\n{malicious_report}\n{suspicious_report}\n{network}\n"

    return output

def main():
    options = get_arguments()
    api_key = check_key()
    response = fetch_data(options.ip_address, api_key)
    output = filter_data(response)
    print(output)

if __name__ == '__main__':
    main()