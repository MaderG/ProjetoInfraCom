from socket import *
from datetime import datetime
import time
import os
import random
import sys
#Cliente UDP




clientHost = 'localhost'  # Endereco IP do Servidor
clientPort = 5000            # Porta que o Servidor esta
dest = (clientHost, clientPort)
buffer_size = 1024


msg = ''

clientSocket = socket(AF_INET, SOCK_DGRAM)

print('Para sair escreva SAIR\n')

hora = datetime.now().strftime('%H:%M')
appMsg = f"{hora} CINtofome: Bem vindo ao CINtofome!\n"

while msg != 'SAIR':
    print(appMsg)

    msg = input()

    inicio = time.time()

    isFile = os.path.exists(msg)
    if isFile == True:
        f = open(msg, 'r')
        data = f.read()
        hora = datetime.now().strftime('%H:%M')
        print(f'{hora} cliente: {data}')

    else:
        hora = datetime.now().strftime('%H:%M')
        print(f'{hora} cliente: {msg}')



    srvMsg, serverAddr = clientSocket.recvfrom(buffer_size)  # recebe a resposta do servidor

    srvMsg = srvMsg.decode()

    hora = datetime.now().strftime('%H:%M')
    appMsg = f'{hora} CINtofome: {srvMsg}' #printa a mensagem do servidor na tela

    if msg == "SAIR":
        print(appMsg)

        clientSocket.close()
        break



