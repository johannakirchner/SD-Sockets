import Pyro5.server, Pyro5.core
from classes import BancoDeFilmes

## Abrir um terceiro terminal e executar o comando: pyro5-ns


def main():
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(BancoDeFilmes)
    print("Objeto servidor publicado")
    print("URI do objeto: ", uri)

    ns = Pyro5.core.locate_ns()
    ns.register("bancofilmes_gabriel_johanna", uri)
    print("Objeto registrado no servico de nome")
    input("Pressione enter para entrar no loop de requisições...")

    daemon.requestLoop()


if __name__ == '__main__':
    main()
