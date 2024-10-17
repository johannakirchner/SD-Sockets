import socket
import string
from threading import Thread

class Filme:
    def __init__(self, id:int, titulo:string, genero:string, ano:int, nota:int):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.nota = nota

    def __str__(self):
        return f"ID: {self.id}, Título: {self.titulo}, Genero: {self.genero}, Ano: {self.ano}, Nota: {self.nota}"

class AtendimentoCliente(Thread):

    def __init__(self, socket_dados:socket.socket):
        super().__init__()
        self.__socket_dados = socket_dados
        self.__filmes = []

    def __get_message_info(self, length):
        message = self.__socket_dados.recv(length).decode()
        return message

    def __get_message_number(self):
        return int.from_bytes(self.__socket_dados.recv(4), "big", signed=True)

    def __criar_filme(self):
        id = len(self.__filmes)
        titulo_len = self.__get_message_number()
        titulo = self.__get_message_info(titulo_len)
        genero_len = self.__get_message_number()
        genero = self.__get_message_info(genero_len)
        ano = self.__get_message_number()
        nota = self.__get_message_number()
        self.__filmes.append(Filme(id=id, titulo=titulo, ano=ano, genero=genero, nota=nota))

    def __listar_filmes(self):
        # Envia primeiro o tamanho da lista de filmes. Para cada filme...
        # envia uma string com suas informacoes e o tamanho da string (tamanho vem antes)

        resposta = len(self.__filmes).to_bytes(4, "big", signed=True)
        for movie in self.__filmes:
            aux_str = str(movie).encode()
            aux_tam = len(aux_str).to_bytes(4, "big", signed=True)
            resposta += aux_tam
            resposta += aux_str
        self.__socket_dados.send(resposta)

    def __editar_filme(self):
        id = self.__get_message_number()
        nova_nota = self.__get_message_number() ## Consome a mensagem inteira, caso o filme não seja encontrado, nao fode o buffer/proximas mensagens
        for filme in self.__filmes:
            if filme.id == id:
                filme.nota = nova_nota
                self.__enviar_resposta(True)
                break
        else:
            self.__enviar_resposta(False)

    def __remover_filme(self):
        id = self.__get_message_number()
        for filme in self.__filmes:
            if filme.id == id:
                self.__filmes.remove(filme)
                self.__enviar_resposta(True)
                break
        else:
            self.__enviar_resposta(False)

    def __enviar_resposta(self, msg: bool):
        if msg:
            resposta = (1).to_bytes(4, "big", signed=True)
        else:
            resposta = (0).to_bytes(4, "big", signed=True)
        self.__socket_dados.send(resposta)

    def run(self):
        funcao = None
        while funcao != 's':
            funcao = (self.__socket_dados.recv(1)).decode()

            if not funcao:
                self.__socket_dados.close()
                break

            if funcao == 'c':  # Criar um novo filme
                self.__criar_filme()
                self.__enviar_resposta(True)
            elif funcao == 'r':  # Listar todos os filmes
                self.__listar_filmes()
            elif funcao == 'u':  # Atualizar um filme existente
                self.__editar_filme()
            elif funcao == 'd':  # Deletar um filme
                self.__remover_filme()
            elif funcao == 's':  # Encerrar conexão
                self.__socket_dados.close()
            else:  # Se o cliente enviar algum código errado
                self.__enviar_resposta(False)

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
