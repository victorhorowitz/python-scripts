#!/usr/bin/python3.11

import subprocess
import re
import argparse
import sys

# Restart VM or device to restore MAC address

# Uses argparse module to collect interface and MAC address arguments and return them as an object
def get_arguments():
    parser = argparse.ArgumentParser(prog='mac_changer.py', description='Change Mac Address for Provided Interface!')
    parser.add_argument('-i', '--interface', required=True, help='selected interface', type=interface_input_check)
    parser.add_argument('-m', '--mac', required=True, metavar='MAC ADDRESS', help='new MAC Address', type=mac_format)
    args = parser.parse_args()
    return args


# Checks the MAC address entered as an argument in the get_arguments function is formatted correctly
def mac_format(m):
    input_mac = re.search(r'^\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}$', m)
    try:
        if input_mac.group(0):
            return m
    except Exception as error:
        print("[+] Error: please provide the mac address in a colon separated format like 00:1b:63:84:45:66")
        sys.exit(1)


# Checks the interface entered as an argument to the get_arguments function exists and has a MAC address
def interface_input_check(i):
    interface_output = subprocess.run(["ifconfig", i], capture_output=True, text=True)
    mac = re.search(r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}', interface_output.stdout)
    if mac:
        return i
    elif interface_output.returncode != 0:
        print(f"[+] Error: the interface {i} does not exist")
        sys.exit(1)
    elif mac is None:
        print(f"[+] Error: the interface {i} does not have a MAC address, enter a different interface")
        sys.exit(1)


# Changes MAC address using BASH commands
def change_mac(interface, mac_address):
    print(f"[+] Changing MAC Address for {interface} to {mac_address}")
    subprocess.run(["ifconfig", interface, "down"], check=True)
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_address], check=True)
    subprocess.run(["ifconfig", interface, "up"], check=True)


# Checks changed MAC address is equal to MAC address user inputted
def check_mac(interface, mac_address):
    ifconfig = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    mac = re.search(r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}', ifconfig.stdout)
    if mac.group(0) == mac_address:
        print(f"[+] MAC Address was successfully changed to {mac_address}")
    else:
        print("the MAC Address did not change successfully")


if __name__ == '__main__':
    options = get_arguments()
    change_mac(options.interface, options.mac)
    check_mac(options.interface, options.mac)




