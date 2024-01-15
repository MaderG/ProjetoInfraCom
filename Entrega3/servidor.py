from socket import *
import random


global clientAddr


def receber_msg():
    msg, clientAddr = serverSocket.recvfrom(buffer_size) #recebe a mensagem do cliente
    msg = msg.decode()
    clientStorage.append(msg)

    return msg


def mandar_msg(resposta):
    srvMsg = resposta
    serverSocket.sendto(srvMsg.encode(), clientAddr) #envia a mensagem para o cliente
    serverStorage.append(srvMsg)

#Estados do cliente
   # 1 - Esperando o numero da mesa
   # 2 - Esperando o nome
   # 3 - Pronto para pedir
   # 4 - Esperando o pedido
   # 5 - Esperando o pagamento


clientes = {}
mesas = {}

opcoes = ("Escolha uma das opções:\n" +
            "|1 - cardapio\n" +
            "|2 - pedir\n" +
            "|3 - conta individual\n" +
            "|4 - não fecho com robô, chame seu gerente\n" +
            "|5 - nada não, tava só testando\n" +
            "|6 - conta da mesa:\n" +
            "|7 - pagar\n" +
            "|8 - levantar\n:")

cardapioPrint = ("\tCardapio:\n" +
                "\t1 - Bife a cavalo: 55.00\n" +
                "\t2 - Parmegiana: 20.00\n" + opcoes)

cardapio ={
    "Frango frito": 15.00,
    "Parmegiana": 20.00,
    "1": "Frango frito",
    "2": "Parmegiana"
}



clientStorage = [] #armazena a mensagem que o cliente enviou
serverStorage = [] #armazena a mensagem que o servidor enviou


serverHost = 'localhost'
serverPort = 5000
orig = (serverHost, serverPort)
buffer_size = 1024

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(orig)

