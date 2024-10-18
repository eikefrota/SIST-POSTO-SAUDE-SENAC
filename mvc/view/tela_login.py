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
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.35, relheight=0.75)

        # Carregar imagens
        self.logo_image = self.carregar_imagem(self.logo_path, (220, 220))
        self.icon_user = self.carregar_imagem(self.user_icon_path, (35, 35))
        self.icon_password = self.carregar_imagem(self.password_icon_path, (35, 35))

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
        self.label_logo.pack(pady=(40, 30))

        # Campo Usuário (CPF)
        self.criar_campo_entrada("CPF", self.icon_user, "Digite seu CPF", False)

        # Campo Senha
        self.criar_campo_entrada("Senha", self.icon_password, "Digite sua senha", True)

        # Botão de Login
        self.btn_login = ctk.CTkButton(self.frame, text="Login", command=self.verificar_login, width=300, height=50, font=("Arial", 18, "bold"))
        self.btn_login.pack(pady=(40, 20))

    def criar_campo_entrada(self, texto_label, icone, placeholder, show):
        """Cria um campo de entrada completo com label e ícone."""
        frame_campo = ctk.CTkFrame(self.frame, fg_color="transparent")
        frame_campo.pack(pady=(20, 10), padx=20)

        # Label
        label = ctk.CTkLabel(frame_campo, text=texto_label, font=("Arial", 14))
        label.pack(anchor='w', pady=(0, 5))

        # Frame para o ícone e o campo de entrada
        frame_entry = ctk.CTkFrame(frame_campo, fg_color="transparent")
        frame_entry.pack()

        # Ícone
        label_icon = ctk.CTkLabel(frame_entry, image=icone, text="")
        label_icon.pack(side='left', padx=(0, 10))

        # Campo de entrada
        entry = ctk.CTkEntry(frame_entry, placeholder_text=placeholder, width=300, height=45, font=("Montserrat", 16), show="*" if show else "")
        entry.pack(side='left')

        if texto_label == "CPF":
            entry.bind("<KeyRelease>", self.formatar_cpf)
            self.entry_usuario = entry
        else:
            self.entry_senha = entry

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
