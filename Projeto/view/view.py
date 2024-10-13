# view.py

import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from tkinter import Menu


class SistemaCadastroView:
    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro")
        self.master.geometry(f"{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()}+0+0")
        self.master.resizable(True, True)

        self.frame = ctk.CTkFrame(self.master, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=1)
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(10, weight=2)
        
        self.logo_path = "imagens/file.png"
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))

        self.create_widgets()
        
    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)

    def create_widgets(self):
        
        
        self.criar_logo_titulo("Cadastro Paciente")

        self.entry_nome = self.create_entry("Nome:", 2, 1, "Digite o nome completo")
        self.entry_cpf = self.create_entry("CPF:", 2, 2, "XXX.XXX.XXX-XX")
        self.entry_datanasc = self.create_entry("Data de Nascimento:", 4, 1, "DD/MM/AAAA")
        self.entry_telefone = self.create_entry("Telefone:", 4, 2, "(DDD) 91234-5678")
        self.entry_email = self.create_entry("Email:", 6, 1, "exemplo@dominio.com")
        self.entry_endereco = self.create_entry("Endereço:", 6, 2, "Digite o endereço")

        self.botao_cadastrar = ctk.CTkButton(self.frame, text="Cadastrar", font=("Arial", 14, "bold"))
        self.botao_cadastrar.grid(row=9, column=1, padx=(5, 5), pady=20, sticky="e")

        self.btn_mostrar_tabela = ctk.CTkButton(self.frame, text="Mostrar tabela", font=("Arial", 14, "bold"))
        self.btn_mostrar_tabela.grid(row=9, column=2, padx=(5, 5), pady=20, sticky="w")

    def create_entry(self, label_text, row, column, placeholder):
        label = ctk.CTkLabel(self.frame, text=label_text, font=("Arial", 14, "bold"))
        label.grid(row=row, column=column, padx=(30, 30), pady=(0, 0), sticky="w")

        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=300, height=30, font=("Montserrat", 16))
        entry.grid(row=row + 1, column=column, padx=(30, 30), pady=(0, 10), sticky="ns")

        return entry

    def criar_logo_titulo(self, texto):
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=1, column=1, padx=(0, 20), pady=(10, 5), sticky="w")
        
        self.label_titulo = ctk.CTkLabel(self.frame, text=texto, font=("Montserrat", 20, "bold"))
        self.label_titulo.grid(row=1, column=1, padx=(20, 0), pady=(10, 5), sticky="e")

        
        
        
    def obter_dados_formulario(self):
        return {
            "nome": self.entry_nome.get(),
            "cpf": self.entry_cpf.get(),
            "data_nascimento": self.entry_datanasc.get(),
            "telefone": self.entry_telefone.get(),
            "email": self.entry_email.get(),
            "endereco": self.entry_endereco.get()
        }

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_cpf.delete(0, ctk.END)
        self.entry_datanasc.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)

    def criar_tabela(self):
        self.tabela_frame = ctk.CTkFrame(self.master, fg_color="white")
        self.tabela_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)

        self.tabela_frame.grid_columnconfigure(0, weight=1)  
        self.tabela_frame.grid_rowconfigure(0, weight=1) 
    
    
        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Data de Nascimento", text="Data de Nascimento")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")
        self.tabela.heading("Endereço", text="Endereço")

        self.tabela.grid(row=0, column=0, sticky="nsew")

        self.tabela.tag_configure('evenrow', background='#E8E8E8')  # Cor clara (linhas pares)
        self.tabela.tag_configure('oddrow', background='#FFFFFF')
        
        self.tabela.bind("<Button-3>", self.mostrar_menu_contexto)
        
        scrollbar_y = ttk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tabela.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")  # Posiciona a scrollbar no lado direito da tabela
        
        scrollbar_x = ttk.Scrollbar(self.tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")  # Posiciona a scrollbar abaixo da tabela

        self.tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.atualizar_tabela()
        
    def mostrar_menu_contexto(self, event):
        """Exibe um menu de contexto na linha selecionada."""
        item = self.tabela.identify_row(event.y)
        if item:
            menu = Menu(self.janela, tearoff=0)
            menu.add_command(label="Alterar", command=lambda: self.alterar_paciente(item))
            menu.add_command(label="Excluir", command=lambda: self.excluir_paciente(item))
            menu.post(event.x_root, event.y_root)

    def atualizar_tabela(self, pacientes):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for i, paciente in enumerate(pacientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'  # Define a tag com base no índice (par/ímpar)
            self.tabela.insert("", "end", values=(paciente["nome"], paciente["cpf"], paciente["data_nascimento"], paciente["telefone"], paciente["email"], paciente["endereco"]), tags=(tag,))