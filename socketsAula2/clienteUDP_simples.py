import socket

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ip_serv = '127.0.0.1'     
porta_serv = 50000
dest = (ip_serv, porta_serv)

# Lendo uma mensagem do usuário
print("Digite mensagem:" )
msg = input()

# Preparando e enviando a mensagem, que estará
# no formato de 2 bytes de tamanho e um texto
# no tamanho especificado
tam = (len(msg)).to_bytes(2, 'big')
udp.sendto(tam + msg.encode(), dest)

# Lê o tamanho da mensagem de resposta
bytes_resp, serv = udp.recvfrom(65535)

tam_resp = int.from_bytes(bytes_resp[0:2], 'big')
resp = bytes_resp[2:2+tam_resp]

print('Resposta: ', resp.decode())

udp.close()
input('aperte enter para encerrar')
