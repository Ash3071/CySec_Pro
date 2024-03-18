#!/usr/bin/env python

import subprocess
import argparse
import re
def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Used to set the network interface.")
    parser.add_argument("-m", "--mac", dest="new_mac", help="Used to set the new mac address.")
    parser.add_argument("-M", "--MAC", dest="current_mac", action="store_true", help="Display current mac address.")

    options = parser.parse_args()

    if not (options.new_mac or options.current_mac):
        print(f"Please enter either -m or --mac (to change the mac address) or enter --M or --MAC (to view the current MAC address")
        exit(1)
    else:
        return options

def change_mac(interface, new_mac):
    mac_search_result = get_mac_address(interface)
    print(f"[+] Changing MAC address for {interface} from {mac_search_result.group(0)} to {new_mac}")

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac_address(interface):
    current_mac_address = subprocess.check_output(["ifconfig", interface], universal_newlines=True)
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", current_mac_address)
    return mac_search_result

def display_current_mac(interface):
    mac_search_result = get_mac_address(interface)
    if mac_search_result:
        print(f"MAC address --> {mac_search_result.group(0)}")
    else:
        print(f"[-] MAC address not found!!!!")

options = get_arguments()

if (options.interface and options.new_mac):
    change_mac(options.interface, options.new_mac)
else:
    display_current_mac(options.interface)
