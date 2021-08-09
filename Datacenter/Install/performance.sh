#!/bin/bash

interface=eth1

setpci -s 0b:00.0 68.w=5936

#Adjest ring size
ethtool -G $interface rx 8192 tx 8192
ethtool -g $interface

#Queue Length
ifconfig $interface txqueuelen 20000
ifconfig $interface mtu 9000

mlnx_tune -p HIGH_THROUGHPUT
