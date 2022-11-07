#!/usr/bin/env python3

import requests
import argparse
import json
import yaml
from yaml.loader import SafeLoader

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
    if config['greynoise'] == 'your_api_key_goes_here':
        print('\n[-] GreyNoise is missing an API Key\n')
        exit()
    else:
        return config['greynoise']

def fetch_data(ip_address, api_key): # Requests data
    # api_client = GreyNoise(api_key)
    # response = api_client.ip(ip_address)
    # return response

    url = f'https://api.greynoise.io/v3/community/{ip_address}'

    headers = {
    'key': api_key
    }

    response = requests.request(method='GET', url=url, headers=headers)
    decodedResponse = json.loads(response.text)
    return decodedResponse

def filter_data(data): # Filters data
    # Get name, classification, last seen
    if 'status' in data:
        details = f"Details: Request is not a valid routable IPv4 address"
        output = f'\n[-] GreyNoise\n{details}\n'
    elif data['message'] != 'Success':
        details = f"Details: {data['message']}"
        output = f'\n[-] GreyNoise\n{details}\n'
    elif data['message'] == 'Success':
        name = f"Name: {data['name']}"
        classification = f"Classified: {data['classification']}"
        last_seen = f"Last Seen: {data['last_seen']}"
        output = f"\n[+] GreyNoise\n{name}\n{classification}\n{last_seen}\n"
    else:
        output = '\n[-] GreyNoise\nNo Data Available\n'
    return output

def main():
    options = get_arguments()
    api_key = check_key()
    response = fetch_data(options.ip_address, api_key)
    output = filter_data(response)
    print(output)

if __name__ == '__main__':
    main()