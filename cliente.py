import sys
import Pyro5.client, Pyro5.errors

def criar_filme(banco_filmes):
    titulo = input("Digite o nome do filme: ")
    genero = input("Digite o genero do filme: ")
    ano = input("Digite o ano do filme: ")
    nota = input("Digite a nota do filme ou deixe em branco: ")
    if not nota:
        nota = -1
    banco_filmes.criar_filme(titulo, genero, ano, nota)

def atualizar_filme(banco_filmes):
    id_filme = int(input("Digite o ID do filme que deseja atualizar: "))
    nova_nota = float(input("Digite a nova nota do filme: "))
    banco_filmes.editar_filme(id_filme, nova_nota)

def deletar_filme(banco_filmes):
    id_filme = int(input("Digite o ID do filme que deseja remover: "))
    banco_filmes.remover_filme(id_filme)

def listar_filmes(banco_filmes):
    print("\nAqui esta sua lista de filmes:")
    for filme in banco_filmes.listar_filmes():
        print(filme)

def main():
    banco_filmes = Pyro5.client.Proxy("PYRONAME:bancofilmes_gabriel_johanna")
    input("Chamada método de proxy...(pressione enter)")
    try:
        banco_filmes._pyroBind()
        input("Bind...(pressione enter)")
    except Pyro5.errors.CommunicationError:
        print("Objeto remoto nao encontrado. Encerrando execucao")
        sys.exit(1)

    while True:
        print("\nEscolha uma operação:")
        print("1. Criar filme")
        print("2. Listar filmes")
        print("3. Atualizar filme")
        print("4. Deletar filme")
        print("5. Sair")
        
        opcao = input("Digite sua escolha: ")
        
        if opcao == '1':
            criar_filme(banco_filmes)
        elif opcao == '2':
            listar_filmes(banco_filmes)
        elif opcao == '3':
            atualizar_filme(banco_filmes)
        elif opcao == '4':
            deletar_filme(banco_filmes)
        elif opcao == '5':
            banco_filmes.encerrar_conexao()
            print("Conexão encerrada.")
            break
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == '__main__':
    main()
