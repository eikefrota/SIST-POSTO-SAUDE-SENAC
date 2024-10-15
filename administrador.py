import customtkinter as ctk
from PIL import Image, ImageTk

class TelaAdministrador:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Administrador")

        # Configurar a janela para ocupar toda a tela, como no código 02
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        # Constantes
        self.logo_path = "imagens/logo.png"
        self.cor_botoes = "#007ACC"
        self.cor_texto_bemvindo = "#005a99"

        # Criar a interface centralizada
        self.criar_interface_centralizada()

    def criar_interface_centralizada(self):
        """Limpa a tela e cria os widgets da interface centralizada."""
        # Limpar a janela atual para trocar de interface
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="#FFFFFF")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.2, relheight=0.5)

        # Configuração do grid para centralização
        self.frame.grid_rowconfigure(0, weight=1)  # Linha superior expansível
        self.frame.grid_rowconfigure(1, weight=1)  # Linha com a imagem
        self.frame.grid_rowconfigure(2, weight=1)  # Linha com o texto de boas-vindas
        self.frame.grid_rowconfigure(3, weight=1)  # Linha com o primeiro botão
        self.frame.grid_rowconfigure(4, weight=1)  # Linha com o segundo botão
        self.frame.grid_rowconfigure(5, weight=1)  # Linha inferior expansível
        self.frame.grid_columnconfigure(0, weight=1)  # Coluna única centralizada

        # Carregar imagens
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))

        # Criar widgets
        self.criar_widgets()

    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)

    def criar_widgets(self):
        """Cria os widgets centrais."""
        # Logo
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, pady=(10, 5), sticky="nsew", padx=20)

        # Texto de boas-vindas
        self.label_bemvindo = ctk.CTkLabel(
            self.frame, 
            text="Bem-vindo, Administrador!", 
            font=("Arial", 24, "bold"), 
            text_color=self.cor_texto_bemvindo
        )
        self.label_bemvindo.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="nsew")

        # Botão "Cadastrar Médico"
        self.btn_cadastrar_medico = ctk.CTkButton(
            self.frame, text="Cadastrar Médico", width=150, font=("Arial", 14, "bold"), fg_color=self.cor_botoes
        )
        self.btn_cadastrar_medico.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        
        # Botão "Cadastrar Recepcionista"
        self.btn_cadastrar_recepcionista = ctk.CTkButton(
            self.frame, text="Cadastrar Recepcionista", width=150, font=("Arial", 14, "bold"), fg_color=self.cor_botoes
        )
        self.btn_cadastrar_recepcionista.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")
