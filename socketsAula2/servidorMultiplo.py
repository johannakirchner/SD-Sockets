import socket
import struct
from threading import Thread

class AtendimentoCliente(Thread):

    def __init__(self, socket_dados:socket.socket):
        super().__init__()
        self.__socket_dados = socket_dados

    def run(self):
        funcao = None
        while funcao != 's':
            funcao = (self.__socket_dados.recv(1)).decode()
            # if para o caso de mensagem de desconexão do cliente (FIN e FIN ACK)
            if not funcao:
                self.__socket_dados.close()
                break
            if (funcao == 'a' or funcao == 'b' or funcao == 'c' or funcao == 'd'):
                op1 = int.from_bytes((self.__socket_dados.recv(4)),"big",signed=True)
                op2 = int.from_bytes((self.__socket_dados.recv(4)),"big",signed=True)
                if(funcao == 'a'):
                    resultado = op1 + op2
                elif(funcao == 'b'):
                    resultado = op1 - op2
                elif(funcao == 'c'):
                    resultado = op1*op2
                else:
                    resultado = op1/op2
                if (funcao == 'a' or funcao == 'b' or funcao == 'c'):
                    resposta = funcao.encode() + resultado.to_bytes(4,"big",signed=True)
                else:
                    resposta = funcao.encode() + struct.pack(">d",resultado)
                self.__socket_dados.send(resposta)
            # Mensagem de saida, encerramento do socket
            elif (funcao == 's'):
                self.__socket_dados.close()
            # Se o cliente enviar algum código errado
            else:
                resposta = 'e'.encode()
                self.__socket_dados.send(resposta)

def main():

    socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    porta = 50000

    destino = (ip,porta)
    socket_conexao.bind(destino)
    socket_conexao.listen(10)

    while True:

        socket_dados, info_cliente = socket_conexao.accept()
        thread = AtendimentoCliente(socket_dados)
        thread.start()

if __name__ == '__main__':
    main()


# estrutura de mensagem de resposta

# sempre começa com 1 byte de código
# 'a', 'b', 'c', 'd' indicam função executada corretamente
# 'a', 'b', 'c' são seguidas por um inteiro, codificado em 4 bytes, sinalizado, big endian
# 'd' é seguido por um double, 8 bytes, formato big endian
# código 'e' indica erro de pedido do cliente, e não é seguido de nada