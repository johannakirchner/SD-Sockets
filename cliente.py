import socket

def codificar_comando(comando):
    return comando.encode()

def codificar_inteiro(valor):
    return valor.to_bytes(4, "big", signed=True)

def codificar_string(valor):
    mensagem = len(valor).to_bytes(4, "big", signed=True)  # Envia o comprimento da string
    mensagem += valor.encode()  # Envia a string
    return mensagem

def receber_resposta(socket_cliente):
    resposta = int.from_bytes(socket_cliente.recv(4), "big", signed=True)
    if resposta == 1:
        print("Operacao realizada com sucesso")
    else:
        print("Erro na operacao")

def receber_lista(socket_cliente):
    print("Aqui esta sua lista de filmes")
    tam_lista = int.from_bytes(socket_cliente.recv(4), "big", signed=True)
    for i in range(tam_lista):
        tam_item = int.from_bytes(socket_cliente.recv(4), "big", signed=True)
        info = socket_cliente.recv(tam_item).decode()
        print(info)

def criar_filme(socket_cliente):
    titulo = input("Digite o título do filme: ")
    genero = input("Digite o genero do filme: ")
    ano = int(input("Digite o ano do filme: "))
    nota = input("Digite a nota do filme ou pressione enter para nao adicionar nota: ")
    if nota == "":
        nota = -1
    else:
        nota = int(nota)

    mensagem = codificar_comando('c')
    mensagem += codificar_string(titulo)
    mensagem += codificar_string(genero)
    mensagem += codificar_inteiro(ano)
    mensagem += codificar_inteiro(nota)

    socket_cliente.send(mensagem)
    receber_resposta(socket_cliente)

def listar_filmes(socket_cliente):
    mensagem = codificar_comando('r')
    socket_cliente.send(mensagem)
    receber_lista(socket_cliente)

def atualizar_filme(socket_cliente):
    listar_filmes(socket_cliente)
    id = int(input("Digite o ID do filme a ser atualizado: "))
    nova_nota = int(input("Digite a nova nota do filme: "))
    
    mensagem = codificar_comando('u')
    mensagem += codificar_inteiro(id)
    mensagem += codificar_inteiro(nova_nota)
    socket_cliente.send(mensagem)

    receber_resposta(socket_cliente)

def deletar_filme(socket_cliente):
    id = int(input("Digite o ID do filme a ser deletado: "))
    
    mensagem = codificar_comando('d')
    mensagem += codificar_inteiro(id)
    socket_cliente.send(mensagem)

    receber_resposta(socket_cliente)

def main():
    ip = '127.0.0.1'
    porta = 50000
    destino = (ip, porta)
    
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect(destino)

    while True:
        print("\nEscolha uma operação:")
        print("1. Criar filme")
        print("2. Listar filmes")
        print("3. Atualizar filme")
        print("4. Deletar filme")
        print("5. Sair")
        
        opcao = input("Digite sua escolha: ")
        
        if opcao == '1':
            criar_filme(socket_cliente)
        elif opcao == '2':
            listar_filmes(socket_cliente)
        elif opcao == '3':
            atualizar_filme(socket_cliente)
        elif opcao == '4':
            deletar_filme(socket_cliente)
        elif opcao == '5':
            enviar_comando(socket_cliente, 's')
            socket_cliente.close()
            print("Conexão encerrada.")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == '__main__':
    main()
