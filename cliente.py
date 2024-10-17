import socket

class Client:
    def __init__(self, ip = "127.0.0.1", porta =50000):
        self.__endereco_ip = ip
        self.__porta = porta

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__endereco_ip, self.__porta))

    @staticmethod
    def __codificar_comando(comando):
        return comando.encode()

    @staticmethod
    def __codificar_inteiro(valor):
        return valor.to_bytes(4, "big", signed=True)

    @staticmethod
    def __codificar_string(valor):
        mensagem = len(valor).to_bytes(4, "big", signed=True)
        mensagem += valor.encode()
        return mensagem

    def receber_resposta(self): ## Respostas sao 0 ou 1 apenas, se 1 a operacao anterior deu certo, 0 caso contrario
        resposta = int.from_bytes(self.__socket.recv(4), "big", signed=True)
        if resposta == 1:
            print("Operacao realizada com sucesso")
        else:
            print("Erro na operacao")

    def receber_lista(self):
        print("Aqui esta sua lista de filmes")
        tam_lista = int.from_bytes(self.__socket.recv(4), "big", signed=True)
        for i in range(tam_lista):
            tam_item = int.from_bytes(self.__socket.recv(4), "big", signed=True)
            info = self.__socket.recv(tam_item).decode()
            print(info)

    def criar_filme(self):
        titulo = input("Digite o título do filme: ")
        genero = input("Digite o genero do filme: ")
        ano = int(input("Digite o ano do filme: "))
        nota = input("Digite a nota do filme ou pressione enter para nao adicionar nota: ")
        if nota == "":
            nota = -1
        else:
            nota = int(nota)

        mensagem = self.__codificar_comando('c')
        mensagem += self.__codificar_string(titulo)
        mensagem += self.__codificar_string(genero)
        mensagem += self.__codificar_inteiro(ano)
        mensagem += self.__codificar_inteiro(nota)

        self.__socket.send(mensagem)
        self.receber_resposta()

    def listar_filmes(self):
        mensagem = self.__codificar_comando('r')
        self.__socket.send(mensagem)
        self.receber_lista()

    def atualizar_filme(self):
        self.listar_filmes()
        id = int(input("Digite o ID do filme a ser atualizado: "))
        nova_nota = int(input("Digite a nova nota do filme: "))

        mensagem = self.__codificar_comando('u')
        mensagem += self.__codificar_inteiro(id)
        mensagem += self.__codificar_inteiro(nova_nota)
        self.__socket.send(mensagem)

        self.receber_resposta()

    def deletar_filme(self):
        id = int(input("Digite o ID do filme a ser deletado: "))
        mensagem = self.__codificar_comando('d')
        mensagem += self.__codificar_inteiro(id)
        self.__socket.send(mensagem)

        self.receber_resposta()

    def encerrar_conexao(self):
        self.__socket.send(self.__codificar_comando('s'))
        self.receber_resposta()
        self.__socket.close()

def main():
    cliente = Client()
    while True:
        print("\nEscolha uma operação:")
        print("1. Criar filme")
        print("2. Listar filmes")
        print("3. Atualizar filme")
        print("4. Deletar filme")
        print("5. Sair")
        
        opcao = input("Digite sua escolha: ")
        
        if opcao == '1':
            cliente.criar_filme()
        elif opcao == '2':
            cliente.listar_filmes()
        elif opcao == '3':
            cliente.atualizar_filme()
        elif opcao == '4':
            cliente.deletar_filme()
        elif opcao == '5':
            cliente.encerrar_conexao()
            print("Conexão encerrada.")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == '__main__':
    main()
