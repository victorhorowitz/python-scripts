import scapy.all as scapy
import argparse

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address")
    print("-----------------------------------")
    for client in results_list:
        print(client["ip"] + "\t\t" + client["mac"])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide an IP or subnet to scan for online hosts')
    parser.add_argument('-i', required=True, help='ip address or subnet (subnet syntax: <ip>/<subnet> e.g. 172.16.160.0/24)')
    args = parser.parse_args()

    scan_result = scan(args.i)
    print_result(scan_result)
