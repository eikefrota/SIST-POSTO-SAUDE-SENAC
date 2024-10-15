from mvc.model.model import UsuarioModel

def criar_admin():
    usuario_model = UsuarioModel()
    
    nome = input("Digite o nome do administrador: ")
    cpf = input("Digite o CPF do administrador: ")
    senha = input("Digite a senha do administrador: ")

    sucesso = usuario_model.adicionar_usuario(nome, cpf, senha, 'admin')
    if sucesso:
        print("Administrador criado com sucesso!")
    else:
        print("Erro ao criar administrador. Verifique se o CPF já está em uso.")

if __name__ == "__main__":
    criar_admin()