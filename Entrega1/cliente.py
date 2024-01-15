from socket import *
from datetime import datetime
from time import sleep
import os
#Cliente UDP

clientHost = 'localhost'  # Endereco IP do Servidor
clientPort = 5000            # Porta que o Servidor esta
dest = (clientHost, clientPort)
buffer_size = 1024

clientSocket = socket(AF_INET, SOCK_DGRAM)

print('Para sair escreva SAIR\n')

hora = datetime.now().strftime('%H:%M')
appMsg = f"{hora} CINtofome: Bem vindo ao CINtofome!\n"


while True:
    msg = input(appMsg)
    isFile = os.path.exists(msg)
    if isFile == True:
        f = open(msg, 'r')
        data = f.read()
        hora = datetime.now().strftime('%H:%M')
        print(f'{hora} cliente: {data}')

    else:
        hora = datetime.now().strftime('%H:%M')
        print(f'{hora} cliente: {msg}')

    if msg == 'SAIR':
        hora = datetime.now().strftime('%H:%M')
        print(f"{hora} CINtofome: Obrigado e volte sempre!")
        clientSocket.close()
        break

    clientSocket.sendto(msg.encode(), dest)  #envia a mensagem para o servidor

    srvMsg, serverAddr = clientSocket.recvfrom(buffer_size)  # recebe a resposta do servidor
    srvMsg = srvMsg.decode()

    hora = datetime.now().strftime('%H:%M')
    appMsg = f'{hora} CINtofome: {srvMsg}' #printa a mensagem do servidor na tela









