#!/bin/bash

mv OwlAccessTerminal /usr/bin
chmod 755 /usr/bin/OwlAccessTerminal
mv OwlAprilTagProcessor /usr/bin
chmod 755 /usr/bin/OwlAprilTagProcessor
mkdir -p /etc/owl
mv *.py /etc/owl
chmod 755 /etc/owl/owl_terminal_configure.py /etc/owl/owl_apriltag_configure.py
python3 /etc/owl/owl_apriltag_configure.py
mv *.service /etc/systemd/system/
chmod 777 /etc/systemd/system/owl-terminal.service /etc/systemd/system/owl-apriltag.service
systemctl enable owl-terminal.service owl-apriltag.service