#!/usr/bin/env python3

import requests
import json
import yaml
from yaml.loader import SafeLoader
import pycountry
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
    if config['abuseipdb'] == 'your_api_key_goes_here':
        print('\n[-] AbuseIPDB is missing an API Key\n')
        exit()
    else:
        return config['abuseipdb']

def fetch_data(ip_address, api_key): # Requests data
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '365'
    }

    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    decodedResponse = json.loads(response.text)

    return decodedResponse

def filter_data(data): # Filters data
    if 'errors' in data:
        details = f"Details: {data['errors'][0]['detail']}"
        output = f"\n[-] AbuseIPDB\n{details}\n"
    elif data['data']['isPublic'] == False:
        ip_address = data['data']['ipAddress']
        output = f'\n[-] AbuseIPDB\nIP Address {ip_address} is not a Public IP Address.\n'
    else:
        country_code = data['data']['countryCode']
        country_name = pycountry.countries.get(alpha_2=country_code).name
        a_conf = f"Abuse Confidence: {data['data']['abuseConfidenceScore']}%"
        country = f"Country: {country_name}"
        isp = f"ISP: {data['data']['isp']}"
        usage_type = f"Usage Type: {data['data']['usageType']}"
        domain = f"Domain: {data['data']['domain']}"
        hostnames_list = ', '.join(map(str, data['data']['hostnames']))
        hostnames = f"Hostnames: {hostnames_list}"
        whitelist = f"Whitelisted: {data['data']['isWhitelisted']}"
        reports = f"Reports: {data['data']['totalReports']}"
        output = f"\n[+] AbuseIPDB\n{a_conf}\n{country}\n{isp}\n{usage_type}\n{domain}\n{hostnames}\n{whitelist}\n{reports}\n"
    return output

def main():
    options = get_arguments()
    api_key = check_key()
    response = fetch_data(options.ip_address, api_key)
    output = filter_data(response)
    print(output)

if __name__ == '__main__':
    main()