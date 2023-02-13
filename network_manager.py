import os
import subprocess
import json
import requests

server_status = subprocess.Popen("systemctl status owl-network.service | grep Active | awk '{print $2}'", shell=True, stdout=subprocess.PIPE).stdout.readline().decode('utf-8').strip('\n')
if server_status == "active":
    info = requests.get('http://localhost:8000/api/status').json()
    if info['status'] == "disconnected":
        network_status_list = subprocess.Popen("nmcli device status | grep \" wifi \" | awk '{print $1} {print $3} {print $4}'", shell=True, stdout=subprocess.PIPE).stdout.readlines()
        network_connection = network_status_list[2].decode('utf-8').strip('\n')
        if network_connection != "Hotspot":
            os.system("nmcli dev wifi rescan")
            wifi_info = subprocess.Popen("nmcli dev wifi list | grep Infra | awk '$1!=\"*\"' | awk '{print $2} {print $7}'", shell=True, stdout=subprocess.PIPE).stdout.readlines()
            wifi_json = {}
            for i, count in zip(range(0, len(wifi_info), 2), range(len(wifi_info) // 2)):
                wifi_json.update({str(count): {"ssid": wifi_info[i].decode('utf-8').strip('\n'), "signal": wifi_info[i + 1].decode('utf-8').strip('\n')}})
            with open("/etc/owl/net-server/wifi_list.json", "w", encoding='utf-8') as f:
                f.write(json.dumps(wifi_json, ensure_ascii=False))
            f.close()
            hotspot_check = subprocess.Popen("nmcli c show | grep \"Hotspot\" | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout.readline().decode('utf-8').strip('\n')
            if hotspot_check != "":
                os.system("nmcli c up Hotspot")
            else:
                network_device = network_status_list[0].decode('utf-8').strip('\n')
                ssid = "owl_" + network_device.strip("wlx")
                os.system("nmcli dev wifi hotspot ssid \"" + ssid + "\" password \"12345678\"")
else:
    os.system("systemctl restart owl-network.service")