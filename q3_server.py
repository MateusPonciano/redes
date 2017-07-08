import socket
import json

#coloca informações de um peer em um dicionário
def get_info_peer(cliente):
    peer = dict()

    peer['ip'] = cliente[0]
    peer['port'] = cliente[1]+1
    peer['rec_port'] = 0 #porta em que o peer receberá as mensagens
    peer['jogador'] = ''

    return peer

#adiciona rec_port e carrega informações do peer em json
def get_rec_port(cliente, peer):
    peer['rec_port'] = cliente[1]+1

    jpeer = json.dumps(peer)

    return jpeer.encode('utf-8')

#envia informações de um peer para o outro peer
def send_peer(data, udp, cliente):
    return udp.sendto(data, cliente)

def main():
    #cria socket UDP
    host = ''
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 6007
    orig = (host, port)
    udp.bind(orig)

    while True:
        #recebe mensagem de um peer e guarda as informações
        msg, cliente = udp.recvfrom(1024)
        if msg.decode('utf-8') == 'Hello':
            con1 = get_info_peer(cliente)
            con1['jogador'] = 'X' #define o jogador como X
            udp.sendto('ok'.encode('utf-8'), cliente)
            print (cliente, msg.decode('utf-8'))

        while True:
            #recebe mensagem do outro peer e guarda as informações
            msg2, cliente2 = udp.recvfrom(1024)
            if msg2.decode('utf-8') == 'Hello':
                con2 = get_info_peer(cliente2)
                con2['jogador'] = '0' #define o jogador como 0
                udp.sendto('ok'.encode('utf-8'), cliente2)
                print (cliente2, msg2.decode('utf-8'))

                break

        #adiciona as portas de recepção
        jpeer1 = get_rec_port(cliente, con2)
        jpeer2 = get_rec_port(cliente2, con1)

        #envia as informações de um peer para o outro
        send_peer(jpeer2, udp, cliente2)
        send_peer(jpeer1, udp, cliente)

    udp.close()

if __name__ == '__main__':
    main()
