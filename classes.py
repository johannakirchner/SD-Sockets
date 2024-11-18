import Pyro5.server
from Pyro5.serializers import SerializerBase

class Filme:
    def __init__(self, id: int, titulo: str, genero: str, ano: int, nota: float):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.nota = nota
    def __str__(self):
        return f"ID: {self.id}, Título: {self.titulo}, Genero: {self.genero}, Ano: {self.ano}, Nota: {self.nota}"


def filme_class_to_dict(obj: Filme):
    movieDict = {
        "__class__": "objeto.Filme",
        "id": obj.id,
        "titulo": obj.titulo,
        "genero": obj.genero,
        "ano": obj.ano,
        "nota": obj.nota
    }
    return movieDict

def filme_dict_to_class(dict):
    a = Filme(dict["id"], dict["titulo"], dict["genero"], dict["ano"], dict["nota"])
    return a


@Pyro5.server.expose
class BancoDeFilmes:
    __next_id = 0
    def __init__(self):
        self.__filmes = []

    def criar_filme(self, titulo: str, genero: str, ano: int, nota: float = -1.0):
        id = BancoDeFilmes.__next_id
        BancoDeFilmes.__next_id += 1
        self.__filmes.append(Filme(id=id, titulo=titulo, ano=ano, genero=genero, nota=nota))
        print("Filme adicionado com sucesso")

    def listar_filmes(self):
        try:
            lista = [movie.__str__() for movie in self.__filmes]
            return lista
        except Exception as e:
            print(f"Erro ao listar filmes: {e}")
            return []

    def editar_filme(self, id: int, nova_nota: float):
        for filme in self.__filmes:
            if filme.id == id:
                filme.nota = nova_nota
                print("Operação realizada com sucesso!")
                break
        else:
            print("A operação falhou!")

    def remover_filme(self, id):
        for filme in self.__filmes:
            if filme.id == id:
                self.__filmes.remove(filme)
                print("Operação realizada com sucesso!")
                break
        else:
            print("A operação falhou!")
    
    def encerrar_conexao(self):
        print("Conexão encerrada pelo cliente.")

    def registrar_serializadores():
        from Pyro5.serializers import SerializerBase
        SerializerBase.register_class_to_dict(Filme, filme_class_to_dict)
        SerializerBase.register_dict_to_class("objeto.Filme", filme_dict_to_class)

