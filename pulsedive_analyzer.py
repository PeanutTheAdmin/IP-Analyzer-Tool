#!/usr/bin/env python3

import requests
import pulsedive
import yaml
from yaml.loader import SafeLoader
import argparse
import whois
import re

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
    if config['pulsedive'] == 'your_api_key_goes_here':
        print('\n[-] Pulsedive is missing an API Key\n')
        exit()
    else:
        return config['pulsedive']

def fetch_data(ip_address, api_key): # Requests data
    try:
        # Set Api Key
        pud = pulsedive.Pulsedive(api_key)
        # Fetch Data on IP Address
        decodedResponse = pud.indicator(value=ip_address)
    except requests.exceptions.HTTPError as e:
        error_code = str(e)
        if error_code[:3] == '404':
            decodedResponse = 404
        else:
            decodedResponse = 'OTHER'

    return decodedResponse

def filter_data(data): # Filters data
    # risk, stamp_updated, stamp_retired, whois - emails,
    # attributes with ports and technology
    if data == 404: # If 404 error then it is an invalid indicator
        output = f'\n[-] PulseDive\nDetails: Invalid IP Address or Not Found\n'
    elif data == 'OTHER': # Other exception has occured that has not been definded
        output = f'\n[-] PulseDive\nDetails: An unhandled error occured\n'
    else:
        risk = f"Risk: {data['risk']}" # Gets risk level
        updated = f"Updated: {data['stamp_updated']}" # Gets date of when it was last updated

        if data['stamp_retired'] == '': # Gets date if it was retired
            retired = f"Retired: N/A"
        else:
            retired = f"Retired: {data['stamp_retired']}"
        
        ports = get_ports_list(data) # Gets ports list
        technology = get_technology_list(data) # Gets technology list
        emails = get_abuse_emails(data) # Gets email abuse list
        
        output = f'\n[+] PulseDive\n{risk}\n{updated}\n{retired}\n{ports}\n{technology}\n{emails}\n'

    return output

def get_abuse_emails(data): # Kinda messy (if/else statments) and needs to be cleaned up
    if 'whois' in data['properties']:
        if 'contact' in data['properties']['whois']:
            email_list = re.findall(r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}', str(data['properties']['whois']['contact']))
            if len(email_list) > 1:
                email_list = [*set(email_list)] # filters out duplicates in list
                email_list.sort() # Sorts list from A-Z
                email_list = ', '.join(map(str, email_list))
                emails = f"Report Abuse: {email_list}"
            else:
                emails = f"Report Abuse: {email_list[0]}"
        elif 'whois' in data['properties']:
            email_list = re.findall(r'[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5}', str(data['properties']['whois']))
            if len(email_list) > 0:
                email_list = [*set(email_list)] # filters out duplicates in list
                email_list.sort() # Sorts list from A-Z
                email_list = ', '.join(map(str, email_list))
                emails = f"Report Abuse: {email_list}"
            else:
                emails = alt_abuse_emails(data['indicator'])
        else:
            emails = alt_abuse_emails(data['indicator'])
    else:
        emails = alt_abuse_emails(data['indicator'])
    
    return emails

# alternative way to get emails for abuse reporting, if pulse dive does not have emails then this will pull them.
def alt_abuse_emails(ip_address):
    try: # try/except block works to see if there is an email available via whois module.
        emails_output = whois.whois(ip_address).emails
        if type(emails_output) == list: # Checks to see if the output from whois is a list
            emails_output = ', '.join(map(str, emails_output))
            emails = f"Email Abuse: {emails_output}\n"
        else:
            emails = f"Email Abuse: {emails_output}\n"
    except FileNotFoundError: # if no email was available 
        emails = 'Report Abuse: N/A'
    return emails

def get_ports_list(data): # Gets list of ports
    if 'port' in data['attributes']:
        if len(data['attributes']['port']) > 1:
            ports_list = ', '.join(map(str, data['attributes']['port']))
            ports = f"Ports: {ports_list}"
        else:
            ports = f"Ports: {data['attributes']['port'][0]}"
    else:
        ports = "Ports: N/A"
    return ports

def get_technology_list(data): # Gets list of technology
    if 'technology' in data['attributes']:
        if len(data['attributes']['technology']) > 1:
            technology_list = ', '.join(map(str, data['attributes']['technology']))
            technology = f"Technology: {technology_list}"
        else:
            technology = f"Technology: {data['attributes']['technology'][0]}"
    else:
        technology = "Technology: N/A"
    return technology

def main():
    options = get_arguments()
    api_key = check_key()
    response = fetch_data(options.ip_address, api_key)
    output = filter_data(response)
    print(output)

if __name__ == '__main__':
    main()