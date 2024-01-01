import subprocess
import requests
def scan_wifi(interface='wlan0'):
    result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=Bssid"], capture_output=True)
    if result.returncode != 0:
        raise Exception("Fehler beim Scannen der WLAN-Netzwerke")
    
    # Speichere die Rohdaten-Ausgabe in einer Datei namens "output.txt"
    with open("output.txt", "wb") as file:
        file.write(result.stdout)
def ip_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        
        # Speichern Sie die Informationen in einer output.txt-Datei
        with open("output.txt", "w") as file:
            for key, value in data.items():
                file.write(f"{key}: {value}\n")
        
        return "IP-Informationen wurden in output.txt gespeichert."
    except Exception as e:
        return str(e)




