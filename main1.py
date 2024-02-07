#https://www.instructables.com/Raspberry-Pi-Pico-and-4x3-Keypad/
#https://www.electrosoftcloud.com/en/multithreaded-script-on-raspberry-pi-pico-and-micropython/
#https://github.com/octopuslab-cz/micropython-keypad -------
#https://www.youtube.com/watch?v=aRQMDSmFGCo ------ com buffer
#https://github.com/brettmclean/pad4pi
#https://www.youtube.com/watch?v=lzv9cwdU_ok
#https://www.youtube.com/watch?v=7-PoXmxeCmQ
#https://www.youtube.com/watch?v=7-PoXmxeCmQ
#https://www.google.com/search?q=micropython+keypad+keyboard+input&sca_esv=601135296&rlz=1C1FCXM_pt-PTPT1039PT1039&sxsrf=ACQVn0_lROLk6WnordGKv_kfUyfVGE9Jkg%3A1706122724602&ei=5F2xZbiWJNyI9u8P7Kq3qAU&udm=&oq=micropython+keypad+input&gs_lp=Egxnd3Mtd2l6LXNlcnAiGG1pY3JvcHl0aG9uIGtleXBhZCBpbnB1dCoCCAAyCBAhGKABGMMEMggQIRigARjDBEixN1CkC1iFGHACeAGQAQCYAdUCoAGxDKoBBTItNC4yuAEByAEA-AEBwgIKEAAYRxjWBBiwA8ICBhAAGAcYHsICCBAAGAgYBxgewgIKECEYChigARjDBOIDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp#fpstate=ive&vld=cid:ad1ca188,vid:7-PoXmxeCmQ,st:0
#https://www.instructables.com/Raspberry-Pi-Pico-and-4x3-Keypad/
#https://www.electrosoftcloud.com/en/multithreaded-script-on-raspberry-pi-pico-and-micropython/
#https://github.com/octopuslab-cz/micropython-keypad -------
#https://www.youtube.com/watch?v=aRQMDSmFGCo ------ com buffer
#https://github.com/brettmclean/pad4pi
#https://www.youtube.com/watch?v=lzv9cwdU_ok
#https://www.youtube.com/watch?v=7-PoXmxeCmQ
#https://www.youtube.com/watch?v=7-PoXmxeCmQ
#https://www.google.com/search?q=micropython+keypad+keyboard+input&sca_esv=601135296&rlz=1C1FCXM_pt-PTPT1039PT1039&sxsrf=ACQVn0_lROLk6WnordGKv_kfUyfVGE9Jkg%3A1706122724602&ei=5F2xZbiWJNyI9u8P7Kq3qAU&udm=&oq=micropython+keypad+input&gs_lp=Egxnd3Mtd2l6LXNlcnAiGG1pY3JvcHl0aG9uIGtleXBhZCBpbnB1dCoCCAAyCBAhGKABGMMEMggQIRigARjDBEixN1CkC1iFGHACeAGQAQCYAdUCoAGxDKoBBTItNC4yuAEByAEA-AEBwgIKEAAYRxjWBBiwA8ICBhAAGAcYHsICCBAAGAgYBxgewgIKECEYChigARjDBOIDBBgAIEGIBgGQBgg&sclient=gws-wiz-serp#fpstate=ive&vld=cid:ad1ca188,vid:7-PoXmxeCmQ,st:0
#https://www.youtube.com/watch?v=HKhY1qV8JbY ------------- timers
'''
Código de luzes: ver no scrip

'''
from ota import OTAUpdater
from machine import Pin, Timer, RTC
import machine
from secrets import SSID, PASSWORD
#from WIFI_CONFIG import SSID, PASSWORD
import utime
import time
import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import ubinascii
import sys
import _thread
#necessários para acertar a hora com o servidor NTP
import socket


import struct
import ujson

#import digitalmatrix

