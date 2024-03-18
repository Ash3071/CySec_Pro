#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", required=True, help="Used to enter the ip address or address range")
    options = parser.parse_args()
    return options

#Function to send ARP Broadcast
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadCast_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadCast = broadCast_request/arp_request
    answered_host = scapy.srp(arp_request_broadCast, timeout=1, verbose=False)[0]
    host_list = []
    for element in answered_host:
        host_dictionary = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        host_list.append(host_dictionary)
    return host_list

def printResult(scan_result):
    print(f"IP Address\t\t\t MAC Address")
    for host in scan_result:
        print(f"{host['ip']}\t\t\t {host['mac']}")

options = get_arguments()
scan_result = scan(options.target_ip)
printResult(scan_result)
