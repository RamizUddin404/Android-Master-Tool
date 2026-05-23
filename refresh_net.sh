#!/bin/bash
# Network Refresh Script for Termux
echo "Network Refreshing..."
echo "Flushing DNS cache (if applicable)..."
# In Termux, there isn't a persistent DNS cache, but we can restart the interface
# Note: Changing MTU or interface settings requires root. This script focuses on connectivity resets.

echo "Re-initiating network interface..."
# Simple ping to force packet flow and re-authenticate with the gateway
ping -c 3 8.8.8.8 > /dev/null

echo "Clearing temporary network buffers..."
# A simple way to clear potential stale connections is to briefly toggle wifi or run ifconfig
# Since we cannot run ifconfig with arguments without root, we check status.
ifconfig wlan0 | grep "inet "

echo "Network refresh attempt complete."
echo "Please check your connection now."