ledOnBoard = Pin("LED", Pin.OUT)
timer = Timer()
a=0
#flagUpdate para que o update seja feito apenas se a flag estiver disponivel
flagUpdate = 0
#horaUpdate para fazer o update apenas 1x por dia
horaUpdate = 18
#Flag para control da temperatura da Board
flagTemperatura = 0
#para obter a tempertura do sensor onboard
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
##########################################pin utilizado para abrir a porta########################
fechadura = Pin(1, Pin.OUT)
#iniciação da variavel para utilização na função abrePorta para verificar se o codigo está construido na totalidade
codigoCompleto = 1
#flag para impedir que a atualização seja interrompida pelo keypad
flagKeypad = 0
#Resposta esperada/autorizada pela API para abrir a porta
codigoAberturaPortaAPI=1000
#PIN para fazer o reset à board
desliga = Pin(0, Pin.OUT) #não usado, seria para fazer um reset remoto com um transistor
codigoPorta=''
MAX_COMPRIMENTO_CODIGO_ENTRADA = 8
# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
#path para atualizações no github
#firmware_url = "https://raw.githubusercontent.com/pauloaclara/testesOTA/main/"

User_Key = "null"

#ajuste das contas para a  hora
NTP_DELTA = 2208988800
#servidor a inquirir para a hora
host = "pool.ntp.org"
rtc=machine.RTC()

#mac do equipamento
mac = ubinascii.hexlify(wlan.config('mac'),':').decode()
#testa o MAC para ver se é a PIC de testes.
if(mac == "d8:3a:dd:66:37:a1"):
    print("o meu mac é igual ao teu, sou utilizado apenas para testes")
    firmware_url = "https://raw.githubusercontent.com/pauloaclara/testeOTA/main/"

#raiz da API
apiBaseRoot = 'https://pcpac.com/homes.pcpac.com/API102023/PHPREST/API/'


#setup the inputs and outputs according to the matrix keypad's wiring
R1 = machine.Pin(2,machine.Pin.OUT)
R2 = machine.Pin(3,machine.Pin.OUT)
R3 = machine.Pin(4,machine.Pin.OUT)
R4 = machine.Pin(5,machine.Pin.OUT)
C1 = machine.Pin(6,machine.Pin.IN,machine.Pin.PULL_DOWN)
C2 = machine.Pin(7,machine.Pin.IN,machine.Pin.PULL_DOWN)
C3 = machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_DOWN)
#C4 = machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_DOWN)

def Keyboard_Scanner():  #This function will handle the keyboard and run in its own thread.
    global User_Key
    Lock = "UNLOCKED"    #Variable Lock is used to compare against for action to occur
    
    while True:                 #loop forever
        Key_Pressed = "null"    #Set variable to 'null' at start of scan
        
        #Power each row one by one. While a row is powered, test the four columns
        #to see if any are "high", thus being pressed.  If a button is pressed
        #record that button value in variable Key_Pressed.
        R1.value(1)             #set power ON for row 1, off for the other three
        R2.value(0)
        R3.value(0)
        R4.value(0)    
        if C1.value() == True: Key_Pressed = 1 #check each button in column
        if C2.value() == True: Key_Pressed = 2
        if C3.value() == True: Key_Pressed = 3
#        if C4.value() == True: Key_Pressed = "A"
                  
        R1.value(0)             #set power ON for row 2, off for the other three
        R2.value(1)
        R3.value(0)
        R4.value(0)    
        if C1.value() == True: Key_Pressed = 4
        if C2.value() == True: Key_Pressed = 5
        if C3.value() == True: Key_Pressed = 6
#        if C4.value() == True: Key_Pressed = "B"
            
        R1.value(0)             #set power ON for row 3, off for the other three
        R2.value(0)
        R3.value(1)
        R4.value(0)    
        if C1.value() == True: Key_Pressed = 7
        if C2.value() == True: Key_Pressed = 8
        if C3.value() == True: Key_Pressed = 9
#        if C4.value() == True: Key_Pressed = "C"
            
        R1.value(0)             #set power ON for row 4, off for the other three
        R2.value(0)
        R3.value(0)
        R4.value(1)    
        if C1.value() == True: Key_Pressed = '*'
        if C2.value() == True: Key_Pressed = 0
        if C3.value() == True: Key_Pressed = '#'
