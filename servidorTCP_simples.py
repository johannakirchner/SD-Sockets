import socket

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = ''
porta = 50000
origem = (ip, porta)

# Vincula com a porta e IP usados
tcp.bind(origem)

# Aguarda a chegada de uma conexão TCP
# Se chegar mais de uma, as demais serão recusadas
tcp.listen(1)

# Aceitar a conexão TCP recebida a mais tempo
tcp_dados, cliente = tcp.accept()

while True:
    # Tamanho da mensagem que será recebida
    tam_bytes = tcp_dados.recv(2)
    if not tam_bytes:
        break
    tam_msg = int.from_bytes(tam_bytes, 'big')

    # Recebendo a mensagem
    msg = tcp_dados.recv(tam_msg)
    if not msg:
        break
    print('Mensagem recebida: ', msg.decode())

    # Enviando a resposta, em mensagem com o formato
    # de 2 bytes de tamanho, e uma mensagem no tamanho indicado
    resp = 'Ola, seja bem vindo ao server TCP!'
    tam_resp = (len(resp)).to_bytes(2,'big')
    tcp_dados.send(tam_resp + resp.encode())

# Fechando os sockets
tcp.close()
tcp_dados.close()

input('aperte enter para encerrar')
