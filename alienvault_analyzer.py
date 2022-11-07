#!/usr/bin/env python3

from OTXv2 import OTXv2
from OTXv2 import IndicatorTypes
from OTXv2 import BadRequest
import argparse
import yaml
from yaml.loader import SafeLoader

def get_arguments(): # Gets The IP Address to Analyze
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest='ip_address', help='Sets IP Address to fetch information.')
    (options) = parser.parse_args()
    if not options.ip_address:
        parser.error('[-] Please Specify an IP Address to fetch information.')
    return options

def check_key():
    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=SafeLoader)
    if config['alienvault'] == 'your_api_key_goes_here':
        print('\n[-] AlienVault is missing an API Key\n')
        exit()
    else:
        return config['alienvault']

def fetch_data(ip_address, api_key): # Requests data
    try:
        otx = OTXv2(api_key)
        response = otx.get_indicator_details_by_section(IndicatorTypes.IPv4, ip_address)
    except BadRequest as e:
        response = f'Invalid IP Address ({ip_address})'

    return response

# Filters data
def filter_data(data):
    if type(data) == str:
        details = f"Details: {data}"
        output = f"\n[-] AlienVault\n{details}\n"
    elif len(data['validation']) > 0: # if validation contains data
        classification = which_source(data['validation'][0]['source'])
        reports = data['pulse_info']['count']
        output = f"\n[+] AlienVault\nClassification: {classification}\nReports: {reports}\n"
    elif 'validation' in data and len(data['pulse_info']['pulses']) > 0: # if validation key exist but there is no data in validation and there are pulses
        tags = get_tags(data)
        reports = data['pulse_info']['count']
        output = f"\n[+] AlienVault\nReports: {reports}\nTags: {tags}\n"
    elif 'validation' in data: # if validation key exist but there is no data in validation
        reports = data['pulse_info']['count']
        output = f"\n[+] AlienVault\nReports: {reports}\n"
    elif len(data['pulse_info']['pulses']) > 0: # if there is data in pulses
        tags = get_tags(data)
        reports = data['pulse_info']['count']
        output = f"\n[+] AlienVault\nReports: {reports}\nTags: {tags}\n"
    else:
        reports = data['pulse_info']['count']
        output = f"\n[+] AlienVault\nReports: {reports}\n"

    return output

# Gets tags and filters them from each pulse
def get_tags(data):
    raw_list = []
    for a in range(len(data['pulse_info']['pulses'])): # Loops over total number of pulses
        for b in range(len(data['pulse_info']['pulses'][a]['tags'])): # Loops over individual pulse
            raw_list.append(data['pulse_info']['pulses'][a]['tags'][b]) # appends each tag set in individual pulse
            for c in range(len(raw_list)): # loops over list and makes each item lowercase
                raw_list[c] = raw_list[c].lower()
    filtered_list = [*set(raw_list)] # filters out duplicates in list
    filtered_list.sort() # Sorts list from A-Z
    if filtered_list[0] == '': # Simple way to remove the first index if it contains nothing, just a quick way to clean the list
        filtered_list.pop(0)
    filtered_tags = ', '.join(map(str, filtered_list)) # Converts the list into a string seperated by commas
    return filtered_tags

def which_source(source):
    if source == 'cdn':
        classification = 'Content Delivery Network(CDN)'
    elif source == 'false_positive':
        classification = 'False Positive'
    elif source == 'cloud':
        classification = 'Cloud provider'
    else:
        classification = source
    return classification

def main():
    options = get_arguments()
    api_key = check_key()
    response = fetch_data(options.ip_address, api_key)
    output = filter_data(response)
    print(output)


if __name__ == '__main__':
    main()