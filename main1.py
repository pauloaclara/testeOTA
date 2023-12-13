from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD
from machine import Pin, Timer, RTC
import utime
import time

ledOnBoard = Pin("LED", Pin.OUT)
ledOnBoard.on()
#time=Timer()
firmware_url = "https://raw.githubusercontent.com/pauloaclara/testeOTA/main/"

while True:
    print("slpeeping")
    time.sleep(2)

    for i in range(10):
        ledOnBoard.on()
        time.sleep(1)
        ledOnBoard.off()
        time.sleep(0.5)
    #time.sleep(0.5)
    try:
        ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main1.py")
        ota_updater.download_and_install_update_if_available()
        for i in range(10):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    
    except:
        ledOnBoard.on()
        time.sleep(1)