#        if C4.value() == True: Key_Pressed = "D"
 
        # if lock was Locked, check to see if it can be unlocked
        # If we get through the keypad scan without seeing a Key_Press
        # value other than null, no key is pressed, so lets unlock the function.  
        if (Lock == "LOCKED") and (Key_Pressed == "null"):
            Lock = "UNLOCKED"
            
        # Key was pressed and because Lock wasn't locked, this is a new key press
        # Lock the routine from processing another keypress until
        # User_Key is processed in the main loop AND the the button was released
        # which prevents key repeating
        #
        if (Lock == "UNLOCKED") and (Key_Pressed != "null"):
            Lock = "LOCKED"
            User_Key = Key_Pressed
        
        utime.sleep(.02) #slow down the loop a bit as full speed isn't needed

'''
row_list = [2, 3, 4, 5]  
col_list = [6, 7, 8]

for x in range(0, 4):
  row_list[x] = Pin(row_list[x], Pin.OUT)
  row_list[x].value(1)

for x in range(0 ,3):
  col_list[x] = Pin(col_list[x], Pin.IN, Pin.PULL_UP)

key_list = [[1, 2, 3],\
      [4, 5, 6],\
      [7, 8, 9],\
      ['*', 0, '#']]

codigoPorta=str('')
MAX_COMPRIMENTO_CODIGO_ENTRADA = 8



def keypad(col, row):
  for r in row:
    r.value(0)
    result = [col[0].value(), col[1].value(), col[2].value()]
    if min(result) == 0:
      key = key_list[int(row.index(r))][int(result.index(0))]
      r.value(1)
      return (key)
    r.value(1)
'''  
def eliminaCodigoPorta():
    global codigoPorta
    codigoPorta=''
    return True
    
def souAsterisco(keyLida):
    
    if keyLida == "*":
        #print("estou no asterisco")
        #print(keylida)
        eliminaCodigoPorta()
        #print("sou um asterisco")
        #print(keyLida)
        return True
    
def souCardinal(keyLida):
    if keyLida == "#":
        #print("estou souCardinal")
        #print("sou um cardinal")
        
        #print(keyLida)
        #print("imprimi o cardinal?")
        return True
    
def souNumero(keyLida):
    #print("estouno souNumero\n")
    #print("recebi\n")
    #print(keyLida)
    if keyLida >= 0 and keyLida <= 9:
        #print("passei a condição, tenho o numero\n")
        #print(keyLida)
        #print("e o tipo: \n")
        #print(type(keyLida))
        
        keyLida = str(keyLida)
        #print("fiz a transformação para string \n")
        #print(keyLida)
        #print("passei o tipo (str): \n")
        #print(type(keyLida))
        #print(keyLida)
        constroiCodigoPorta(keyLida)
        #print("sou um numero")
        #print(keyLida)
        return True
    
def constroiCodigoPorta(keyLida):
    global codigoPorta
    #print("estou no codigo porta\n")
    #print("recebi: ")
    #print(type(keyLida))
    #print(keyLida)
    #print("codigo acutal da porta")
    #print(codigoPorta)
    #print("comprimento do codigo da porta")
    #print(len(codigoPorta))
    if len(codigoPorta)<=MAX_COMPRIMENTO_CODIGO_ENTRADA:
        #print("passei a condição de menor do que o maximo comprimento")
        #print("e tenho o codigo: ")
        #print(codigoPorta)
        codigoPorta = codigoPorta + keyLida
        #print("depois de acrescentado o ultimo passei a ter")
        #print(codigoPorta)
    else:
        #print("se entre aqui, entrei erradamente no else do constroiCodigoPorta")
        codigoPorta=''
    #print(codigoPorta)
    return True  
    
def validaKey(keyLida):
    #print("estou no validaKey\nrecebi: ")
    #print(keyLida)
    #print("sou do tipo")
    #print(type(keyLida))
    if isinstance(keyLida, str):
        #print("sou do tipo depois do isinstace")
        #print(type(keyLida))
    
        
        if souAsterisco(keyLida):
            #print("sou asterisco")
            return
        elif souCardinal(keyLida):
            #print("sou cardinal")
            return
    if isinstance(keyLida, int):
        #print("sou do tipo depois do isinstace no numero")
        #print(type(keyLida))
        #print("sou numero-----")
        #print(keyLida)
        souNumero(keyLida)
        return
    else:
        #print("Erro, sou desconhecido")
        return False
