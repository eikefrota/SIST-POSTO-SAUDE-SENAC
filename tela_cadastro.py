from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk

class SistemaCadastro:
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        self.janela.resizable(True, True)

        self.logo_path = "imagens/file.png"
        
        self.pacientes = []
        
        self.criar_interface_cadastro()
        
    def criar_interface_cadastro(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

        self.frame.grid_columnconfigure(0, weight=1)  # Coluna vazia à esquerda (expansível)
        self.frame.grid_columnconfigure(1, weight=0)  # Coluna das labels e entrys (não expansível)
        self.frame.grid_columnconfigure(2, weight=0)  # Coluna das labels e entrys (não expansível)
        self.frame.grid_columnconfigure(3, weight=1)  # Coluna vazia à direita (expansível)
        
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        
        self.criar_widgets_cadastro()
        
        self.tabela = ttk.Treeview(self.frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")
    
    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)
    
    def criar_label(self, texto, linha, coluna):
        label = ctk.CTkLabel(self.frame, text=texto, font=("Arial", 14, "bold"))
        label.grid(row=linha, column=coluna, padx=(30, 30), pady=(0, 0), sticky="w")
        return label

    def criar_entry(self, linha, coluna, placeholder):
        """Cria um campo de entrada com ícone."""
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=300, height=30, font=("Montserrat", 16))
        entry.grid(row=linha, column=coluna, padx=(30, 30), pady=(0,10), sticky="ns")
        return entry 
    
    def retornar_label(self, label_info, linha):
        return self.criar_label(label_info, linha)
    
    def retornar_entry(self, linha, coluna, placeholder_inf):
        return self.criar_entry(linha, coluna, placeholder_inf)

    def criar_widgets_cadastro(self):
        # Logo centralizado
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=1, columnspan=2, pady=(10, 5), sticky="n")

        # Primeiro conjunto: Nome e CPF
        self.criar_label("Nome:", 1, 1)  # Coluna 1 (centralizada)
        self.entry_nome = self.criar_entry(2, 1, "Digite o nome completo")  # Distância maior para o Nome

        self.criar_label("CPF:", 1, 2)  # Coluna 2
        self.entry_cpf = self.criar_entry(2, 2, "XXX.XXX.XXX-XX")

        # Segundo conjunto: Data de Nascimento e Telefone
        self.criar_label("Data de Nascimento:", 3, 1)  # Coluna 1
        self.entry_datanasc = self.criar_entry(4, 1, "DD/MM/AAAA")

        self.criar_label("Telefone:", 3, 2)  # Coluna 2
        self.entry_telefone = self.criar_entry(4, 2, "(DDD) 91234-5678")

        # Terceiro conjunto: Email e Endereço
        self.criar_label("Email:", 5, 1)
        self.entry_email = self.criar_entry(6, 1, "exemplo@dominio.com")

        self.criar_label("Endereço:", 5, 2)
        self.entry_endereco = self.criar_entry(6, 2, "Digite o endereço")

        # Botões
        self.botao_cadastrar = ctk.CTkButton(self.frame, text="Cadastrar", font=("Arial", 14, "bold"), command=self.cadastrar_paciente)
        self.botao_cadastrar.grid(row=11, column=1, padx=(5, 5), pady=20, sticky="e")

        self.btn_mostrar_tabela = ctk.CTkButton(self.frame, text="Mostrar tabela", font=("Arial", 14, "bold"), command=self.exibir_tabela_pacientes)
        self.btn_mostrar_tabela.grid(row=11, column=2, padx=(5, 5), pady=20, sticky="w")   



    def cadastrar_paciente(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        datanasc = self.entry_datanasc.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        endereco = self.entry_endereco.get()

        # Verifica se todos os campos estão preenchidos
        if nome and cpf and datanasc and telefone and email and endereco:
            try:
                # Valida o CPF e o telefone
                if len(cpf) != 11 or not cpf.isdigit():
                    raise ValueError("O CPF deve conter 11 dígitos numéricos.")
                
                if len(telefone) < 10 or not telefone.isdigit():
                    raise ValueError("O telefone deve conter apenas números e ter pelo menos 10 dígitos.")

                # Aqui não estamos convertendo datanasc, mas você pode adicionar lógica para validar a data
                # Para o email, uma validação simples:
                if "@" not in email or "." not in email:
                    raise ValueError("O e-mail informado é inválido.")

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

                # Limpar os campos após o cadastro
                self.limpar_campos()

                messagebox.showinfo("Cadastro Concluído", "Pessoa cadastrada com sucesso!")

                if hasattr(self, 'tabela'):
                    self.atualizar_tabela()

            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")


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
        self.tabela_frame = ctk.CTkFrame(self.janela, fg_color="#FFFFFF")
        self.tabela_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)

        # Configurando o grid para redimensionar dinamicamente
        self.tabela_frame.grid_columnconfigure(0, weight=1)  # Permitir que a tabela expanda
        self.tabela_frame.grid_rowconfigure(0, weight=1)     # Permitir que a tabela expanda verticalmente

        # Criar a tabela com grid, configurada para expandir conforme a janela é redimensionada
        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold")) # Nomes maiores e negrito
        
        # Definir as colunas
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Data de Nascimento", text="Data de Nascimento")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")
        self.tabela.heading("Endereço", text="Endereço")

        # Aplicar larguras sugeridas e alinhamento
        self.tabela.column("Nome", anchor="center", width=250)
        self.tabela.column("CPF", anchor="center", width=150)
        self.tabela.column("Data de Nascimento", anchor="center", width=160)
        self.tabela.column("Telefone", anchor="center", width=150)
        self.tabela.column("Email", anchor="center", width=250)
        self.tabela.column("Endereço", anchor="center", width=300)

        # Usar grid para a tabela, ocupando toda a área disponível
        self.tabela.grid(row=0, column=0, sticky="nsew")  # Expande em todas as direções
        
        # Scrollbars para caso a tabela tenha muitos itens
        scrollbar_y = ttk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tabela.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")  # Posiciona a scrollbar no lado direito da tabela
        
        scrollbar_x = ttk.Scrollbar(self.tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")  # Posiciona a scrollbar abaixo da tabela

        self.tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sempre atualiza a tabela após a criação
        self.atualizar_tabela()

        # Botão para retornar à tela de cadastro
        self.botao_voltar = ctk.CTkButton(self.tabela_frame, text="Voltar", command=self.criar_interface_cadastro)
        self.botao_voltar.grid(row=2, column=0, pady=10, sticky="ew")



    def atualizar_tabela(self):    # Inserir os pacientes cadastrados na tabela
        for paciente in self.pacientes:
            self.tabela.insert("", "end", values=(paciente["nome"], paciente["cpf"], paciente["data_nascimento"], paciente["telefone"], paciente["email"], paciente["endereco"]))
        
