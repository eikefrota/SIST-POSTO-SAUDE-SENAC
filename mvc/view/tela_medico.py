import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image
import os

class TelaMedico:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.frame = None
        self.tabela = None
        self.configurar_janela()
        self.logo_path = os.path.abspath("mvc/imagens/logo.png")
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))

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

        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.criar_widgets_medico()

    def criar_widgets_medico(self):
        self.criar_logo()
        self.criar_titulo("Painel do Médico")

        self.criar_label("Pesquisar Paciente:", 1, 0, sticky="e")
        self.entry_pesquisa = ctk.CTkEntry(self.frame, width=300, height=30, font=("Arial", 14))
        self.entry_pesquisa.grid(row=1, column=1, padx=(20, 0), pady=(10, 5), sticky="w")
        self.botao_pesquisar = ctk.CTkButton(self.frame, text="Pesquisar", font=("Arial", 14, "bold"), width=100, height=30, command=self.pesquisar_paciente)
        self.botao_pesquisar.grid(row=1, column=2, padx=(10, 0), pady=(10, 5), sticky="w")

        self.criar_tabela_pacientes()

        self.botao_atender = ctk.CTkButton(self.frame, text="Atender Paciente", font=("Arial", 16, "bold"), width=200, height=40, command=self.atender_paciente)
        self.botao_atender.grid(row=4, column=0, columnspan=2, pady=10)

        self.botao_voltar = ctk.CTkButton(self.frame, text="Voltar", font=("Arial", 16, "bold"), width=200, height=40, command=self.voltar)
        self.botao_voltar.grid(row=4, column=2, columnspan=2, pady=10)

    def criar_logo(self):
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=0, column=0, padx=(20, 0), pady=(10, 5), sticky="w")

    def criar_titulo(self, texto):
        self.label_titulo = ctk.CTkLabel(self.frame, text=texto, font=("Montserrat", 24, "bold"))
        self.label_titulo.grid(row=0, column=1, columnspan=3, padx=(20, 0), pady=(10, 5), sticky="w")

    def criar_label(self, texto, linha, coluna, sticky="w"):
        label = ctk.CTkLabel(self.frame, text=texto, font=("Arial", 16, "bold"))
        label.grid(row=linha, column=coluna, padx=(30, 10), pady=(0, 0), sticky=sticky)
        return label

    def criar_tabela_pacientes(self):
        colunas = ('ID', 'Nome', 'CPF', 'Data', 'Hora', 'Status')
        self.tabela = ttk.Treeview(self.frame, columns=colunas, show='headings')

        for col in colunas:
            self.tabela.heading(col, text=col)
            self.tabela.column(col, width=150, anchor='center')

        self.tabela.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tabela.yview)
        scrollbar.grid(row=2, column=4, sticky='ns')
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.tabela.bind("<Double-1>", self.on_paciente_select)

    def atualizar_tabela_pacientes(self, pacientes):
        self.tabela.delete(*self.tabela.get_children())
        for paciente in pacientes:
            if paciente['status'] != 'Atendido':
                self.tabela.insert('', 'end', values=(
                    paciente['id'],
                    paciente['nome'],
                    paciente['cpf'],
                    paciente['data'],
                    paciente['hora'],
                    paciente['status']
                ))

    def pesquisar_paciente(self):
        termo_pesquisa = self.entry_pesquisa.get().strip()
        pacientes_filtrados = self.controller.pesquisar_pacientes(termo_pesquisa)
        self.atualizar_tabela_pacientes(pacientes_filtrados)

    def on_paciente_select(self, event):
        item = self.tabela.selection()[0]
        paciente = self.tabela.item(item, "values")
        self.controller.selecionar_paciente(paciente)

    def atender_paciente(self):
        item = self.tabela.selection()
        if item:
            paciente = self.tabela.item(item[0], "values")
            self.controller.abrir_tela_prontuario(paciente[2])  # Passando o CPF do paciente
        else:
            messagebox.showerror("Erro", "Selecione um paciente para atender.")

    def voltar(self):
        self.controller.main_controller.voltar_para_tela_principal()

    def mostrar(self):
        print("Chamando mostrar() na TelaMedico")
        if self.frame is None or not self.frame.winfo_exists():
            print("Criando nova interface médico")
            self.criar_interface_medico()
        else:
            print("Atualizando interface existente")
            self.frame.lift()
        self.janela.update_idletasks()
        print("Atualizando tabela de pacientes")
        self.atualizar_tabela_pacientes(self.controller.listar_consultas_do_dia())

    def esconder(self):
        if self.frame and self.frame.winfo_exists():
            self.frame.place_forget()

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def destruir(self):
        if self.frame and self.frame.winfo_exists():
            self.frame.destroy()
        self.frame = None
        self.tabela = None
