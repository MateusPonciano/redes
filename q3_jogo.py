import json
import socket

class Game():
    def __init__(self):
        self.board = [
        [['1', '_'], ['2', '_'], ['3', '_']],
        [['4', '_'], ['5', '_'], ['6', '_']],
        [['7', '_'], ['8', '_'], ['9', '_']],
        ]

        self.jogador = 'X'

        self.jogadas_disponiveis = 9

        self.jogadas1 = [] #lista de jogadas X
        self.jogadas2 = [] #lista de jogadas 0

    #mostra o jogo
    def showBoard(self):
        print('\n')
        for linha in self.board:
            #o número da posição não é mostrado
            print(' ', linha[0][1], '|', linha[1][1], '|', linha[2][1])
            if not linha == self.board[2]:
                print ('-------------')
        print ('\n')

    #faz a jogada
    def jogada(self, posicao):
        success = False

        for linha in self.board:
            for position in linha:
                if position[0] == posicao:
                    #verifica se a posição já está ocupada
                    if position[1] == '_':
                        #o _ é substituido por X ou 0
                        position[1] = self.jogador
                        #uma jogada a menos
                        self.jogadas_disponiveis -= 1
                        success = True #jogada realizada
                        break

                    else:
                        break

                else: continue
        return success

    #verifica se algum jogador ganhou
    def ganhar(self, jogador):
        ganhou = False

        #todas as possibilidades
        ganho = [
          ['1', '2', '3'],
          ['4', '5', '6'],
          ['7', '8', '9'],
          ['1', '4', '7'],
          ['2', '5', '8'],
          ['3', '6', '9'],
          ['3', '5', '7'],
          ['1', '5', '9']
        ]

        #verifica se alguma das possibilidades está na lista de jogadas
        #de um dos jogadores
        if jogador == 'X':
            for possib in ganho:
                if (possib[0] in self.jogadas1) and (possib[1] in self.jogadas1) and (possib[2] in self.jogadas1):
                    ganhou = True

        else:
            for possib in ganho:
                if (possib[0] in self.jogadas2) and (possib[1] in self.jogadas2) and (possib[2] in self.jogadas2):
                    ganhou = True

        return ganhou

#os 2 jogadores irão rodar as classes de cliente e servidor

#classe que enviará as mensagens para o outro peer
class Game_client():
    def __init__(self):
        #socket UDP
        self.host = '127.0.0.1'
        self.port = 0
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (self.host, self.port)

    def send_msg(self, msg):
        #envia mensagem para outro peer
        self.dest = (self.host, self.port)
        self.udp.sendto (msg.encode('utf-8'), self.dest)

    def close_connection(self):
        self.udp.close()

#classe que receberá mensagens do outro peer
class Game_server():
    def __init__(self):
        #socket UDP
        self.host = ''
        self.port = 1
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.orig = (self.host, self.port)

    def listen(self):
        #recebe mensagem do outro peer
        self.orig = (self.host, self.port)
        while True:
            msg, cliente = self.udp.recvfrom(1024)
            if msg: break

        return msg.decode('utf-8')

    def close_connection(self):
        self.udp.close()

#classe que fará conexão com o servidor
#antes de conectar-se com outro jogador
class Connection():
    def __init__(self):
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = '127.0.0.1'
        self.port = 6007

    #envia mensagem 'Hello' para o servidor
    def __send_hello(self):
        msg = 'Hello'
        dest = (self.host, self.port)
        self.udp.sendto(msg.encode('utf-8'), dest)
        #essa mensagem é enviada para o servidor
        #conhecer o ip e número de porta de cada peer

    def get_peer(self):
        resp = ''
        print ('waiting for connection...')
        self.__send_hello() #envia 'Hello'
        #espera resposta do servidor com informação
        #para conectar-se ao outro peer
        while True:
            resp, server = self.udp.recvfrom(1024)
            print (resp.decode('utf-8'))
            if resp.decode('utf-8').startswith('{'):
                break

        peer = resp.decode('utf-8')
        jpeer = json.loads(peer) #carrega resposta em json

        return jpeer
