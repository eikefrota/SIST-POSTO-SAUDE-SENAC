import customtkinter as ctk

class Cadastro():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
    
    import customtkinter as ctk
from tkinter import messagebox
from paciente import Paciente  # Importar a classe Paciente do arquivo paciente.py

class Cadastro():
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro de Paciente")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")

        # Criando campos de entrada para os dados do paciente
        self.label_nome = ctk.CTkLabel(janela, text="Nome:")
        self.label_nome.pack(pady=5)
        self.entry_nome = ctk.CTkEntry(janela)
        self.entry_nome.pack(pady=5)

        self.label_cpf = ctk.CTkLabel(janela, text="CPF:")
        self.label_cpf.pack(pady=5)
        self.entry_cpf = ctk.CTkEntry(janela)
        self.entry_cpf.pack(pady=5)

        self.label_data_nasc = ctk.CTkLabel(janela, text="Data de Nascimento:")
        self.label_data_nasc.pack(pady=5)
        self.entry_data_nasc = ctk.CTkEntry(janela)
        self.entry_data_nasc.pack(pady=5)

        self.label_telefone = ctk.CTkLabel(janela, text="Telefone:")
        self.label_telefone.pack(pady=5)
        self.entry_telefone = ctk.CTkEntry(janela)
        self.entry_telefone.pack(pady=5)

        self.label_email = ctk.CTkLabel(janela, text="E-mail:")
        self.label_email.pack(pady=5)
        self.entry_email = ctk.CTkEntry(janela)
        self.entry_email.pack(pady=5)

        self.label_endereco = ctk.CTkLabel(janela, text="Endereço:")
        self.label_endereco.pack(pady=5)
        self.entry_endereco = ctk.CTkEntry(janela)
        self.entry_endereco.pack(pady=5)

        # Botão para cadastrar paciente
        self.botao_cadastrar = ctk.CTkButton(janela, text="Cadastrar", command=self.cadastrar_paciente)
        self.botao_cadastrar.pack(pady=20)

    # Função para cadastrar paciente
    def cadastrar_paciente(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        dataNasc = self.entry_data_nasc.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        endereco = self.entry_endereco.get()

        if nome and cpf and dataNasc and telefone and email and endereco:
            paciente = Paciente(nome, cpf, dataNasc, telefone, email, endereco)
            messagebox.showinfo("Cadastro", f"Paciente {paciente.getNome()} cadastrado com sucesso!")
        else:
            messagebox.showwarning("Erro", "Todos os campos devem ser preenchidos!")

# Código principal
if __name__ == "__main__":
    root = ctk.CTk()  # Cria a janela principal
    app = Cadastro(root)  # Inicializa a interface gráfica
    root.mainloop()  # Inicia o loop da interface
