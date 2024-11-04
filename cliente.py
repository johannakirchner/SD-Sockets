import sys
import Pyro5.client, Pyro5.errors


def main():
    banco_filmes = Pyro5.client.Proxy("PYRONAME:bancofilmes")

    try:
        banco_filmes._pyroBind()
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
            banco_filmes.criar_filme()
        elif opcao == '2':
            banco_filmes.listar_filmes()
        elif opcao == '3':
            banco_filmes.atualizar_filme()
        elif opcao == '4':
            banco_filmes.deletar_filme()
        elif opcao == '5':
            banco_filmes.encerrar_conexao()
            print("Conexão encerrada.")
            break
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == '__main__':
    main()
