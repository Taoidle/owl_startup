import os
import json

CONFIG_PATH = '/etc/owl/owl_apriltag_config.json'
START_MS = 1000
DURATION_MS = 300
TIMEOUT_MS = 1000
TIMEOUT_COUNT = 6
AP_W = 640
AP_H = 480

if __name__ == '__main__':
    if not os.path.exists(CONFIG_PATH):
        os.system(r'touch %s' % CONFIG_PATH)
        json_dict = {
            "configTagProcessor": {
                "timeStartMs": START_MS,
                "timeDurationMs": DURATION_MS,
                "timeoutCountLimit": TIMEOUT_COUNT
            },
            "configAprilTagData": {
                "resizeWidth": AP_W,
                "resizeHeight": AP_H,
                "aprilTagDetectorMaxHammingBitsCorrected": 1
            },
            "configGetImage": {
                "host": "127.0.0.1",
                "port": "23331",
                "target": "/1",
                "version": 11,
                "timeoutMs": TIMEOUT_MS
            },
            "configSendResult": {
                "host": "127.0.0.1",
                "port": "23331",
                "target": "/cmd",
                "version": 11,
                "timeoutMs": TIMEOUT_MS
            }
        }
        with open(CONFIG_PATH, "w", encoding='utf-8') as f:
            f.write(json.dumps(json_dict, ensure_ascii=False))
        f.close()
    else:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as fr:
            json_data = json.load(fr)
            json_data["configTagProcessor"]["timeStartMs"] = START_MS
            json_data["configTagProcessor"]["timeDurationMs"] = DURATION_MS
            json_data["configTagProcessor"]["timeoutCountLimit"] = TIMEOUT_COUNT
            json_data["configAprilTagData"]["resizeWidth"] = AP_W
            json_data["configAprilTagData"]["resizeHeight"] = AP_H
            json_data["configGetImage"]["timeoutMs"] = TIMEOUT_MS
            json_data["configSendResult"]["timeoutMs"] = TIMEOUT_MS
        with open(CONFIG_PATH, 'w', encoding='utf-8') as fw:
            json.dump(json_data, fw, ensure_ascii=False)
        fw.close()
        fr.close()