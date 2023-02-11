#!/bin/bash

mv OwlAccessTerminal /usr/bin
chmod 755 /usr/bin/OwlAccessTerminal
mv OwlAprilTagProcessor /usr/bin
chmod 755 /usr/bin/OwlAprilTagProcessor
mkdir -p /etc/owl
mv *.py /etc/owl
chmod 755 /etc/owl/*.py
python3 /etc/owl/owl_apriltag_configure.py
git clone https://github.com/Taoidle/OwlNetworkManager.git
mv OwlNetworkManager/ /etc/owl/net-server
chmod 755 /etc/owl/net-server/*
chmod 755 *.service *.timer
mv *.service *.timer /etc/systemd/system/
systemctl start owl-net-timer.timer
systemctl enable owl-net-config-server.service owl-net-timer.timer owl-terminal.service owl-apriltag.service