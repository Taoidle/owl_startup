import os
import json
import subprocess

CM_W = 800
CM_H = 600
VC_API = "CAP_V4L"
FRONT_USB = "usb-1c1c000.usb-1"
CONFIG_PATH = '/etc/owl/owl_terminal_config.json'
ALGORITHM_PATH = '/etc/owl/algorithm/map_calc.js'
CAMERA_READ_MAX_MS = 500
CAMERA_READ_RETRY_MS = 100
CAMERA_READ_RETRY_TIMES = 5

def getUsbSerialNum(device: str) -> str:
    return subprocess.Popen("v4l2-ctl -d " + device.strip('\n') + " --info | grep \"Bus info\" | awk '{print $4}'", shell=True,
                            stdout=subprocess.PIPE).stdout.readline().decode('utf-8').strip('\n')


def getCameraDevices() -> list:
    video_devices_list = os.popen('ls /dev | grep video').readlines()
    devices_list = []
    devices_usb_list = []
    devices_real_list = []
    for i in range(len(video_devices_list)):
        item_info_1 = getUsbSerialNum('/dev/' + video_devices_list[i].strip('\n'))
        if "usb" in item_info_1:
            devices_list.append('/dev/video' + str(i))
            devices_usb_list.append(item_info_1)
    if devices_usb_list[0] == devices_usb_list[1]:
        for i in range(0, len(devices_usb_list) - 1, 2):
            devices_real_list.append(devices_list[i])
    else:
        for i in range(len(devices_usb_list),1):
            devices_real_list.append(devices_list[i])
    return devices_real_list


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
            "camera_read_max_ms": CAMERA_READ_MAX_MS,
            "camera_read_retry_ms": CAMERA_READ_RETRY_MS,
            "camera_read_retry_times": CAMERA_READ_RETRY_TIMES,
            "downCameraId": 2,
            "frontCameraId": 1,
            "multicast_address": "239.255.0.1",
            "multicast_port": 30003,
            "listen_address": "0.0.0.0",
            "multicast_interval_seconds": 15,
            "cmd_nmcli_path": "nmcli",
            "cmd_bash_path": "/bin/bash",
            "js_map_calc_file": ALGORITHM_PATH,
            "js_map_calc_function_name": "calc_map_position",
            "disable_multicast": 0,
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
            json_data["camera_read_max_ms"] = CAMERA_READ_MAX_MS,
            json_data["camera_read_retry_ms"] = CAMERA_READ_RETRY_MS,
            json_data["camera_read_retry_times"] = CAMERA_READ_RETRY_TIMES,
            json_data["js_map_calc_file"] = ALGORITHM_PATH
        with open(CONFIG_PATH, 'w', encoding='utf-8') as fw:
            json.dump(json_data, fw, ensure_ascii=False)
        fw.close()
        fr.close()