'''        
def leKey():
    global keyLida
    keyLida = keypad(col_list, row_list)
 #  validaKey(keyLida)
    if keyLida != None:
        #teste para a ligação do keypad
        print("*****")
        print(keyLida)
        ledOnBoardBlink(leKey) #nao retirado, d«a erro, para diminuir o delay na leitura das teclas
        validaKey(keyLida)
    #tempo para evitar que uma unica pressao seja lida 2 vezes seguidas    
    utime.sleep(0.15)
    return
'''
'''
if User_Key != "null":             #Check for value in User_Key and act on it 
            print(User_Key)
            #Key_Code = User_Key            #Copy User_Key to  a variable used within main loop
            User_Key = "null"              #Reset User_Key to null so it can be written to again
            print("Key Code =",Key_Code)
        
    utime.sleep(.1)  # A sleep just to slow things down to mimic work being performed
'''    #here in the main loop is where all the normal processing happens
def leKey():#nova
    global keyLida
    global User_Key
    global Key_Code
    #print("estou na função")
    #global User_Key
    #global codigoPorta
    #codigoCompleto = 1
    if User_Key != "null":             #Check for value in User_Key and act on it 
            #print(User_Key)
            Key_Code = User_Key            #Copy User_Key to  a variable used within main loop
            keyLida = Key_Code
            User_Key = "null"              #Reset User_Key to null so it can be written to again
            #print("Key Code =",Key_Code)
            #validaKey(Key_Code)
            #print("*****")
            #print(keyLida)
            ledOnBoardBlink(leKey) #nao retirado, d«a erro, para diminuir o delay na leitura das teclas
                                    #no ultimos testes efetuados na board de testes, depois de retirado não dei erro.
            validaKey(keyLida)
        
    utime.sleep(.1)  # A sleep just to slow things down to mimic work being performed
    #here in the main loop is where all the normal processing happens
    return



def validaResposta(resposta):
    #ver codigo de erro na API do servidor
    if resposta == codigoAberturaPortaAPI:
        return True
    

def constroiURL(stringCodigoLidoDoKeyboard):
    #controi o URL para enviar o MAC e o codigo e compara o valor de retorno de acordo com a resposta esperada de acordo com o ficheiro de erros na API do servidor
    #apiBaseRoot = 'https://pcpac.com/homes.pcpac.com/API102023/PHPREST/API/authDevices/getAuth.php?MAC='
    endPoint = 'authDevices/getAuth.php?'
    stringMAC = 'MAC=' 
    StringComMac = mac
    #StringComMac = 'd8:3a:dd:66:37:a1'
    stringCodigo = '&code='
    #stringCodigoLidoDoKeyboard = '22222222'
    stringTemp = '&temp='
    #tambem envia a temperatura
    stringTotal = apiBaseRoot + endPoint + stringMAC + StringComMac + stringCodigo + stringCodigoLidoDoKeyboard+stringTemp+str(temperatura())
    r = urequests.get(stringTotal)
    #print(stringTotal)
    #print(r.content)
    #print(r)
    try:
        if r.json != '':
            resposta = r.json()
            #print(resposta)
            
            if (resposta==codigoAberturaPortaAPI):
                #print(r)
                print(r.json())
                r.close()
                return True
            #else:
            #    print(r)
            #print(r.json())
             #   return False
    except:
        return False
        #pass
                
    return False
    
    


def abreAFechadura():
    fechadura.value(True)#abre a fechadura
    time.sleep(0.5)
    fechadura.value(False)#fecha a fechadura
    ledOnBoardBlink(abreAFechadura)
    
    return True
    
