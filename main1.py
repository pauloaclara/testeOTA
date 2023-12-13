from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD
from machine import Pin, Timer, RTC

ledOnBoard = Pin("LED", Pin.OUT)
ledOnBoard.on()

firmware_url = "https://raw.githubusercontent.com/pauloaclara/testeOTA/main/"

#while True:
    ledOnBoard.on()
    #try:
        ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main1.py")
        ota_updater.download_and_install_update_if_available()
        if ledOnBoard.on():
            ledOnBoard.off()
        else:
            ledOnBoard.off()
    #except:
        ledOnBoard.on()
