import cherrypy
import json


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
@cherrypy.tools.json_out()
class BancoDeFilmes:
    __next_id = 0
    def __init__(self):
        self.__filmes = []

    def criar_filme(self):
        try:
            # le o corpo da requisicao e converte JSON
            body = cherrypy.request.body.read().decode("utf-8")
            data = json.loads(body)

            # confere se os campos obrigatorios estao presentes
            if not all(k in data for k in ["titulo", "ano", "genero"]):
                raise cherrypy.HTTPError(400, "Parâmetros obrigatórios: titulo, ano, genero")

            titulo = data["titulo"]
            ano = int(data["ano"])
            genero = data["genero"]
            nota = float(data.get("nota", -1))  

            # validacoes
            if not titulo.strip():
                raise cherrypy.HTTPError(422, "O campo 'titulo' não pode ser vazio")
        
            if not genero.strip():
                raise cherrypy.HTTPError(422, "O campo 'genero' não pode ser vazio")
            
            if not isinstance(ano, int) or ano < 1900 or ano > 2100:
                raise cherrypy.HTTPError(422, "O campo 'ano' deve ser um número entre 1900 e 2100")
            
            if nota != -1 and (not isinstance(nota, (int, float)) or nota < 0):
                raise cherrypy.HTTPError(422, "A 'nota' deve ser um número não negativo")


            id = BancoDeFilmes.__next_id
            BancoDeFilmes.__next_id += 1
            self.__filmes.append(Filme(id=id, titulo=titulo, ano=ano, genero=genero, nota=nota))

            return f"Filme '{titulo}' adicionado com sucesso!"
        except json.JSONDecodeError:
            raise cherrypy.HTTPError(415, "Formato de entrada inválido. Deve ser um JSON.")
        except Exception as e:
            raise cherrypy.HTTPError(500, f"Erro ao criar filme: {e}")


    def listar_filmes(self):
        try:
            # transforma a lista de filmes em json
            filmes_json = [{"id": filme.id, "titulo": filme.titulo, "genero": filme.genero, "ano": filme.ano, "nota": filme.nota} for filme in self.__filmes]
            return filmes_json 
        except Exception as e:
            print(f"Erro ao listar filmes: {e}")
            raise cherrypy.HTTPError(500, "Erro ao listar filmes")

    def editar_filme(self, id): 
        try:
            # le o corpo da requisicao e converte JSON
            body = cherrypy.request.body.read().decode("utf-8")
            data = json.loads(body)

            if "nota" not in data:
                raise cherrypy.HTTPError(400, "Parâmetro obrigatório: nota")
            
            nota = float(data.get("nota", -1))  
    
            if nota != -1 and (not isinstance(nota, (int, float)) or nota < 0):
                raise cherrypy.HTTPError(422, "A 'nota' deve ser um número não negativo")

            for filme in self.__filmes:
                if filme.id == int(id): 
                    filme.nota = nota
                    return {"status": "sucesso", "mensagem": "Filme editado com sucesso!"}

            return {"status": "erro", "mensagem": "Filme não encontrado!"}

        except json.JSONDecodeError:
            raise cherrypy.HTTPError(415, "Formato de entrada inválido. Deve ser um JSON.")
        except Exception as e:
            raise cherrypy.HTTPError(500, f"Erro ao editar filme: {e}")


    def remover_filme(self, id):
        try:
            for filme in self.__filmes:
                if filme.id == int(id):
                    self.__filmes.remove(filme)
                    return "Filme removido com sucesso"

            raise cherrypy.HTTPError(404, "Filme não encontrado")
        except Exception as e:
            raise cherrypy.HTTPError(500, f"Erro ao remover filme: {e}")


