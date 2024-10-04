from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk

class SistemaCadastro:
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        self.logo_path = "imagens/file.png"
        
        self.pacientes = []
        
        self.criar_interface_cadastro()
        
    def criar_interface_cadastro(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.5, relheight=0.7)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        
        for i in range(1, 13):  # Para os campos de entrada e labels
            self.frame.grid_rowconfigure(i, weight=0) 
        self.frame.grid_rowconfigure(13, weight=1)
        
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        
        self.criar_widgets_cadastro()
    
    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)
    
    def criar_label(self, texto, linha, coluna):
        label = ctk.CTkLabel(self.frame, text=texto, font=("Arial", 14, "bold"))
        label.grid(row=linha, column=coluna, padx=(42, 0), pady=(0, 0), sticky="w")
        return label

    def criar_entry(self, linha, coluna, placeholder):
        """Cria um campo de entrada com ícone."""
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=300, height=30, font=("Montserrat", 16))
        entry.grid(row=linha, column=coluna, padx=(10, 10), pady=(0,15), sticky="ns")
        return entry 
    
    def retornar_label(self, label_info, linha):
        return self.criar_label(label_info, linha)
    
    def retornar_entry(self, linha, coluna, placeholder_inf):
        return self.criar_entry(linha, coluna, placeholder_inf)

    def criar_widgets_cadastro(self):
        
        # Logo centralizado
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="n")

        # Primeiro conjunto: Nome e CPF
        self.criar_label("Nome:", 1, 0)
        self.entry_nome = self.criar_entry(2, 0, "Digite o nome completo")  # Distância maior para o Nome

        self.criar_label("CPF:", 1, 1)
        self.entry_cpf = self.criar_entry(2, 1, "XXX.XXX.XXX-XX")

        # Segundo conjunto: Data de Nascimento e Telefone
        self.criar_label("Data de Nascimento:", 3, 0)
        self.entry_datanasc = self.criar_entry(4, 0, "DD/MM/AAAA")  # Distância maior para Data de Nascimento

        self.criar_label("Telefone:", 3, 1)
        self.entry_telefone = self.criar_entry(4, 1, "(DDD) 91234-5678")

        # Terceiro conjunto: Email e Endereço
        self.criar_label("Email:", 5, 0)
        self.entry_email = self.criar_entry(6, 0, "exemplo@dominio.com")  # Distância maior para Email

        self.criar_label("Endereço:", 5, 1)
        self.entry_endereco = self.criar_entry(6, 1, "Digite o endereço")


        self.botao_cadastrar = ctk.CTkButton(self.frame, text="Cadastrar", command=self.cadastrar_paciente)
        self.botao_cadastrar.grid(row=9, column=0, columnspan=2,  padx=10, pady=20)

        self.btn_mostrar_tabela = ctk.CTkButton(self.frame, text="Mostrar tabela", command=self.exibir_tabela_pacientes)
        self.btn_mostrar_tabela.grid(row=10, column=0, columnspan=2, padx=10, pady=20)



    def cadastrar_paciente(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        datanasc = self.entry_datanasc.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        endereco = self.entry_endereco.get()

        # Criar dicionário para o paciente
        paciente = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": datanasc,
            "telefone": telefone,
            "email": email,
            "endereco": endereco
        }

        # Armazenar paciente na lista
        self.pacientes.append(paciente)
        

        # Imprimir informações do paciente
        print(f"Paciente cadastrado: {paciente}")

        # Limpar os campos após o cadastro
        self.limpar_campos()

        messagebox.showinfo("Cadastro Concluído", "Pessoa cadastrada com sucesso!")
        self.atualizar_tabela()

    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_cpf.delete(0, ctk.END)
        self.entry_datanasc.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)

    def exibir_tabela_pacientes(self):
        # Limpar a tela para mostrar a tabela
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        # Criar a Tabela (Treeview)
        self.tabela_frame = ctk.CTkFrame(self.janela, border_width=3, fg_color="#FFFFFF")
        self.tabela_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)

        # Criar a tabela toda vez que o método for chamado
        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold")) #nomes maiores e negrito
        
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

        # Sempre atualiza a tabela após a criação
        self.atualizar_tabela()

        # Botão para retornar à tela de cadastro
        self.botao_voltar = ctk.CTkButton(self.tabela_frame, text="Voltar", command=self.criar_interface_cadastro)
        self.botao_voltar.pack(pady=10)


    def atualizar_tabela(self):    # Inserir os pacientes cadastrados na tabela
        for paciente in self.pacientes:
            self.tabela.insert("", "end", values=(paciente["nome"], paciente["cpf"], paciente["data_nascimento"], paciente["telefone"], paciente["email"], paciente["endereco"]))
        
