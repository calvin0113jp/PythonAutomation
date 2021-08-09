#!/bin/bash

#--------------------------------------------

interface=eth1
ip=100.100.100.100
port=100
iperf_file=iperf_pc2.log
ib_file=ib_pc2.log

#--------------------------------------------


echo -e "\033[33mKill Process \033[0m"

killall iperf
killall ib_write_bw

echo -e "\033[33mStarting traffic \033[0m"

iperf -c $ip -t 60 -i 5 -P 10 -p $port | tee $iperf_file &
ib_write_bw -d mlx5_0 --report_gbits --run_infinite -p 10000 -F $ip | tee $ib_file &

# Send the iperf log every 5 sec to server1
while true;
do
	sleep 5
	scp $iperf_file  root@192.168.1.20:/root/$iperf_file 
	scp $ib_file root@192.168.1.20:/root/$ib_file
done
