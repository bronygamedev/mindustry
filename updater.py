import requests
import json
import subprocess
import time
from os import path

url = "https://api.github.com/repos/Anuken/Mindustry/releases/latest"
info = requests.get(url).content
info_parsed = json.loads(info)
base_path = path.dirname(path.abspath(__file__))
download_url = f'https://github.com/Anuken/Mindustry/releases/download/{info_parsed["tag_name"]}/Mindustry.jar'
config_file_path = base_path + "/config.json"
if path.isfile(config_file_path):
    with open(config_file_path, "r") as f:
        config = json.loads(f.read())
else:
    config = {"version": "v1"}


def check_for_version_change(new_version: str):
    current_version = config["version"].replace("v", "").split()
    new_version = new_version.replace("v", "").split()
    for index, i in enumerate(current_version):
        if new_version[index] != current_version[index]:
            return True
    return False


if __name__ == "__main__":
    if check_for_version_change(info_parsed["tag_name"]):
        with open("Mindustry.jar", "wb") as f:
            f.write(requests.get(download_url).content)
            f.close()
        config["version"] = info_parsed["tag_name"]
        with open(config_file_path, "w") as f:
            f.write(json.dumps(config))
