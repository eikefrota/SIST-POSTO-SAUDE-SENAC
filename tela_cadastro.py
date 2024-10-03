from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk

class SistemaCadastro:
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        self.pacientes = []
        
        # Criar a interface uma vez
        self.criar_interface_cadastro()
        
    def criar_interface_cadastro(self):
        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="#FFFFFF")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.3, relheight=0.9)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        self.criar_widgets_cadastro()

    def criar_widgets_cadastro(self):
        self.retornar_label("Nome:", 0)
        self.entry_nome = self.retornar_entry(1, "Digite o nome")

        self.retornar_label("CPF:", 2)
        self.entry_cpf = self.retornar_entry(3, "Digite o CPF")

        self.retornar_label("Data de Nascimento:", 4)
        self.entry_datanasc = self.retornar_entry(5, "DD/MM/AA")

        self.retornar_label("Telefone:", 6)
        self.entry_telefone = self.retornar_entry(7, "Digite o telefone")

        self.retornar_label("Email:", 8)
        self.entry_email = self.retornar_entry(9, "Digite o email")

        self.retornar_label("Endereço:", 10)
        self.entry_endereco = self.retornar_entry(11, "Digite o endereço")
        
        self.botao_cadastrar = ctk.CTkButton(self.frame, text="Cadastrar", command=self.cadastrar_paciente)
        self.botao_cadastrar.grid(row=12, column=0, columnspan=2,  padx=10, pady=20)

        self.btn_mostrar_tabela = ctk.CTkButton(self.frame, text="Mostrar tabela", command=self.exibir_tabela_pacientes)
        self.btn_mostrar_tabela.grid(row=13, column=0, columnspan=2, padx=10, pady=20)

    def retornar_label(self, label_info, linha):
        return self.criar_label(label_info, linha)
    
    def retornar_entry(self, linha, placeholder_inf):
        return self.criar_entry(linha, placeholder_inf)

    def cadastrar_paciente(self):
        # Verificar se as entradas estão inicializadas
        if all([self.entry_nome, self.entry_cpf, self.entry_datanasc, 
                self.entry_telefone, self.entry_email, self.entry_endereco]):
            nome = self.entry_nome.get()
            cpf = self.entry_cpf.get()
            datanasc = self.entry_datanasc.get()
            telefone = self.entry_telefone.get()
            email = self.entry_email.get()
            endereco = self.entry_endereco.get()

            paciente = {
                "nome": nome,
                "cpf": cpf,
                "data_nascimento": datanasc,
                "telefone": telefone,
                "email": email,
                "endereco": endereco
            }
            self.exibir_mensegebox()

            self.pacientes.append(paciente)
            print(f"Paciente cadastrado: {paciente}")
            self.limpar_campos()
        else:
            print("Erro: Entradas não inicializadas!")
        


    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_cpf.delete(0, ctk.END)
        self.entry_datanasc.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)

    def criar_label(self, texto, linha):
        label = ctk.CTkLabel(self.frame, text=texto, font=("Arial", 12, "bold"))
        label.grid(row=linha, column=1, padx=10, pady=(10, 0), sticky="w")

    def exibir_mensegebox(self):
       messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")  

    def criar_entry(self, linha, placeholder):
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=250, font=("Montserrat", 16))
        entry.grid(row=linha, column=1, padx=10, pady=(0, 20), sticky="w")
        return entry  # Certifique-se de retornar a entrada
    
    def exibir_tabela_pacientes(self):
        # Limpar a tela para mostrar a tabela
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        # Criar a Tabela (Treeview)
        self.tabela_frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="#FFFFFF")
        self.tabela_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.7, relheight=0.7)

        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")
        
        # Definir as colunas
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Data de Nascimento", text="Data de Nascimento")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")
        self.tabela.heading("Endereço", text="Endereço")

        self.tabela.column("Nome", width=150)
        self.tabela.column("CPF", width=100)
        self.tabela.column("Data de Nascimento", width=120)
        self.tabela.column("Telefone", width=100)
        self.tabela.column("Email", width=200)
        self.tabela.column("Endereço", width=200)

        self.tabela.pack(fill="both", expand=True)

        # Inserir os pacientes cadastrados na tabela
        for paciente in self.pacientes:
            self.tabela.insert("", "end", values=(paciente["nome"], paciente["cpf"], paciente["data_nascimento"], paciente["telefone"], paciente["email"], paciente["endereco"]))
        
        # Botão para retornar à tela de cadastro
        self.botao_voltar = ctk.CTkButton(self.tabela_frame, text="Voltar", command=self.criar_interface_cadastro)
        self.botao_voltar.pack(pady=10)

# Exemplo de execução
if __name__ == "__main__":
    root = ctk.CTk()
    app = SistemaCadastro(root)
    root.mainloop()
