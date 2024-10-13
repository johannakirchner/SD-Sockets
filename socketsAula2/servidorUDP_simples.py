import socket

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip = ''
porta = 50000
origem = (ip, porta)

# Vincula com a porta e IP usados
udp.bind(origem)

# Necessário ler a mensagem toda, 
# senão é marcada como lida e descartada
dados, cliente = udp.recvfrom(65535)

# Leitura da parte de tamanho
tam_msg = int.from_bytes(bytes(dados[0:2]), 'big')
print('Tamanho da mensagem: ', tam_msg)

# Leitura da parte de dados
msg = dados[2:2+tam_msg]
print('Mensagem recebida: ', msg.decode())

# Enviando a resposta, em mensagem com o formato
# de 2 bytes de tamanho, e uma mensagem no tamanho indicado
resp = 'Ola, seja bem vindo ao server UDP!'
tam_resp = (len(resp)).to_bytes(2,'big')
udp.sendto(tam_resp + resp.encode(), cliente)

# Fechando o socket
udp.close()

input('aperte enter para encerrar')
