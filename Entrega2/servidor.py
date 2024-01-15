from socket import *
import random

#Na primeira entrega diz que o arquivo precisa ser armazenado no servidor, entao:

clientStorage = [] #armazena a mensagem que o cliente enviou
serverStorage = [] #armazena a mensagem que o servidor enviou


serverHost = 'localhost'
serverPort = 5000
orig = (serverHost, serverPort)
buffer_size = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(orig)

while True:

    msg, clientAddr = serverSocket.recvfrom(buffer_size) #recebe a mensagem do cliente
    msg = msg.decode()
    clientStorage.append(msg)

    if msg == 'SAIR':
        srvMsg = f'ACK da mensagem {msg}\nObrigado e volte sempre!\n'

        serverSocket.sendto(srvMsg.encode(), clientAddr) #envia a mensagem para o cliente
        serverStorage.append(srvMsg)

    else:
        srvMsg = f'ACK da mensagem {msg}'
        if random.random() > 0.2:
            serverSocket.sendto(srvMsg.encode(), clientAddr)
            serverStorage.append(srvMsg)



serverSocket.close()

