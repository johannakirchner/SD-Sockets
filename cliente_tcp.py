import socket

def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip_serv = '127.0.0.1'
    porta_serv = 50000
    dest = (ip_serv, porta_serv)
    tcp.connect(dest)

    conexao_encerrada = False

    while not conexao_encerrada:
        # Lendo uma mensagem
        msg = input("Digite texto: ")
        if msg == "":
            break
        msg = msg.encode()

        # Preparando e enviando a mensagem, que estará
        # no formato de 2 bytes de tamanho e um texto
        # no tamanho especificado
        tam = (len(msg)).to_bytes(2, 'big')
        tcp.send(tam + msg)

        # Lê o tamanho da mensagem de resposta
        bytes_resp = tcp.recv(2)
        tam_resp = int.from_bytes(bytes_resp, 'big')

        # Lê a mensagem, considerando o tamanho recebido
        resp = tcp.recv(tam_resp)

        print('Resposta: ', resp.decode())

    tcp.close()
    input('aperte enter para encerrar')

if __name__ == '__main__':
    main()