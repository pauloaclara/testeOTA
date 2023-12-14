from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD
from machine import Pin, Timer, RTC
import utime
import time

ledOnBoard = Pin("LED", Pin.OUT)
desliga = Pin(0, Pin.OUT)

ledOnBoard.on()
#time=Timer()
firmware_url = "https://raw.githubusercontent.com/pauloaclara/testeOTA/main/"
desliga.off()

while True:
    desliga.off()
    for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    print("slpeeping")
    time.sleep(2)
    desliga.off()
    for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    
    for i in range(30):
        ledOnBoard.on()
        time.sleep(0.03)
        ledOnBoard.off()
        time.sleep(0.03)
    #time.sleep(0.5)
    try:
        ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main1.py")
        ota_updater.download_and_install_update_if_available()
        
        for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
            
    
    except:
        ledOnBoard.on()
        time.sleep(1)
        
    print("vou apagar1")
    time.sleep(3)
    print("vou apagar2")
    time.sleep(3)
    desliga.on()
    for i in range(10):
        ledOnBoard.on()
        time.sleep(0.2)
        ledOnBoard.off()
        time.sleep(0.2)
