import socket
from q3_jogo import Game, Game_client, Game_server, Connection

posicoes = '''

      1 | 2 | 3
    -------------
      4 | 5 | 6
    -------------
      7 | 8 | 9

'''

#verifica se a posição é válida
def valida(posicao):
    validade = False
    if posicao.isdigit(): #verifica sé é um número
        if 0 < int(posicao) < 10: #verifica se está entre 1 - 9
            validade = True

    return validade

#jogo do jogador X
def do_jogo_X(game, cliente, servidor):
    while True:
        if game.jogador == 'X':
            if game.jogadas_disponiveis > 0:
                if game.jogadas_disponiveis == 9:
                    game.showBoard()
                    position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")

                    #verifica se a posição é válida ou se já está ocupada
                    while not valida(position):
                        position = input("Posição Inválida ")
                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada ")

                    #adiciona a jogada na lista de jogadas de X
                    game.jogadas1.append(position)
                    #envia mensagem com a posição jogada para o outro peer
                    cliente.send_msg(position)
                    game.showBoard()
                    #verifica se o jogador X ganhou
                    if game.ganhar(game.jogador):
                        game.showBoard()
                        print ('Jogador X ganhou')
                        break

                else:
                    #na segunda jogada escuta o socket do outro peer (bind)
                    if game.jogadas_disponiveis == 8:
                        servidor.orig = (servidor.host, servidor.port)
                        servidor.udp.bind(servidor.orig)

                    #recebe posição do outro peer
                    position_ant = servidor.listen()
                    game.jogador = '0'
                    game.jogada(position_ant)
                    #atualiza o jogo com a jogada do outro peer
                    game.jogadas2.append(position_ant)
                    #adiciona a jogada na lista de jogadas de 0

                    #verifica se o jogador 0 ganhou
                    if game.ganhar(game.jogador):
                        game.showBoard()
                        print ('Jogador 0 ganhou')
                        break

                    game.jogador = 'X'

                    game.showBoard()
                    position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")
                    #verifica se a posição é válida ou se já está ocupada
                    while not valida(position):
                        position = input("Posição Inválida ")

                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada ")

                    #adiciona a jogada na lista de jogadas de X
                    game.jogadas1.append(position)
                    #envia mensagem com a posição jogada para o outro peer
                    cliente.send_msg(position)
                    game.showBoard()
                    #verifica se o jogador X ganhou
                    if game.ganhar(game.jogador):
                        print ('Jogador X ganhou')
                        break

                    #verifica se acabaram as jogadas
                    if game.jogadas_disponiveis  == 0:
                        print("Deu velha")
                        break

#jogo do jogador 0
def do_jogo_0(game, cliente, servidor):
    while True:
        if game.jogador == '0':
            if game.jogadas_disponiveis > 0:
                if game.jogador == '0':
                    if game.jogadas_disponiveis == 9:
                        #na primeira jogada escuta o socket do outro peer (bind)
                        servidor.orig = (servidor.host, servidor.port)
                        servidor.udp.bind(servidor.orig)

                    position_ant = servidor.listen()
                    #recebe posição do outro peer
                    game.jogador = 'X'
                    game.jogada(position_ant)
                    #atualiza o jogo com a jogada do outro peer
                    game.jogadas1.append(position_ant)
                    #adiciona a jogada na lista de jogadas de X

                    #verifica se o jogador X ganhou
                    if game.ganhar(game.jogador):
                        game.showBoard()
                        print ('Jogador X ganhou')
                        break

                    game.jogador = '0'
                    game.showBoard()

                    #verifica se acabaram as jogadas
                    if game.jogadas_disponiveis  == 0:
                        print("Deu velha")
                        break

                    position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")

                    #verifica se a posição é válida ou se já está ocupada
                    while not valida(position):
                        position = input("Posição Inválida ")

                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada\n")

                    #adiciona a jogada na lista de jogadas de 0
                    game.jogadas2.append(position)
                    #envia mensagem com a posição jogada para o outro peer
                    cliente.send_msg(position)
                    game.showBoard()

                    #verifica se o jogador 0 ganhou
                    if game.ganhar(game.jogador):
                        print('Jogador 0 ganhou')
                        break


        #verifica se acabaram as jogadas
        if game.jogadas_disponiveis == 0:
            print("Deu velha")
            break


def main():
    print(posicoes)

    #inicia o jogo, cliente, servidor(do peer) e faz conexão com o servidor
    game = Game()
    cliente = Game_client()
    servidor = Game_server()
    con = Connection()
    peer = con.get_peer()
    servidor.port = peer['rec_port']
    cliente.port = peer['port']
    cliente.host = peer['ip']
    game.jogador = peer['jogador']

    #verifica qual é o jogador e roda o jogo
    if game.jogador == 'X':
        do_jogo_X(game, cliente, servidor)

    elif game.jogador == '0':
        do_jogo_0(game, cliente, servidor)



    cliente.close_connection()
    servidor.close_connection()

if __name__ == '__main__':
    main()
