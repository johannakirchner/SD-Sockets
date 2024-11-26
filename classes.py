import cherrypy


class Filme:
    def __init__(self, id: int, titulo: str, genero: str, ano: int, nota: float):
        self.id = id
        self.titulo = titulo
        self.genero = genero
        self.ano = ano
        self.nota = nota
    def __str__(self):
        return f"ID: {self.id}, Título: {self.titulo}, Genero: {self.genero}, Ano: {self.ano}, Nota: {self.nota}"

@cherrypy.expose
class BancoDeFilmes:
    __next_id = 0
    def __init__(self):
        self.__filmes = []

    def criar_filme(self, **args):
        id = BancoDeFilmes.__next_id
        BancoDeFilmes.__next_id += 1
        if 'titulo' in args.keys() and 'ano' in args.keys() and 'genero' in args.keys():
            if 'nota' in args.keys():
                self.__filmes.append(Filme(id=id, titulo=args['titulo'], ano=args['ano'], genero=args['genero'], nota=args['nota']))
            else:
                self.__filmes.append(Filme(id=id, titulo=args['titulo'], ano=args['ano'], genero=args['genero'], nota=-1))
        else:
            raise cherrypy.HTTPError(400, "Parametro nao informado")
        return "Filme adicionado com sucesso"

    def listar_filmes(self):
        try:
            lista = [movie.__str__() for movie in self.__filmes]
            return lista
        except Exception as e:
            print(f"Erro ao listar filmes: {e}")
            return []

    def editar_filme(self, **args):
        for filme in self.__filmes:
            if filme.id == int(args['id']):
                filme.nota = args['nota']
                return "Operação realizada com sucesso!"

        return "A operação falhou!"

    def remover_filme(self, **args):
        for filme in self.__filmes:
            if filme.id == int(args['id']):
                self.__filmes.remove(filme)
                return "Operação realizada com sucesso!"
        else:
            return "A operação falhou!"

