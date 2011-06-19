#!/bin/bash
. /etc/mac-anonymity

connection_type="$1"

if [ "${connection_type}" == "wireless" ]; then
        essid="$2"
        bssid="$3"

	if [ "$bssid" == "$HOME_NETWORK_MAC" ]
	then
		ifconfig wlan0 down
		macchanger -m "$IDENTIFY_TO_HOME_NETWORK" wlan0
		ifconfig wlan0 up
	else
		ifconfig wlan0 down
		macchanger -r wlan0
		ifconfig wlan0 up
	fi
fi
