#solving API Trivia Challenges
# CHALLENGES AT THE MOMENT
# What is the serial number of the AP in the network “I love API”?
# How many SSIDs are ENABLED in the wireless network “I love API”?
# What is the WAN IP address and the firmware version of the MX in “I love API” network?
# When was the last wireless association of the “Mercury” device in the “I love API” network? You should be able to know the date and time
# Create a combined network (MX, MS and MR) with your name
# Add a new public IP address to the Uplink statistics of the MX in your network
# Create a Layer 7 firewall rule in your network blocking the webpage [yourname.com]
# Create a group policy with your name and assign it to one of the VLANs in your MX



#solutions
# 1. What is the serial number of the AP in the network “I love API”?

import requests
import json
from api_key import key
from pprint import pprint

url_base = "https://api.meraki.com/api/v0/"




#first we need to get the org ID

def get_org_details(key):
    url = url_base + "organizations"
    payload = {}
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }

    r = requests.get(url, headers=headers, data = payload)

    #retrieve data from the response

    output = json.loads(r.text)

    org_id = output[0]['id']
    org_name = output[0]['name']
    org_url = output[0]['url']


    return [org_id,org_name,org_url]

#Now we list the networks in the organization

def get_org_networks(org_id,key):
    url_networks = url_base + "organizations/" + org_id + "/networks"


    payload = {}
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }

    r_networks = requests.get(url_networks, headers=headers, data = payload)

    output_networks = json.loads(r_networks.text)

    return output_networks

#Now get devices in network

def get_network_devices(network_id,key):
    url_network_devices = url_base + "networks/" + network_id + "/devices"


    payload = {}
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }

    r_networks = requests.get(url_network_devices, headers=headers, data = payload)

    output_devices = json.loads(r_networks.text)

    return output_devices

"""
org_id = get_org_details(key)[0]

network_id = get_org_networks(org_id,key)[0]['id']

network_devices = get_network_devices(network_id,key)
print(network_devices)

serial_number = network_devices[1]['serial']

print(serial_number)
"""
# 2.How many SSIDs are ENABLED in the wireless network “I love API”?



def get_network_ssids(network_id,key):
    url = url_base + "networks/" + network_id + "/ssids"

    payload = {}
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }


    r_ssids =requests.get(url, headers= headers, data=payload)

    output_ssids = json.loads(r_ssids.text)

    return output_ssids

def get_enable_network_ssids(ssids):
    list_of_ssids = []
    for entry in ssids:
        if entry['enabled'] == True:
            list_of_ssids.append(entry)


    return list_of_ssids

"""


org_id = get_org_details(key)[0]

network_id = get_org_networks(org_id,key)[0]['id']


ssids = get_network_ssids(network_id,key)
enable_ssids = get_enable_network_ssids(ssids)

number_of_enabled_ssids = len(enable_ssids)
"""

#3 What is the WAN IP address and the firmware version of the MX in “I love API” network?

"""
org_id = get_org_details(key)[0]

network_id = get_org_networks(org_id,key)[0]['id']


network_devices =get_network_devices(network_id,key)

for entry in network_devices:
    mx_details = []
    if entry['model'].startswith('MX'):
        mx_details.append(entry['firmware'])
        mx_details.append(entry['wan1Ip'])

print("MX firmware: {}".format(mx_details[0]))
print("MX WAN IP : {}".format(mx_details[1]))

"""


# Create a combined network (MX, MS and MR) with your name


def create_network(org_id,key):
    url = url_base + "organizations/" + org_id + "/networks"


    payload = {
        "name": "John Mensah Onumah",
        "type": " appliance switch wireless",
        "timeZone": "America/Chicago"
    }
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }


    r_create_network = requests.post(url, headers=headers, data=payload)

    print(r_create_network.status_code)
    pprint(json.loads(r_create_network.text))


# org_id = get_org_details(key)[0]
# create_network(org_id,key)

# network_devices = get_network_devices('L_706502191543752614',key)

# pprint(network_devices)

def get_org_inventory(org_id,key):
    url_networks = url_base + "organizations/" + org_id + "/inventory"


    payload = {}
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }

    r_org_devices = requests.get(url_networks, headers=headers, data = payload)

    org_devices = json.loads(r_org_devices.text)

    return org_devices


# org_id = get_org_details(key)[0]

# devices = get_org_inventory(org_id,key)

# pprint(devices)


# 6.Add a new public IP address to the Uplink statistics of the MX in your network

def update_connectivity_destination(network_id,key):

    url = url_base + "networks/" + network_id + "/connectivityMonitoringDestinations"


    # payload = {
    #     "ip": "1.1.1.1",
    #     "description": "cloudflare",
    #     "default": False

    # }


    destinations = [{"ip": "8.8.8.8", "description": "Google", "default": True},{"ip": "1.1.1.1", "description": "cloudflare", "default": False}]

    payload = {
        'destinations': destinations
    }
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }

    res_update_monitoring = requests.put(url, headers=headers, json=payload)

    print(res_update_monitoring.status_code)
    output = json.loads(res_update_monitoring.text)

    return output


# org_id = get_org_details(key)[0]

# network_id = get_org_networks(org_id,key)[0]['id']

# pprint(get_org_networks(org_id,key))

# network_id = 'L_706502191543752614'

# response = update_connectivity_destination(network_id,key)

# pprint(response)



def find_network_id(network_name,org_id,key):
    networks = get_org_networks(org_id,key)

    for network in networks:
        if network['name'] == network_name:
            return network['id']
            exit

# 7 Create a Layer 7 firewall rule in your network blocking the webpage [yourname.com]

def update_l7firewall_rule(network_id,key):

    url = url_base + "networks/" + network_id + "/l7FirewallRules"


    payload = {
        "rules": [
        {"policy": "deny",
        "type": "host",
        "value": "johnonumah.com"
            }
        ]
    }
    headers = {
    'X-Cisco-Meraki-API-Key': key
    }

    res_update_l7rule = requests.put(url, headers=headers, json=payload)

    print(res_update_l7rule.status_code)
    output = json.loads(res_update_l7rule.text)

    return output


# org_id = get_org_details(key)[0]


# network_id = find_network_id('John Mensah Onumah',org_id,key)

# response = update_l7firewall_rule(network_id,key)

# pprint(response)



# Create a group policy with your name and assign it to one of the VLANs in your MX

def create_group_policy(network_id,key):
    url = url_base + "networks/" + network_id + "/groupPolicies"


    payload = {
    "name": "John Onumah",
    "scheduling": {
        "enabled": False
    },
    "bandwidth": {
        "settings": "network default"
    },
  
    "vlanTagging": {
        "settings": "network default"
    },         
    }

    headers = {
    'X-Cisco-Meraki-API-Key': key
    }


    res_update_groupPolicies = requests.post(url, headers=headers, json=payload)

    print(res_update_groupPolicies.status_code)
    output = json.loads(res_update_groupPolicies.text)

    return output




org_id = get_org_details(key)[0]


network_id = find_network_id('John Mensah Onumah',org_id,key)

response = create_group_policy(network_id,key)

pprint(response)
