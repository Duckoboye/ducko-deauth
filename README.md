# Ducko-DeAuth
This is a simple program(script?) to send WiFi deauth frames to the specified MAC. Built for IEEE 802.11.
Primarily depends on Scapy. Linux-exclusive as I'm too lazy to figure out how to make it cross-platform.
Built it to understand how deauth attacks work.

### dependencies
* Scapy [https://scapy.net/]
* iwconfig
* ifconfig  
*Both iw and if are usually installed by default*

### usage
deauth.py [-h] [-i INTERFACE] [-c COUNT] [-b BSSID] [-t TARGET_MAC] [-e INTERVAL] [-m] [-f]

optional arguments:
 **-h, --help**
 show this help message and exit
	
  **-i INTERFACE, --interface INTERFACE**
	* Interface used to send packets from
	
  **-c COUNT, --count COUNT**
	* Amount of deauth frames to send
	
  **-b BSSID, --bssid BSSID**
	* BSSID of target AP
	
  **-t TARGET_MAC, --target-mac TARGET_MAC**
	* MAC address of the target machine
	
  **-e INTERVAL, --interval INTERVAL**
	Time between packets in ms. Default: 0.100
	
  **-m, --keep-monitor**
	Keep monitor mode enabled after packets are sent.
	
  **-f, --kill-networkmanager**
	Stops NetworkManager before enabling monitor mode so it can't interfere.
	
