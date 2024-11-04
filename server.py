import Pyro5.server, Pyro5.core

class Filme:
    def __init__(self, id: int, titulo: str, genero: str, ano: int, nota: float):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.nota = nota

    def __str__(self):
        return f"ID: {self.id}, Título: {self.titulo}, Genero: {self.genero}, Ano: {self.ano}, Nota: {self.nota}"


@Pyro5.server.expose
class BancoDeFilmes:
    def __init__(self):
        self.__filmes = []

    def __criar_filme(self, titulo: str, genero: str, ano: int, nota: float = 0.0):
        id = len(self.__filmes)
        self.__filmes.append(Filme(id=id, titulo=titulo, ano=ano, genero=genero, nota=nota))
        print("Filme adicionado com sucesso")

    def __listar_filmes(self):
        lista = []
        for movie in self.__filmes:
            lista.append(movie.__str__())
        return lista

    def __editar_filme(self, id: int, nova_nota: float):
        for filme in self.__filmes:
            if filme.id == id:
                filme.nota = nova_nota
                print("Operação realizada com sucesso!")
                break
        else:
            print("A operação falhou!")

    def __remover_filme(self, id):
        for filme in self.__filmes:
            if filme.id == id:
                self.__filmes.remove(filme)
                print("Operação realizada com sucesso!")
                break
        else:
            print("A operação falhou!")

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
                self.__enviar_resposta(True)
                self.__socket_dados.close()
            else:  # Se o cliente enviar algum código errado
                self.__enviar_resposta(False)

def main():
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(BancoDeFilmes)
    print("URI do objeto: ", uri)

    ns = Pyro5.core.locate_ns()
    ns.register("bancofilmes", uri)
    daemon.requestLoop()


if __name__ == '__main__':
    main()
