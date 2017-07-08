import json
import socket

def recebe_arq(arq, tcp):
    with open(arq, 'wb') as f:
        while True:
            print ('receiving data...')
            data = tcp.recv(1024) #recebe bytes do arquivo
            print('data=%s', (data))
            if not data:
                break
            if data == b'FIM': #verifica se já recebeu todo o arquivo
                break
            f.write(data) #escreve bytes em um arquivo

    f.close()
    print('Concluido')

def send_arq(arq, con):
    f = open(arq,'rb')
    data = f.read(1024) #lê bytes do arquivo
    while (data):
        con.send(data) #envia os bytes
        data = f.read(1024)
    f.close()

    print ('Arquivo enviado')

#as funções abaixo acessam o arquivo de dados diretamente

#lê todo o arquivo de dados e o carrega em json
def get_users(fname):
    arq = open(fname, 'r')
    content = arq.read()
    arq.close()
    if not content.startswith('{'): #verifica se o arquivo está vazio
        data = json.loads('{}')

    else:
        with open(fname) as f:
            data = json.load(f)
        f.close()

    return data

#adiciona um novo usuário ao arquivo
def add_user(fname, username, password):
    success = False

    data = get_users(fname) #lê o arquivo

    #verifica se o usuário já existe
    if not username in data:
        data[username] = {'password' : password, 'pastas' : []}

        with open(fname, 'w') as f:
            json.dump(data, f)

        f.close()
        success = True #usuário adicionado

    return success

#adiciona pasta à lista de pastas de um usuário
def new_pasta(fname, user, nome_pasta):
    success = False

    data = get_users(fname)

    if user in data: #verifica se usuário existe
        data[user]['pastas'].append(nome_pasta)

        with open(fname, 'w') as f:
            json.dump(data, f)

        f.close()
        success = True #pasta adicionada

    return success

#faz autenticação do usuário
def autentication(fname, user, password):
    data = get_users(fname)

    if not user in data: #verifica se o usuário existe
        return False
    elif data[user]['password'] == password:
        #verifica se a senha está correta
        return True
    else:
        return False

#verifica se o usuário tem acesso a determinada pasta
def permission(fname, user, nome_pasta):
    data = get_users(fname)

    if not user in data:
        return False

    elif nome_pasta in data[user]['pastas']:
        #verifica se a pasta está na lista de pastas do usuário
        return True

    else: return False

#retorna a lista de pastas de um usuário
def get_pastas(fname, user):
    data = get_users(fname)

    pastas = data[user]['pastas']

    return pastas