# ver nova fucção abre porta    
def abrePorta():
    global codigoPorta
    codigoCompleto = 1
    #len(leKey())
    leKey()
    if len(codigoPorta)>=MAX_COMPRIMENTO_CODIGO_ENTRADA:
        #print("tenho 8")
        ledOnBoardBlink(codigoCompleto) #comentado para reduzir o delay da pergunta/resposta ao servidor
        #print(codigoPorta)
        
        if constroiURL(codigoPorta):#constroi o URL, compara o valor recebido, retorna boolean
            abreAFechadura()
            #print("não abri a porta")
            #limpa o codigo utilizado
            codigoPorta=''
            
        #limpa o codigo utilizado
        codigoPorta=''       
        return

'''
def abrePorta():
    #print("estou na função")
    global User_Key
    global codigoPorta
    codigoCompleto = 1
    if User_Key != "null":             #Check for value in User_Key and act on it 
            print(User_Key)
            #Key_Code = User_Key            #Copy User_Key to  a variable used within main loop
            User_Key = "null"              #Reset User_Key to null so it can be written to again
            print("Key Code =",Key_Code)
        
    utime.sleep(.1)  # A sleep just to slow things down to mimic work being performed
    #here in the main loop is where all the normal processing happens
    
'''
def ledOnBoardBlink(funcao):
    if funcao == abreAFechadura:
        ledOnBoard.on()
        time.sleep(1)
        ledOnBoard.off()
    if funcao == connect:
        ledOnBoard.on()
        time.sleep(0.5)
        ledOnBoard.off()
    if funcao == leKey:
        ledOnBoard.on()
        time.sleep(0.1)
        ledOnBoard.off() 
    if funcao == codigoCompleto:
        for i in range(3):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    if funcao == 1111:
        for i in range(10):
            ledOnBoard.on()
            time.sleep(0.1)
            ledOnBoard.off()
            time.sleep(0.1)
    if funcao == set_time:
        for i in range(5):
            ledOnBoard.on()
            time.sleep(0.5)
            ledOnBoard.off()
            time.sleep(0.1)
    
  
#definição da função da hora
def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
 
 
def temperatura():
    #Temperatura em Celsius
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    return temperature

def enviaTemperatura():
    #https://forums.raspberrypi.com/viewtopic.php?t=351475
    #Envia a temperatura a cada 10 minutos
    global flagTemperatura
    Payload=''
    endPoint = 'logs/logDiversos.php'
    timestamp=rtc.datetime()
    timestring="%02d"%(timestamp[5])
    #print("minuto"+timestring)
    #print("\ntipo: ")
    #print(type(timestring))
    if (timestring == '00' or timestring == '10' or timestring == '20' or timestring == '30' or timestring == '40' or timestring == '50') and flagTemperatura == 0:
        flagTemperatura = 1
        #print("estou para enviar")
        #print(flagTemperatura)
        url = apiBaseRoot + endPoint
        headers = { "Content-Type": "application/json" }
        Payload= {"MAC": mac, "temperature": temperatura()}  
        #print(Payload)
        insertPayload = ujson.dumps(Payload)
        #print("sending...temperatura")
        start_time = time.ticks_ms()
        response = urequests.post(url, headers=headers, data =insertPayload)       
        return temperatura()
    if (timestring == '01' or timestring == '11' or timestring == '21' or timestring == '31' or timestring == '41' or timestring == '51') and flagTemperatura == 1:
        flagTemperatura = 0
        #print("flagTemperatura = 0")
        return
    
    
#definição da ligação à rede    
def connect():
    #Connect to WLAN
    global a
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    try:
        wlan.connect(SSID, PASSWORD)
    except:
        print('Username or password not set')
        return
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        ledOnBoardBlink(connect)
        time.sleep(0.5)
        a+=1
        print (a)
        if a == 5:
            a=0
            wlan.active(False)
            time.sleep(3)
            wlan.active(True)
            wlan.connect(SSID, PASSWORD)
    ip = wlan.ifconfig()[0]
    """print(wlan.ifconfig())"""
    print(f'Connected on {ip}')    
    return ip

