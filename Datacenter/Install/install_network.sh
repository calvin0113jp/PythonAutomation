#!/bin/bash

apt install resolvconf -y

cp sshd_config /etc/ssh/sshd_config
cp interfaces /etc/network/interfaces
service resolvconf restart
/etc/init.d/networking restart
service sshd restart

