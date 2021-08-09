#!/bin/bash
#Disable netplan

interface=enp6s0


apt-get -y update
apt-get install ifupdown

ifdown --force $interface lo && ifup -a
systemctl unmask networking
systemctl enable networking
systemctl restart networking

sleep1
systemctl stop systemd-networkd.socket systemd-networkd \
networkd-dispatcher systemd-networkd-wait-online

systemctl disable systemd-networkd.socket systemd-networkd \
networkd-dispatcher systemd-networkd-wait-online

systemctl mask systemd-networkd.socket systemd-networkd \
networkd-dispatcher systemd-networkd-wait-online

apt-get --assume-yes purge nplan netplan.io
