import os
import subprocess

network_status_list = subprocess.Popen("nmcli device status | grep \" wifi \" | awk '{print $1} {print $3} {print $4}'", shell=True, stdout=subprocess.PIPE).stdout.readlines()
network_device = network_status_list[0].decode('utf-8').strip('\n')
network_status = network_status_list[1].decode('utf-8').strip('\n')
network_connection = network_status_list[2].decode('utf-8').strip('\n')
if network_status == "disconnected" and network_connection != "Hotspot":
    hotspot_check = subprocess.Popen(" nmcli c show | grep \"Hotspot\" | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.readline().decode('utf-8').strip('\n')
    if hotspot_check is not None:
        os.system("nmcli c up Hotspot")
    else:
        ssid = "owl_" + network_device.strip("wlx")
        os.system("nmcli dev wifi hotspot ssid \"" + ssid + "\" password \"12345678\"")