while True:

    msg = receber_msg()

    if msg == 'chefia':

        ip, port = clientAddr

        id = f"{ip}:{port}" # dados mais importantes do cliente

        if not (id in clientes): #se não houver, cadastrar um novo

            clientes[id] = {"mesa": '',
                    "nome": '',
                    "contaIndividual": 0,
                    "pedidos": [],
                    "estado": 1}

            mandar_msg("Digite sua mesa")

    else:
        ip, port = clientAddr
        id = f"{ip}:{port}"

        if not (id in clientes):
            mandar_msg("Envie a palavra 'chefia' para ser cadastrado")

        else:
            clienteAtual = clientes[id] # pega os dados do cliente que mandou a msg

            #Estado 1: receber o n da cadeira

            if clienteAtual["estado"] == 1:
                mesa = msg
                clienteAtual["mesa"] = mesa
                clienteAtual["estado"] = 2  #pega o número da mesa e atualiza para o segundo estado para pegar o nome

                clientes[id] = clienteAtual

                if not (mesa in mesas):
                    # se não existe a mesa, cria uma
                    mesas[mesa] = {"pedidos": [],
                                   "conta": 0,
                                   "clientes": [id]}

                else:
                    #se ja existe a mesa, adiciona um novo cliente à ela
                    mesas[mesa]["clientes"].append(id)
                mandar_msg("Digite seu nome")

            #Estado 2: recebimento do nome

            elif clienteAtual["estado"] == 2:
                clienteAtual["nome"] = msg
                clienteAtual["estado"] = 3
                clientes[id] = clienteAtual
                mandar_msg(opcoes)

            #Estado 3: cliente pronto, podendo fazer varios pedidos
            elif (clienteAtual["estado"] == 3):
                # Pedido do cardapio
                if (msg == "1" or msg == "1 - cardapio" or msg == "cardapio"):
                    mandar_msg(cardapioPrint)

                # Pedir algo
                elif (msg == "2" or msg == "2 - pedir" or msg == "pedir"):
                    clienteAtual["estado"] = 4
                    clientes[id] = clienteAtual
                    mandar_msg("Informe o numero ou nome do prato (0 - voltar para opcoes): ")

                # Pedir conta individual
                elif (msg == "3" or msg == "3 - conta individual" or msg == "conta individual"):
                    valorIndividual = clienteAtual["contaIndividual"]
                    mandar_msg(f"O valor da sua conta atual é: {valorIndividual}\n{opcoes}")

                elif (msg == "4" or msg == "4 - não fecho com robô, chame seu gerente" or msg == "não fecho com robô, chame seu gerente"):
                    mandar_msg("Como é amigo?")

                elif (msg == "5" or msg == "5 - nada não, tava só testando" or msg == "nada não, tava só testando"):
                    mandar_msg("Tudo bem")

                # Pedir a conta da mesa
                elif (msg == "6" or msg == "6 - conta da mesa" or msg == "conta da mesa"):
                    contaMesa = ""
                    mesaAtual = mesas[clienteAtual["mesa"]]
                    #Coletando as informações para enviar na mensagem
                    for clienteID in mesaAtual["clientes"]:
                        cliente = clientes[clienteID]
                        clienteNome = cliente["nome"]
                        clienteContaInd = cliente["contaIndividual"]
                        contaMesa += f"\n|\t{clienteNome}\t|\n"
                        for pedido in cliente["pedidos"]:
                            pedidoNome, pedidoPreco = pedido
                            contaMesa += f"{pedidoNome} => {pedidoPreco}\n"
                        contaMesa += f"Total - {clienteContaI}\n----------------------\n"

                    totalMesa = mesaAtual["conta"]
                    contaMesa += f"Total da mesa - {totalMesa}\n----------------------\n"
                    mandar_msg(f"{msgCM}\n{opcoes}")

                #Pagamento

                #Nesse caso, o estado do cliente poderá ir para o estado n 5
                elif (pkt["msg"] == "7" or pkt["msg"] == "7 - pagar" or pkt["msg"] == "pagar"):
                    clienteAtual["estado"] = 5
                    e[id] = clienteAtual
                    valorIndividual = clienteAtual["contaIndividual"]
                    mandar_msg(f"Sua conta foi: {valorIndividual}\nQuanto deseja pagar? (0 -caso queira voltar)")

                #Levantar
                elif (msg == "8" or msg == "8 - levantar" or msg == "levantar"):
                    # ve se o cliente ja pagou a conta
                    if (clienteAtual["contaIndividual"] == 0):
                        mesaAtual = mesas[clienteAtual["mesa"]]
                        mesaAtual["clientes"].remove(id)
                        if (len(mesaAtual["clientes"]) == 0):
                            del mesas[clienteAtual["mesa"]]
                        del clientes[id]
                        enviar_msg("Tchau!", nextAck)
                    else:
                        mandar_msg(f"Você ainda não pagou sua conta!\n{opcoes}")

                #Estado 4: esperando pedido
                elif (clienteAtual["estado"] == 4):
                    #Se a mensagem for 0, o cliente retorna ao estado 3
                    if (msg == "0"):
                        clienteAtual["estado"] = 3
                        clientes[id] = clienteAtual
                        mandar_msg(opcoes)
                    #Verifica se o que foi pedido está no cardápio
                    elif not (msg in cardapio):
                        mandar_msg("Código não reconhecido. Insira novamente: ")
                    #Registra o pedido na conta do cliente e na mesa dele
                    else:
                        pedido = msg
                        if pedido.isnumeric():
                            pedido = cardapio[pedido]
                            # nome       preço
                        clienteAtual["pedidos"].append((pedido, cardapio[pedido]))
                        clienteAtual["contaIndividual"] += cardapio[pedido]
                        clienteAtual["estado"] = 3
                        clientes[id] = currentClient

                        mesaAtual = mesas[clienteAtual["mesa"]]
                        mesaAtual["pedidos"].append((pedido, cardapio[pedido]))
                        mesaAtual["conta"] += cardapio[keyPedido]
                        mesas[clienteAtual["mesa"]] = currentMesa
                        mandar_msg(f"Pedido confirmado!!\n {opcoes}")

                #Estado: Esperando pagamento
                elif (clienteAtual["estado"] == 5):
                    valor = msg
                    #verifica se o que foi enviado pelo cliente é numérico
                    if not (valor.isnumeric()):
                        mandar_msg(f"Insira um valor numérico: ")
                    #verifica se o valor está de acordo com a conta e tira a diferenca
                    else:
                        valor = float(valor)
                        print(valor < clienteAtual["contaIndividual"])
                        if (valor == 0):
                            clienteAtual["estado"] = 3
                            clientes[id] = currentClient
                            mandar_msg(f"{opcoes}")

                        elif (valor < clienteAtual["contaIndividual"]):
                            mandar_msg(f"Valor inferior ao da conta! Insira novo valor: ")
                        elif (valor > clienteAtual["contaIndividual"]):
                            diferenca = valor - clienteAtual["contaIndividual"]
                            clienteAtual["contaIndividual"] = 0
                            clienteAtual["estado"] = 3
                            clientes[id] = clienteAtual
                            mandar_msg(f"Você está pagando {diferenca} a mais que sua conta. O restante será descontado da conta da mesa!\n{opcoes}")
                        else:
                            clienteAtual["contaIndividual"] = 0
                            clienteAtual["estado"] = 3
                            clientes[id] = currentClient
                            mandar_msg(f"Valor recebido!\n{opcoes}")

                        mesaAtual = mesas[clienteAtual["mesa"]]
                        mesaAtual["conta"] -= valor
                        if mesaAtual["conta"] < 0:
                            mesaAtual["conta"] = 0
                        mesas[clienteAtual["mesa"]] = mesaAtual



