from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

class SistemaLogin:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Login")
        
        # Constantes
        self.logo_path = "D:/Users/Aluno/Documents/SIS-POS-SAU/file.png"
        self.user_icon_path = "D:/Users/Aluno/Documents/SIS-POS-SAU/user_login.png"
        self.password_icon_path = "D:/Users/Aluno/Documents/SIS-POS-SAU/password_login.png"

        # Simulação de banco de dados de usuários
        self.usuarios = {
            "admin": {"senha": "admin123", "cargo": "Administrador"},
            "medico": {"senha": "medico123", "cargo": "Médico"},
            "recepcionista": {"senha": "recepcao123", "cargo": "Recepcionista"}
        }

        # Criar a interface de login
        self.criar_interface_login()

    def criar_interface_login(self):
        """Limpa a tela e cria os widgets da interface de login."""
        # Limpar a janela atual para trocar de interface
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="#FFFFFF")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.2, relheight=0.5)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        # Carregar imagens
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        self.icon_user = self.carregar_imagem(self.user_icon_path, (25, 25), ctk_image=False)
        self.icon_password = self.carregar_imagem(self.password_icon_path, (25, 25), ctk_image=False)

        # Criar widgets
        self.criar_widgets_login()

    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)


    def retornar_label(self, label_info, linha):
        return self.criar_label(label_info, linha)
    
    def retornar_entry(self, icone, linha, placeholder_inf, show):
        return self.criar_entry(icone, linha, placeholder_inf, show)


    def criar_widgets_login(self):
        """Cria os widgets para a interface de login."""
        # Logo
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="n")

        #Campo Usuário
        self.retornar_label("Usuario", 1)
        self.retornar_entry(self.icon_user, 2, "Digite seu usuário", show=False)

        # Campo Senha
        self.retornar_label("Senha", 3)
        self.retornar_entry(self.icon_password, 4, "Digite sua senha", show=True)

        # Botão de Login
        self.btn_login = ctk.CTkButton(self.frame, text="Login", command=self.verificar_login, width=200, font=("Arial", 14, "bold"))
        self.btn_login.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky="n")
        
        # Botão "Esqueci a Senha"
        self.btn_esqueci_senha = ctk.CTkButton(self.frame, text="Esqueci a Senha", command=self.esqueci_senha, width=150, fg_color="#e23a3b", font=("Arial", 12, "bold"), text_color="white")
        self.btn_esqueci_senha.grid(row=6, column=0, columnspan=2, padx=10, pady=(5, 0))

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
        if not show:
            self.entry_usuario = entry
        else:
            self.entry_senha = entry

    def esqueci_senha(self):
        messagebox.showinfo("Recuperação de Senha", "A opção de recuperação de senha não está implementada.")
    
    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if usuario in self.usuarios and self.usuarios[usuario]["senha"] == senha:
            cargo = self.usuarios[usuario]["cargo"]
            self.abrir_painel(cargo)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def abrir_painel(self, cargo):
        if cargo == "Administrador":
            self.abrir_painel_admin()
        elif cargo == "Médico":
            self.abrir_painel_medico()
        elif cargo == "Recepcionista":
            self.abrir_painel_recepcionista()

    def abrir_painel_admin(self):
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, Administrador!")

    def abrir_painel_medico(self):
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, Médico!")

    def abrir_painel_recepcionista(self):
        messagebox.showinfo("Login bem-sucedido", "Bem-vindo, Recepcionista!")
