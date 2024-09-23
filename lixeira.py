import serial
import time
from pymata4 import pymata4

triggerPin = 12  
echoPin = 11  
tempo_padrao = 20   # segundos
tempo_envio = tempo_padrao + 1  


mySerial = serial.Serial('COM_PORT', 9600)

board = pymata4.Pymata4()

def medir_distancia():
     while (True) :
         
            time.sleep(1)
            board.sonar_read(triggerPin)
     

while True:
    # Leitura do nivel da lixeira
    medida_centimetro = medir_distancia()
    print(f"Distancia em cm: {medida_centimetro}")

    # Calculo do nivel da lixeira
    NIVEL_LIXEIRA = int(map(medida_centimetro, 0, 63, 100, 0))  # Implementar a função map em Python

    print(f"NIVEL: {NIVEL_LIXEIRA}")

    # Verifica se é hora de enviar os dados
    if (time.time() - tempo_ultimo_envio) >= tempo_padrao:
        mySerial.write(b'AT+CWMODE=3\r\n')
        time.sleep(2)
        
        mySerial.write(b'AT+CWJAP="ClaroNetWifi","Elmararo10"\r\n')
        time.sleep(5)
        
        mySerial.write(b'AT+CIPMUX=1\r\n')
        time.sleep(2)
        
        mySerial.write(b'AT+CIPSTART=4,"TCP","184.106.153.149",80\r\n')
        time.sleep(2)

        # Envio dos dados
        mySerial.write(b'AT+CIPSEND=4,44\r\n')
        time.sleep(2)

        mySerial.write(f'GET /update?key=F1L7LDCZCMWZC4IZ&field1={NIVEL_LIXEIRA}\r\n'.encode())
        
        tempo_ultimo_envio = time.time()  # atualiza o tempo do último envio

    time.sleep(1)  
