#!/bin/bash

interface=enp10s0f0

echo -e "\033[33mInstall Common Package\033[0m"
apt install -y linux-tools-common
apt install -y linux-tools-5.0.0-32-generic
apt install -y tuned
apt install -y iperf
apt install -y linux-tools-generic

echo -e "\033[33mTune environment\033[0m"
lspci |grep Mellanox

systemctl stop irqbalance.service
systemctl disable irqbalance.service
cpupower  frequency-set -g performance
tuned-adm profile throughput-performance
mlnx_tune -p HIGH_THROUGHPUT

MellanoxNO=$(lspci | grep Mellanox |head -c 7)
echo -e "\033[33m Bus number = "$MellanoxNO"\033[0m"

lspci -vvs $MellanoxNO |grep -i numa 
setpci -s $MellanoxNO 68.w
setpci -s $MellanoxNO 68.w=5957

setpci=$(setpci -s $MellanoxNO 68.w)

if [ $setpci -eq 5957 ]; then
	echo -e "\033[33m setpci 5957 ok\033[0m"
	setpci_result=Passed
else
	echo -e "\033[33m setpci 5957 failed\033[0m"
	setpci_result=Failed
fi

NUMA_range=$(lscpu |grep "NUMA node0" |tail +22c)
echo -e "\033[33m NUMA 0 range = $NUMA_range\033[0m"
set_irq_affinity_cpulist.sh $NUMA_range $interface

#----------------------------------------------------------
#ethtool tuning
#Adjest ring size
ethtool -G $interface rx 8192 tx 8192
ethtool -g $interface

#Queue Length
ifconfig $interface txqueuelen 20000
ifconfig $interface mtu 9000

echo "-----------------------------------------------------"
echo -e "\033[33m Bus number = "$MellanoxNO" \033[0m"
echo -e "\033[33m Set PCI result = "$setpci_result" \033[0m"
echo -e "\033[33m NUMA 0 range = $NUMA_range\033[0m"
echo "-----------------------------------------------------"

