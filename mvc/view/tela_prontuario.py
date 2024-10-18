import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os

class TelaProntuario:
    def __init__(self, janela, controller, paciente, prontuario=None):
        self.janela = janela
        self.controller = controller
        self.paciente = paciente
        self.prontuario = prontuario
        self.frame = None
        self.logo_path = os.path.abspath("mvc/imagens/logo.png")
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        self.criar_interface_prontuario()

    def carregar_imagem(self, caminho, tamanho):
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def criar_interface_prontuario(self):
        if self.frame:
            self.frame.destroy()
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.95, relheight=0.95)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure((2, 4, 6, 8), weight=1)

        # Header frame
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)

        # Logo
        self.label_logo = ctk.CTkLabel(header_frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, padx=(0, 20), sticky="w")

        # Título
        titulo = ctk.CTkLabel(header_frame, text=f"Prontuário de {self.paciente.nome}", font=("Arial", 24, "bold"))
        titulo.grid(row=0, column=1, sticky="w")

        # Data de Nascimento
        data_nasc = ctk.CTkLabel(header_frame, text=f"Data de Nascimento: {self.paciente.data_nascimento}", font=("Arial", 16, "bold"))
        data_nasc.grid(row=0, column=2, sticky="e", padx=(0, 20))

        # Histórico
        ctk.CTkLabel(self.frame, text="Histórico Médico:", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", padx=20, pady=(10, 5))
        self.historico = ctk.CTkTextbox(self.frame, height=100)
        self.historico.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.historico.insert("1.0", self.prontuario.historico if self.prontuario else "")

        # Medicações
        ctk.CTkLabel(self.frame, text="Medicações:", font=("Arial", 16, "bold")).grid(row=3, column=0, sticky="w", padx=20, pady=(10, 5))
        self.medicacoes = ctk.CTkTextbox(self.frame, height=100)
        self.medicacoes.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.medicacoes.insert("1.0", self.prontuario.medicacoes if self.prontuario else "")

        # Alergias
        ctk.CTkLabel(self.frame, text="Alergias:", font=("Arial", 16, "bold")).grid(row=5, column=0, sticky="w", padx=20, pady=(10, 5))
        self.alergias = ctk.CTkTextbox(self.frame, height=100)
        self.alergias.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.alergias.insert("1.0", self.prontuario.alergias if self.prontuario else "")

        # Observações
        ctk.CTkLabel(self.frame, text="Observações:", font=("Arial", 16, "bold")).grid(row=7, column=0, sticky="w", padx=20, pady=(10, 5))
        self.observacoes = ctk.CTkTextbox(self.frame, height=100)
        self.observacoes.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.observacoes.insert("1.0", self.prontuario.observacoes if self.prontuario else "")

        # Frame para os botões
        button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        button_frame.grid(row=9, column=0, pady=(20, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Botões
        self.btn_salvar = ctk.CTkButton(button_frame, text="Salvar", command=self.salvar_prontuario, font=("Arial", 16, "bold"), width=150)
        self.btn_salvar.grid(row=0, column=0, padx=(0, 10), sticky="e")

        self.btn_voltar = ctk.CTkButton(button_frame, text="Voltar", command=self.voltar, font=("Arial", 16, "bold"), width=150)
        self.btn_voltar.grid(row=0, column=1, padx=(10, 0), sticky="w")

    def salvar_prontuario(self):
        dados_prontuario = {
            "historico": self.historico.get("1.0", "end-1c"),
            "medicacoes": self.medicacoes.get("1.0", "end-1c"),
            "alergias": self.alergias.get("1.0", "end-1c"),
            "observacoes": self.observacoes.get("1.0", "end-1c")
        }
        self.controller.salvar_prontuario(self.paciente.cpf, dados_prontuario)

    def voltar(self):
        self.frame.destroy()
        self.controller.voltar_tela_medico()

    def mostrar(self):
        self.frame.lift()
        self.janela.update_idletasks()
