import socket
import string
from threading import Thread

# Array para armazenar os filmes em memória
filmes = []

class Filme:
    def __init__(self, id:int, titulo:string, genero:string,ano:int, nota:int):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.nota = nota


    def __str__(self):
        return f"ID: {self.id}, Título: {self.titulo},  Genero: {self.genero},Ano: {self.ano}, Nota: {self.nota}"

class AtendimentoCliente(Thread):

    def __init__(self, socket_dados:socket.socket):
        super().__init__()
        self.__socket_dados = socket_dados

    def run(self):
        global filmes
        funcao = None
        while funcao != 's':
            funcao = (self.__socket_dados.recv(1)).decode()

            if not funcao:
                self.__socket_dados.close()
                break

            if funcao == 'c':  # Criar um novo filme
                id = filmes.size()
                titulo_len = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                titulo = self.__socket_dados.recv(titulo_len).decode()
                genero_len = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                genero = self.__socket_dados.recv(genero_len).decode()
                ano = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                nota = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                filmes.append(Filme(id, titulo, ano, genero,nota))
                resposta = f"Filme {titulo} criado com sucesso!".encode()
                self.__socket_dados.send(resposta)

            elif funcao == 'r':  # Listar todos os filmes
                resposta = "\n".join(str(filme) for filme in filmes).encode()
                self.__socket_dados.send(resposta)

            elif funcao == 'u':  # Atualizar um filme existente
                id = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                for filme in filmes:
                    if filme.id == id:
                        novo_nota = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                        filme.nota = novo_nota
                        resposta = f"Filme ID {id} atualizado com sucesso para a nota {novo_nota}!".encode()
                        self.__socket_dados.send(resposta)
                        break
                else:
                    resposta = f"Filme ID {id} não encontrado!".encode()
                    self.__socket_dados.send(resposta)

            elif funcao == 'd':  # Deletar um filme
                id = int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)
                for filme in filmes:
                    if filme.id == id:
                        filmes.remove(filme)
                        resposta = f"Filme ID {id} deletado com sucesso!".encode()
                        self.__socket_dados.send(resposta)
                        break
                else:
                    resposta = f"Filme ID {id} não encontrado!".encode()
                    self.__socket_dados.send(resposta)

            elif funcao == 's':  # Encerrar conexão
                self.__socket_dados.close()

            else:  # Se o cliente enviar algum código errado
                resposta = 'Comando inválido!'.encode()
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
