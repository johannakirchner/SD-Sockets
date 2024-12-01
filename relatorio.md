Alunos: Gabriel de O. e S. P. Barreto RA: 2326221, Johanna Kirchner RA: 2265010

Neste trabalho, continuamos desenvolvendo o 'Gerenciador de Filmes'.

Para a função `criar_filme`, a requisição precisa conter os campos `titulo`, `ano` e `genero`, sendo que o campo `nota` é opcional. Quando um desses campos obrigatórios esteja ausente, é gerado um erro com código HTTP 400, que indica que a requisição está mal formada. As validações para cada campo são:
- `titulo` e `genero` são campos de texto, então é validado se não estão vazios;
- `ano` valida se está entre 1900 e 2100;
- `nota` é opcional, mas caso presente, deve ser um número maior que zero.

Quando uma dessas validações não são atendidas, é retornado um erro com código HTTP 422, que indica que a sintaxe da requisição está correta mas não foi possível processar os conteúdos internos.

Para `editar_filme`, a requisição necessita de um ID e no body a nota que será atribuída, com ambos sendo obrigatórios e também gera erro HTTP 400. Novamente, o campo `nota` tem uma validação de ser número e maior que zero.

Para `remover_filme`, a requisição necessita apenas do ID do filme a ser removido. 

Por fim, para `listar_filmes` não é feito nenhuma verificação, pois apenas retorna a lista dos filmes cadastrados.


Listar
```
GET http://127.0.0.1:9090/filme
```

Adicionar
```
POST http://127.0.0.1:9090/filme

{
    "titulo": "Nome do Filme",
    "genero": "Gênero do Filme",
    "ano": 2024,
    "nota": 8.5
}
```

Editar Nota
```
PATCH http://127.0.0.1:9090/filme/{id}

{
  "nota": 0
}
```

Deletar
```
DELETE http://127.0.0.1:9090/filme/{id}
```