import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import datetime

class TelaMedico:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.frame = None
        self.configurar_janela()
        self.logo_path = os.path.abspath("mvc/imagens/logo.png")
        self.logo_image = self.carregar_imagem(self.logo_path, (100, 100))

    def configurar_janela(self):
        self.janela.title("Painel do Médico")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        self.janela.resizable(True, True)

    def carregar_imagem(self, caminho, tamanho):
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def criar_interface_medico(self):
        if self.frame:
            self.frame.destroy()
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure((1, 2, 3), weight=1)

        # Header com logo e título
        self.criar_header()

        # Campo de pesquisa
        self.criar_campo_pesquisa()

        # Tabela de pacientes
        self.criar_tabela_pacientes()

        # Botões Atender e Voltar
        self.criar_botoes_acoes()

    def criar_header(self):
        header_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        # Logo
        self.label_logo = ctk.CTkLabel(header_frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, padx=(0, 20), sticky="w")

        # Título
        self.label_titulo = ctk.CTkLabel(header_frame, text="Painel do Médico", font=("Montserrat", 24, "bold"))
        self.label_titulo.grid(row=0, column=1, sticky="w")

    def criar_campo_pesquisa(self):
        frame_pesquisa = ctk.CTkFrame(self.frame, fg_color="transparent")
        frame_pesquisa.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.entry_pesquisa = ctk.CTkEntry(frame_pesquisa, placeholder_text="Pesquisar paciente", width=300, height=40, font=("Arial", 14))
        self.entry_pesquisa.pack(side="left", padx=(0, 10))

        self.botao_pesquisar = ctk.CTkButton(frame_pesquisa, text="Pesquisar", font=("Arial", 14, "bold"), width=100, height=40, command=self.pesquisar_paciente)
        self.botao_pesquisar.pack(side="left")

    def criar_tabela_pacientes(self):
        frame_tabela = ctk.CTkFrame(self.frame, fg_color="transparent")
        frame_tabela.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        frame_tabela.grid_columnconfigure(0, weight=1)
        frame_tabela.grid_rowconfigure(0, weight=1)

        colunas = ('ID', 'Nome', 'CPF', 'Data', 'Hora', 'Status')
        self.tabela_pacientes = ttk.Treeview(frame_tabela, columns=colunas, show='headings')

        # Configurar estilo para a tabela
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', '#347083')])
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

        for col in colunas:
            self.tabela_pacientes.heading(col, text=col, anchor='center')
            self.tabela_pacientes.column(col, width=100, anchor='center')

        self.tabela_pacientes.column('ID', width=50)

        self.tabela_pacientes.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tabela_pacientes.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabela_pacientes.configure(yscrollcommand=scrollbar.set)

        # Configurar tags para alternar cores das linhas
        self.tabela_pacientes.tag_configure('oddrow', background="white")
        self.tabela_pacientes.tag_configure('evenrow', background="#f0f0f0")

    def criar_botoes_acoes(self):
        frame_botoes = ctk.CTkFrame(self.frame, fg_color="transparent")
        frame_botoes.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1), weight=1)

        self.botao_atender = ctk.CTkButton(frame_botoes, text="Atender", font=("Arial", 16, "bold"), width=150, height=40, command=self.atender_paciente)
        self.botao_atender.grid(row=0, column=0, padx=(0, 10))

        self.botao_voltar = ctk.CTkButton(frame_botoes, text="Voltar", font=("Arial", 16, "bold"), width=150, height=40, command=self.confirmar_logout)
        self.botao_voltar.grid(row=0, column=1, padx=(10, 0))

    def pesquisar_paciente(self):
        termo_pesquisa = self.entry_pesquisa.get().strip()
        if termo_pesquisa:
            resultados = self.controller.pesquisar_pacientes(termo_pesquisa)
            self.atualizar_tabela_pacientes(resultados)
            if not resultados:
                self.controller.mostrar_erro("Pesquisa", "Nenhum paciente encontrado com o termo informado.")
        else:
            self.controller.mostrar_erro("Erro", "Por favor, insira um termo de pesquisa.")

    def atualizar_tabela_pacientes(self, pacientes):
        self.tabela_pacientes.delete(*self.tabela_pacientes.get_children())
        for i, paciente in enumerate(pacientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tabela_pacientes.insert('', 'end', values=(
                paciente['id'],
                paciente['nome'],
                paciente['cpf'],
                paciente['data'],
                paciente['hora'],
                paciente['status']
            ), tags=(tag,))

    def atender_paciente(self):
        selecao = self.tabela_pacientes.selection()
        if selecao:
            item = self.tabela_pacientes.item(selecao[0])
            paciente = item['values']
            consulta_id = paciente[0]  # O ID da consulta é o primeiro item
            self.controller.atender_paciente(consulta_id)
        else:
            self.controller.mostrar_erro("Erro", "Por favor, selecione um paciente para atender.")

    def confirmar_logout(self):
        if self.controller.confirmar_acao("Confirmar Logout", "Deseja realmente fazer logout?"):
            self.controller.fazer_logout()

    def mostrar(self):
        if self.frame is None or not self.frame.winfo_exists():
            self.criar_interface_medico()
        self.janela.update_idletasks()
        consultas = self.controller.listar_consultas_do_dia()
        self.atualizar_tabela_pacientes(consultas)

    def esconder(self):
        if self.frame and self.frame.winfo_exists():
            self.frame.place_forget()
