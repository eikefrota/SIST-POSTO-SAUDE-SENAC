import os
import customtkinter as ctk
from tkinter import ttk, messagebox, Menu
from PIL import Image, ImageTk

class SistemaCadastroView:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.configurar_janela()
        self.logo_path = os.path.abspath("C:/Users/Clean Vision/OneDrive/Área de Trabalho/logo/logo.png")
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        self.exibir_tela_recepcionista()

    def configurar_janela(self):
        self.janela.title("Sistema de Cadastro")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        self.janela.resizable(True, True)

    def carregar_imagem(self, caminho, tamanho):
        """Carrega e redimensiona uma imagem usando apenas CTkImage."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def criar_label(self, texto, linha, coluna, frame=None):
        """Cria e retorna um label em um frame específico ou no frame principal se não especificado."""
        if frame is None:
            frame = self.frame  # Default para o frame principal
        label = ctk.CTkLabel(frame, text=texto, font=("Arial", 14, "bold"))
        label.grid(row=linha, column=coluna, padx=(30, 30), pady=(0, 0), sticky="w")
        return label

    def criar_entry(self, linha, coluna, placeholder, frame=None):
        """Cria um campo de entrada com placeholder em um frame específico ou no frame principal se não especificado."""
        if frame is None:
            frame = self.frame  # Default para o frame principal
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=300, height=30, font=("Montserrat", 16))
        entry.grid(row=linha, column=coluna, padx=(30, 30), pady=(0, 10), sticky="ns")
        return entry

    def criar_logo(self, frame=None):
        if frame is None:
            frame = self.frame  # Default para o frame principal
        self.label_logo = ctk.CTkLabel(frame, image=self.logo_image, text="")
        self.label_logo.grid(row=1, column=1, padx=(0, 20), pady=(10, 5), sticky="w")

    def criar_titulo(self, texto, frame=None):
        if frame is None:
            frame = self.frame  # Default para o frame principal
        self.label_titulo = ctk.CTkLabel(frame, text=texto, font=("Montserrat", 20, "bold"))
        self.label_titulo.grid(row=1, column=1, padx=(20, 0), pady=(10, 5), sticky="e")

    def exibir_tela_recepcionista(self):
        """Tela inicial para o recepcionista com layout padrão."""
        # Limpar a janela atual
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Criar um novo frame
        self.frame_recepcionista = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame_recepcionista.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.6)

        self.frame_recepcionista.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_recepcionista.grid_rowconfigure((1, 10), weight=1)

        # Criar logo e título
        self.criar_logo(self.frame_recepcionista)
        self.criar_titulo("Área do Recepcionista", self.frame_recepcionista)

        # Botões
        self.botao_cadastro = ctk.CTkButton(self.frame_recepcionista, text="Cadastrar Paciente", 
                                            font=("Arial", 18, "bold"), width=200, height=40, 
                                            command=self.criar_interface_cadastro)
        self.botao_cadastro.grid(row=3, column=1, padx=20, pady=20, sticky="e")

        self.botao_mostrar_tabela = ctk.CTkButton(self.frame_recepcionista, text="Consultar Paciente", 
                                                font=("Arial", 18, "bold"), width=200, height=40, 
                                                command=self.exibir_tabela_pacientes)
        self.botao_mostrar_tabela.grid(row=3, column=2, padx=20, pady=20, sticky="w")

        self.botao_sair = ctk.CTkButton(self.frame_recepcionista, text="Sair", 
                                        font=("Arial", 16, "bold"), width=100, height=30, 
                                        command=self.fazer_logout)
        self.botao_sair.grid(row=5, column=1, columnspan=2, padx=(5, 5), pady=10)

        # Atualizar a janela
        self.janela.update()

    def fazer_logout(self):
        if self.controller.confirmar_acao("Confirmar Logout", "Tem certeza que deseja sair?"):
            self.controller.fazer_logout()

    def criar_interface_cadastro(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

        self.frame.grid_columnconfigure((0, 3), weight=1)
        self.frame.grid_columnconfigure((1, 2), weight=0)

        # Recarregar a imagem da logo antes de criar os widgets
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))

        self.criar_widgets_formulario()

        self.botao_cadastrar = ctk.CTkButton(self.frame, text="Cadastrar", font=("Arial", 14, "bold"), width=200, height=30, command=self.enviar_cadastro)
        self.botao_cadastrar.grid(row=9, column=1, padx=(5, 5), pady=20, sticky="e")

        self.botao_voltar = ctk.CTkButton(self.frame, text="Voltar para Tela Principal", font=("Arial", 14, "bold"), width=200, height=30, command=self.exibir_tela_recepcionista)
        self.botao_voltar.grid(row=9, column=2, padx=(5,5), pady=20, sticky="w")

    def criar_widgets_formulario(self, valores=None, modo_edicao=False):
        self.criar_logo()
        self.criar_titulo("Cadastro de Paciente" if not modo_edicao else "Atualização de Cadastro")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(10, weight=2)

        # Nome, CPF e Data de Nascimento (não editáveis em modo de edição)
        self.criar_label("Nome:", 2, 1)
        self.entry_nome = self.criar_entry(3, 1, "Digite o nome completo")
        
        self.criar_label("CPF:", 2, 2)
        self.entry_cpf = self.criar_entry(3, 2, "XXX.XXX.XXX-XX")
        self.entry_cpf.bind("<KeyRelease>", self.formatar_cpf)
        
        self.criar_label("Data de Nascimento:", 4, 1)
        self.entry_datanasc = self.criar_entry(5, 1, "DD/MM/AAAA")
        self.entry_datanasc.bind("<KeyRelease>", self.formatar_data_nascimento)

        # Telefone, Email e Endereço (sempre editáveis)
        self.criar_label("Telefone:", 4, 2)
        self.entry_telefone = self.criar_entry(5, 2, "(DDD) 91234-5678")
        self.entry_telefone.bind("<KeyRelease>", self.formatar_telefone)

        self.criar_label("Email:", 6, 1)
        self.entry_email = self.criar_entry(7, 1, "exemplo@dominio.com")

        self.criar_label("Endereço:", 6, 2)
        self.entry_endereco = self.criar_entry(7, 2, "Digite o endereço")

        if valores:
            self.preencher_campos(valores)
        
        if modo_edicao:
            self.entry_nome.configure(state="readonly")
            self.entry_cpf.configure(state="readonly")
            self.entry_datanasc.configure(state="readonly")

    def formatar_cpf(self, event):
        cpf = self.entry_cpf.get()
        cpf = ''.join(filter(str.isdigit, cpf))
        cpf = cpf[:11]  # Limita a 11 dígitos
        
        cpf_formatado = ''
        for i, digit in enumerate(cpf):
            if i == 3 or i == 6:
                cpf_formatado += '.'
            elif i == 9:
                cpf_formatado += '-'
            cpf_formatado += digit
        
        self.entry_cpf.delete(0, ctk.END)
        self.entry_cpf.insert(0, cpf_formatado)

    def formatar_telefone(self, event):
        telefone = self.entry_telefone.get()
        telefone = ''.join(filter(str.isdigit, telefone))
        telefone = telefone[:11]  # Limita a 11 dígitos
        
        if len(telefone) > 2:
            telefone = f"({telefone[:2]}) {telefone[2:]}"
        if len(telefone) > 10:
            telefone = f"{telefone[:10]}-{telefone[10:]}"
        
        self.entry_telefone.delete(0, ctk.END)
        self.entry_telefone.insert(0, telefone)

    def formatar_data_nascimento(self, event):
        data = self.entry_datanasc.get()
        data = ''.join(filter(str.isdigit, data))
        data = data[:8]  # Limita a 8 dígitos
        
        if len(data) > 2:
            data = f"{data[:2]}/{data[2:]}"
        if len(data) > 5:
            data = f"{data[:5]}/{data[5:]}"
        
        self.entry_datanasc.delete(0, ctk.END)
        self.entry_datanasc.insert(0, data)

    def preencher_campos(self, valores):
        self.entry_nome.delete(0, 'end')
        self.entry_nome.insert(0, valores.get("nome", ""))
        
        self.entry_cpf.delete(0, 'end')
        self.entry_cpf.insert(0, valores.get("cpf", ""))
        
        self.entry_datanasc.delete(0, 'end')
        self.entry_datanasc.insert(0, valores.get("data_nascimento", ""))
        
        self.entry_telefone.delete(0, 'end')
        self.entry_telefone.insert(0, valores.get("telefone", ""))
        
        self.entry_email.delete(0, 'end')
        self.entry_email.insert(0, valores.get("email", ""))
        
        self.entry_endereco.delete(0, 'end')
        self.entry_endereco.insert(0, valores.get("endereco", ""))

    def exibir_tabela_pacientes(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        self.tabela_frame = ctk.CTkFrame(self.janela, fg_color="white")
        self.tabela_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)
        
        self.tabela_frame.grid_columnconfigure(0, weight=1)
        self.tabela_frame.grid_rowconfigure(1, weight=1)

        self.entry_pesquisa = ctk.CTkEntry(self.tabela_frame, placeholder_text="Digite o nome ou CPF", width=150, font=("Arial", 14))
        self.entry_pesquisa.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        botao_pesquisar = ctk.CTkButton(self.tabela_frame, text="Pesquisar", font=("Arial", 14, "bold"), command=self.realizar_pesquisa)
        botao_pesquisar.grid(row=0, column=2, padx=10, pady=10)

        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        for col in self.tabela["columns"]:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, anchor="center", width=150)

        self.tabela.column("Nome", width=250)
        self.tabela.column("Email", width=250)
        self.tabela.column("Endereço", width=300)

        self.tabela.tag_configure('evenrow', background='#E8E8E8')
        self.tabela.tag_configure('oddrow', background='#FFFFFF')

        self.tabela.bind("<Button-3>", self.mostrar_menu_contexto)

        self.tabela.grid(row=1, column=0, columnspan=3, sticky="nsew")

        scrollbar_y = ttk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tabela.yview)
        scrollbar_y.grid(row=1, column=3, sticky="ns")

        scrollbar_x = ttk.Scrollbar(self.tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_x.grid(row=2, column=0, columnspan=3, sticky="ew")

        self.tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.botao_voltar = ctk.CTkButton(self.tabela_frame, text="Voltar á tela inicial",  font=("Arial", 14, "bold"), command=self.exibir_tela_recepcionista)
        self.botao_voltar.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

        # Após criar a tabela, chamamos o controlador para atualizá-la
        self.controller.atualizar_tabela()

    def realizar_pesquisa(self):
        criterio = self.entry_pesquisa.get()
        self.controller.filtrar_pacientes(criterio)

    def mostrar_menu_contexto(self, event):
        item = self.tabela.identify_row(event.y)
        if item:
            menu = Menu(self.janela, tearoff=0)
            menu.add_command(label="Alterar", command=lambda: self.iniciar_alteracao(item))
            menu.add_command(label="Excluir", command=lambda: self.controller.excluir_paciente(item))
            menu.post(event.x_root, event.y_root)
    
    def exibir_formulario_alteracao(self, item, paciente):
        # Limpar a janela
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Criar o frame para o formulário de alteração
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

        self.frame.grid_columnconfigure((0, 3), weight=1)
        self.frame.grid_columnconfigure((1, 2), weight=0)

        # Criar os widgets do formulário com os dados do paciente
        self.criar_widgets_formulario(paciente, modo_edicao=True)

        # Botão para salvar as alterações
        self.botao_salvar = ctk.CTkButton(self.frame, text="Salvar Alterações", font=("Arial", 14, "bold"), width=200, height=30, command=lambda: self.salvar_alteracoes(item))
        self.botao_salvar.grid(row=9, column=1, padx=(5, 5), pady=20, sticky="e")

        # Botão para cancelar
        self.botao_cancelar = ctk.CTkButton(self.frame, text="Cancelar", font=("Arial", 14, "bold"), width=200, height=30, command=self.exibir_tabela_pacientes)
        self.botao_cancelar.grid(row=9, column=2, padx=(5,5), pady=20, sticky="w")

    def salvar_alteracoes(self, item):
        dados = self.obter_dados_formulario()
        self.controller.alterar_paciente(item, **dados)
        self.exibir_tabela_pacientes()

    def iniciar_alteracao(self, item):
        # Obter os dados do item selecionado
        valores = self.tabela.item(item, 'values')
        # Chamar o controlador para iniciar o processo de alteração
        self.controller.iniciar_alteracao_paciente(item, valores)

    def atualizar_tabela(self, pacientes):
        if not hasattr(self, 'tabela'):
            # Se a tabela ainda não foi criada, não fazemos nada
            return

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for i, paciente in enumerate(pacientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tabela.insert("", "end", values=(
                paciente.nome,
                paciente.cpf,
                paciente.data_nascimento,
                paciente.telefone,
                paciente.email,
                paciente.endereco
        ), tags=(tag,))
        
    def fechar_janela_alteracao(self):
        # Destruir o frame de alteração
        if hasattr(self, 'frame'):
            self.frame.destroy()
        # Exibir novamente a tabela de pacientes
        self.exibir_tabela_pacientes()

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def confirmar_acao(self, titulo, mensagem):
        return messagebox.askyesno(titulo, mensagem)

    def enviar_cadastro(self):
        dados = self.obter_dados_formulario()
        self.controller.cadastrar_paciente(**dados)

    def obter_dados_formulario(self):
        return {
            "nome": self.entry_nome.get(),
            "cpf": self.entry_cpf.get(),
            "data_nascimento": self.entry_datanasc.get(),
            "telefone": self.entry_telefone.get(),
            "email": self.entry_email.get(),
            "endereco": self.entry_endereco.get()
        }

    def limpar_campos(self):
        for entry in [self.entry_nome, self.entry_cpf, self.entry_datanasc, self.entry_telefone, self.entry_email, self.entry_endereco]:
            entry.delete(0, ctk.END)