import os
import json
import subprocess

CM_W = 800
CM_H = 600
VC_API = "CAP_V4L"
FRONT_USB = "usb-1c1c000.usb-1"
CONFIG_PATH = '/etc/owl/owl_terminal_config.json'


def getUsbSerialNum(device: str) -> str:
    return subprocess.Popen("v4l2-ctl -d " + device.strip('\n') + " --info | grep \"Bus info\" | awk '{print $4}'", shell=True,
                            stdout=subprocess.PIPE).stdout.readline().decode('utf-8').strip('\n')

def getCameraDevices() -> list:
    video_devices_list = os.popen('ls /dev | grep video').readlines()
    video_total_devices_num = len(video_devices_list)
    devices_list = []
    for i in range(len(video_devices_list) - 1):
        item_info_1 = getUsbSerialNum('/dev/' + video_devices_list[i].strip('\n'))
        if "usb" in item_info_1:
            if item_info_1 == getUsbSerialNum('/dev/' + video_devices_list[i + 1]).strip('\n') and str('/dev/video' + str(i)) not in devices_list: devices_list.append('/dev/video' + str(i))
            else:
                if 0 <= i - 1 < video_total_devices_num and getUsbSerialNum('/dev/' + video_devices_list[i - 1]).strip('\n') == item_info_1 and str('/dev/video' + str(i + 1)) not in devices_list: devices_list.append('/dev/video' + str(i + 1))
    return devices_list


if __name__ == '__main__':
    camera_devices = getCameraDevices()
    usb1_num = getUsbSerialNum(camera_devices[0])

    if usb1_num == FRONT_USB:
        front_camera = camera_devices[0]
        bottom_camera = camera_devices[1]
    else:
        front_camera = camera_devices[1]
        bottom_camera = camera_devices[0]

    if not os.path.exists(CONFIG_PATH):
        os.system(r'touch %s' % CONFIG_PATH)
        json_dict = {
            "CommandServiceUdpPort": 23333,
            "CommandServiceHttpPort": 23338,
            "ImageServiceTcpPort": 23332,
            "ImageServiceHttpPort": 23331,
            "EmbedWebServerHttpPort": 81,
            "airplane_fly_serial_baud_rate": 115200,
            "airplane_fly_serial_addr": "/dev/ttyS1",
            "camera_addr_1": front_camera,
            "camera_1_VideoCaptureAPI": VC_API,
            "camera_1_w": CM_W,
            "camera_1_h": CM_H,
            "camera_addr_2": bottom_camera,
            "camera_2_VideoCaptureAPI": VC_API,
            "camera_2_w": CM_W,
            "camera_2_h": CM_H,
            "downCameraId": 2,
            "frontCameraId": 1,
            "cmd_nmcli_path": "nmcli",
            "cmd_bash_path": "/bin/bash",
            "embedWebServer": {
                "doc_root": "./html",
                "index_file_of_root": "index.html",
                "backend_json_string": "{}",
                "allowFileExtList": "htm html js json jpg jpeg png bmp gif ico svg css"
            },
            "wifiCmd": {
                "enable": "nmcli wifi on",
                "ap": "nmcli dev wifi hotspot ssid \"<SSID>\" password \"<PWD>\" | cat",
                "connect": "nmcli dev wifi connect \"<BSSID>\" password \"<PWD>\" | cat",
                "scan": "nmcli dev wifi list | cat",
                "showHotspotPassword": "nmcli dev wifi show-password | cat",
                "getWlanDeviceState": "nmcli dev wifi list ifname \"<DEVICE_NAME>\" | cat",
                "listWlanDevice": "nmcli dev status | grep \" wifi \""
            }
        }
        with open(CONFIG_PATH, "w", encoding='utf-8') as f:
            f.write(json.dumps(json_dict, ensure_ascii=False))
        f.close()
    else:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as fr:
            json_data = json.load(fr)
            json_data["camera_addr_1"] = front_camera
            json_data["camera_1_VideoCaptureAPI"] = VC_API
            json_data["camera_1_w"] = CM_W
            json_data["camera_1_h"] = CM_H
            json_data["camera_addr_2"] = bottom_camera
            json_data["camera_2_VideoCaptureAPI"] = VC_API
            json_data["camera_2_w"] = CM_W
            json_data["camera_2_h"] = CM_H
        with open(CONFIG_PATH, 'w', encoding='utf-8') as fw:
            json.dump(json_data, fw, ensure_ascii=False)
        fw.close()
        fr.close()