def fazUpdate():
    global flagUpdate
    global flagKeypad
    flagKeypad = 1
    timestamp=rtc.datetime()
    timestring="%02d"%(timestamp[5])
    #print("minuto"+timestring)
    #print("\ntipo: ")
    #print(type(timestring))
    #if (timestring == str(horaUpdate) or timestring == str(horaUpdate+2) or timestring == str(horaUpdate+4) or timestring == str(horaUpdate+6) or timestring == str(horaUpdate+8) or timestring == str(horaUpdate+10) or timestring == str(horaUpdate+12) or timestring == str(horaUpdate+14) or timestring == str(horaUpdate+18) or timestring == str(horaUpdate+20) or timestring == str(horaUpdate+22)) and flagUpdate == 0:
    #flagUpdate = 1
    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main1.py")
    #print(ota_updater)
    #print("+++++++++++++++")
    #ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "novo")
    #ota_updater.download_and_install_update_if_available()
    ota_updater.download_and_install_update_if_available()
    flagKeypad = 0
        
    #if (timestring == str(horaUpdate+1) or timestring == str(horaUpdate+3) or timestring == str(horaUpdate+5) or timestring == str(horaUpdate+7) or timestring == str(horaUpdate+9) or timestring == str(horaUpdate+11) or timestring == str(horaUpdate+13) or timestring == str(horaUpdate+15) or timestring == str(horaUpdate+17) or timestring == str(horaUpdate+19) or timestring == str(horaUpdate+21) or timestring == str(horaUpdate+23)) and flagUpdate == 1:
    #flagUpdate = 0
    #print("flagTemperatura = 0")
        
    flagKeypad = 0

       


#estabelece a ligação à rede wifi e não avança se não conseguir
ip = connect()



try:
    #para aplicar a hora obtida do servidor NTP ao raspberry
    set_time()
    #Teste para ver a hora obtida
    print(time.localtime())
    ledOnBoardBlink(set_time)
except:
    print("Erro ao acertar a data")
    #Teste para ver a hora obtida
    #print(time.localtime())
    ledOnBoardBlink(1111)
    
    #ntptime.settime()

#teste para ver o MAC
print('MAC: '+mac)
print('***********************************************')
print('\nCódigo de luzes:\nLed on board:')
print('\n\tQuando arranca e até obter ligação wifi,\nPisca a cada segundo, até 5 segundos')
print('\n\tReinicia a ligação e permanece infinito até ter ligação')
print('\n\tQuando obtem ligação o led on board fica apagado')
print('\n\tquando acerta a hora faz 5x 0.5 segundos de luz e 0.1 apagado')
print('\n\tse tiver erro a acertar a hora 10x 0.1 de luz com 0.1 apagado')
#print('\n\n\tQuando lê uma tecla do keypad, pisca 1x 0.3 segundos')
#print('\n\tQuando controi o código a envia, pisca 3x com espaço de 0.1 segundos')
#print('\n\tSe receber uma resposta autorizada da API, abre a fechadura com o led a acender por 0.5 segundos')
print('\n*****************************************************************')
print('\n\t\t\t\tSYSTEM READY')
print('\n*****************************************************************')
#Chama a função em segundo thread
#_thread.start_new_thread(fazUpdate, ())


_thread.start_new_thread(Keyboard_Scanner,())  #This starts the thread running 

'''
#Main Loop to do all the other work needed
while True:
    if User_Key != "null":             #Check for value in User_Key and act on it 
        Key_Code = User_Key            #Copy User_Key to  a variable used within main loop
        User_Key = "null"              #Reset User_Key to null so it can be written to again
        print("Key Code =",Key_Code)
    
    utime.sleep(.1)  # A sleep just to slow things down to mimic work being performed
    #here in the main loop is where all the normal processing happens


''' #após a nova inclusão da "biblioteca" keypad + thread
while True:
    if wlan.isconnected():
        try:
            enviaTemperatura()
        #print("envia 1")
        except:
            eliminaCodigoPorta()
        #try:
            #fazUpdate()
        #except:
            #pass
    
        if flagKeypad == 0:
            try:
                abrePorta()
            except KeyboardInterrupt as theInterrupt:
                print('interrupt')
                #exit(0)
                sys.exit(0) #para sair do programa quando em Thony
            except:
                pass
    else:
        print("estou desligado do wifi")
        ip = connect()
        

