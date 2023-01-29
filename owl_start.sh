#!/bin/bash

mv OwlAccessTerminal /usr/bin
chmod 755 /usr/bin/OwlAccessTerminal
mkdir -p /etc/owl
mv owl_configure.py /etc/owl
chmod 755 /etc/owl/owl_configure.py
sed -i "13a python3 /etc/owl/owl_configure.py" /etc/rc.local
sed -i "14a nohup OwlAccessTerminal -c /etc/owl/config.json > /etc/owl/owl.log &" /etc/rc.local
# reboot

