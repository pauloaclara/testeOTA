'''
https://raw.githubusercontent.com/pauloaclara/testeOTA/main/
atualiza o ficheiro outro e reinicia
para atualizar ligado ao PC - 20:02
para atualizar o main2 ligado à bateria/pilhas
2ª tentativa ligada à bateria pois parecia que tinha um fio desligado
04052025 nova tentativa com o OTA2 - vai ser necessário utilizar uma flag para renomear o ficheiro no main antes de chamar o programa principal
alterada o update_no_reset_no_rename
depois de ter modificado o ota3, esqueci de mudar aqui a biblioteca
tinha um erro de identação em ota3
sem mudar o nome
sei lá
'''

from ota3 import OTAUpdater
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
ledOnBoard.on()
time.sleep(2)


while True:
    desliga.off()
    for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    print("sleeping")
    time.sleep(2)
    desliga.off()
    for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    '''
    for i in range(30):
        ledOnBoard.on()
        time.sleep(0.03)
        ledOnBoard.off()
        time.sleep(0.03)
    #time.sleep(0.5)
    '''
    #try:
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main2.py")
        #ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "novo")
    ota_updater.download_and_install_update_if_available()
        #print(ota_updater.check_for_updates())
    '''     
        for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
            
    
    except:
        ledOnBoard.on()
        time.sleep(1)
        '''
    print("vou apagar1")
    time.sleep(3)
    print("vou apagar2")
    time.sleep(3)
    '''
    #desliga.on()
    for i in range(10):
        ledOnBoard.on()
        time.sleep(0.2)
        ledOnBoard.off()
        time.sleep(0.2)'''
    
