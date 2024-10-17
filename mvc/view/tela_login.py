import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

class TelaLogin:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.janela.title("Login")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        # Constantes
        self.logo_path = "mvc/imagens/logo.png"
        self.user_icon_path = "mvc/imagens/user_login.png"
        self.password_icon_path = "mvc/imagens/password_login.png"

        # Criar a interface de login
        self.criar_interface_login()

    def criar_interface_login(self):
        """Limpa a tela e cria os widgets da interface de login."""
        # Limpar a janela atual para trocar de interface
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="#FFFFFF")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.3, relheight=0.6)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Carregar imagens
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        self.icon_user = self.carregar_imagem(self.user_icon_path, (25, 25))
        self.icon_password = self.carregar_imagem(self.password_icon_path, (25, 25))

        # Criar widgets
        self.criar_widgets_login()

    def carregar_imagem(self, caminho, tamanho):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def criar_widgets_login(self):
        """Cria os widgets para a interface de login."""
        # Logo
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="n")

        # Campo Usuário (CPF)
        self.criar_label("CPF", 1)
        self.entry_usuario = self.criar_entry(self.icon_user, 2, "Digite seu CPF", show=False)
        self.entry_usuario.bind("<KeyRelease>", self.formatar_cpf)

        # Campo Senha
        self.criar_label("Senha", 3)
        self.entry_senha = self.criar_entry(self.icon_password, 4, "Digite sua senha", show=True)

        # Botão de Login
        self.btn_login = ctk.CTkButton(self.frame, text="Login", command=self.verificar_login, width=200, font=("Arial", 14, "bold"))
        self.btn_login.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="n")

    def criar_label(self, texto, linha):
        """Cria uma label alinhada com os campos."""
        label = ctk.CTkLabel(self.frame, text=texto, font=("Arial", 12))
        label.grid(row=linha, column=1, padx=10, pady=(10, 0), sticky="w")

    def criar_entry(self, icone, linha, placeholder, show=False):
        """Cria um campo de entrada com ícone."""
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=250, font=("Montserrat", 16), show="*" if show else "")
        entry.grid(row=linha, column=1, padx=10, pady=(0, 20), sticky="w")
        label_icon = ctk.CTkLabel(self.frame, image=icone, text="")
        label_icon.grid(row=linha, column=0, padx=(0, 5), pady=(0, 20), sticky="e")
        return entry

    def formatar_cpf(self, event):
        cpf = self.entry_usuario.get()
        cpf = ''.join(filter(str.isdigit, cpf))
        cpf = cpf[:11]  # Limita a 11 dígitos
        
        cpf_formatado = ''
        for i, digit in enumerate(cpf):
            if i == 3 or i == 6:
                cpf_formatado += '.'
            elif i == 9:
                cpf_formatado += '-'
            cpf_formatado += digit
        
        self.entry_usuario.delete(0, ctk.END)
        self.entry_usuario.insert(0, cpf_formatado)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # Remover a formatação do CPF
        usuario = ''.join(filter(str.isdigit, usuario))

        resultado = self.controller.verificar_login(usuario, senha)
        if resultado:
            self.controller.abrir_painel(resultado.tipo)
        else:
            self.mostrar_erro("Erro de Login", "Credenciais inválidas")
    
    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)
