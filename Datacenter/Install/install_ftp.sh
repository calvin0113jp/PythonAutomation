#!/bin/bash

apt -y install vsftpd
systemctl status vsftpd
cp vsftpd.conf /etc/vsftpd.conf
