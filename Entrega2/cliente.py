from socket import *
from datetime import datetime
import time
import os
import random
import sys
#Cliente UDP


#a probabilidade que colocamos para a perda de pacotes foi de 20% para ter mais chance de ocorrer durante os testes





clientHost = 'localhost'  # Endereco IP do Servidor
clientPort = 5000            # Porta que o Servidor esta
dest = (clientHost, clientPort)
buffer_size = 1024


msg = ''
demorou = False
pne = False

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)

print('Para sair escreva SAIR\n')

hora = datetime.now().strftime('%H:%M')
appMsg = f"{hora} CINtofome: Bem vindo ao CINtofome!\n"

while msg != 'SAIR':
    try:
        print(appMsg)
        if appMsg != f"{hora} CINtofome: Bem vindo ao CINtofome!\n":
            print(f"a resposta demorou {duracao} segundos para chegar\n")
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

            
        #----------randomizando a perda de pacote-------------
        if random.random() > 0.2: 
            clientSocket.sendto(msg.encode(), dest)  #envia a mensagem para o servidor
            pne = False
        else:
            print("----Pacote não enviado----")
            pne = True
        #----------randomizando a perda de pacote-------------

        srvMsg, serverAddr = clientSocket.recvfrom(buffer_size)  # recebe a resposta do servidor
        demorou = False
        fim = time.time()

        duracao = fim - inicio
        
        srvMsg = srvMsg.decode()

        hora = datetime.now().strftime('%H:%M')
        appMsg = f'{hora} CINtofome: {srvMsg}' #printa a mensagem do servidor na tela

        if msg == "SAIR":
            print(appMsg)
            print(f"a resposta demorou {duracao} segundos para chegar")
            clientSocket.close()
            break
    except:
        demorou = True

        if pne == False: #se o pacote foi enviado o erro foi no ack
            print('----ACK não recebido----')

        print('O tempo limite foi atingido. Aguarde um pouco que vamos tentar novamente')
        appMsg = 'Tentando novamente'
        
        

        while demorou == True:
            try:#-----------------------TENTANDO NOVAMENTE ENVIAR------------------------

                
            
                isFile = os.path.exists(msg)
                if isFile == True:
                    f = open(msg, 'r')
                    data = f.read()
                

                #----------randomizando a perda de pacote-------------
                if random.random() > 0.2: 
                    clientSocket.sendto(msg.encode(), dest)  #envia a mensagem para o servidor
                    pne = False
                else:
                    print("----Pacote não enviado----")
                    pne = True
                #----------randomizando a perda de pacote-------------

                srvMsg, serverAddr = clientSocket.recvfrom(buffer_size)  # recebe a resposta do servidor
                demorou = False
                fim = time.time()

                duracao = fim - inicio
                
                srvMsg = srvMsg.decode()

                hora = datetime.now().strftime('%H:%M')
                appMsg = f'{hora} CINtofome: {srvMsg}' #printa a mensagem do servidor na tela

                if msg == "SAIR":
                    print(appMsg)
                    print(f"a resposta demorou {duracao} segundos para chegar")
                    clientSocket.close()
                    break
                    
                #-----------------------TENTANDO NOVAMENTE ENVIAR------------------------
                
            except:
                time.sleep(1)
                if pne == False:  #se o pacote foi enviado o erro foi no ack
                    print('----ACK não recebido----')

                print("Tentando enviar novamente")
        






