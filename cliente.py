import socket

def enviar_comando(socket_cliente, comando):
    socket_cliente.send(comando.encode())

def enviar_inteiro(socket_cliente, valor):
    socket_cliente.send(valor.to_bytes(4, "big", signed=True))

def enviar_string(socket_cliente, valor):
    socket_cliente.send(len(valor).to_bytes(4, "big", signed=True))  # Envia o comprimento da string
    socket_cliente.send(valor.encode())  # Envia a string

def receber_resposta(socket_cliente):
    resposta = socket_cliente.recv(1024)  # Recebe a resposta (limite de 1024 bytes)
    print(resposta.decode())

def criar_filme(socket_cliente):
    titulo = input("Digite o título do filme: ")
    genero = input("Digite o genero do filme: ")
    ano = int(input("Digite o ano do filme: "))
    nota = -1
    nota = int(input("Digite o nota do filme ou pressione enter para nao adicionar nota: "))
    

    enviar_comando(socket_cliente, 'c')
    enviar_inteiro(socket_cliente, id)
    enviar_string(socket_cliente, titulo)
    enviar_inteiro(socket_cliente, ano)
    
    receber_resposta(socket_cliente)

def listar_filmes(socket_cliente):
    enviar_comando(socket_cliente, 'r')
    receber_resposta(socket_cliente)

def atualizar_filme(socket_cliente):
    id = int(input("Digite o ID do filme a ser atualizado: "))
    novo_titulo = input("Digite o novo título do filme: ")
    novo_ano = int(input("Digite o novo ano do filme: "))
    
    enviar_comando(socket_cliente, 'u')
    enviar_inteiro(socket_cliente, id)
    enviar_string(socket_cliente, novo_titulo)
    enviar_inteiro(socket_cliente, novo_ano)
    
    receber_resposta(socket_cliente)

def deletar_filme(socket_cliente):
    id = int(input("Digite o ID do filme a ser deletado: "))
    
    enviar_comando(socket_cliente, 'd')
    enviar_inteiro(socket_cliente, id)
    
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
