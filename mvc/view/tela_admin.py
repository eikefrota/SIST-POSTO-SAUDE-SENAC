import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

class TelaAdmin:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.janela.title("Painel do Administrador")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        self.logo_path = os.path.abspath("C:/Users/Clean Vision/OneDrive/Área de Trabalho/logo/logo.png")
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        self.criar_interface_admin()

    def carregar_imagem(self, caminho, tamanho):
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def criar_interface_admin(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.frame_admin = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame_admin.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.6)

        self.frame_admin.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_admin.grid_rowconfigure((1, 10), weight=1)

        self.criar_logo(self.frame_admin)
        self.criar_titulo("Área do Administrador", self.frame_admin)

        self.botao_adicionar_medico = self.criar_botao("Adicionar Médico", self.mostrar_form_medico, 3, 1)
        self.botao_adicionar_recepcionista = self.criar_botao("Adicionar Recepcionista", self.mostrar_form_recepcionista, 3, 2)
        self.botao_listar_profissionais = self.criar_botao("Listar Profissionais", self.listar_profissionais, 4, 1)
        self.botao_sair = self.criar_botao("Sair", self.fazer_logout, 5, 1, 2)

        self.janela.update()

    def criar_logo(self, frame):
        self.label_logo = ctk.CTkLabel(frame, image=self.logo_image, text="")
        self.label_logo.grid(row=1, column=1, padx=(0, 20), pady=(10, 5), sticky="w")

    def criar_titulo(self, texto, frame):
        self.label_titulo = ctk.CTkLabel(frame, text=texto, font=("Montserrat", 20, "bold"))
        self.label_titulo.grid(row=1, column=1, padx=(20, 0), pady=(10, 5), sticky="e")

    def criar_botao(self, texto, comando, linha, coluna, colspan=1):
        botao = ctk.CTkButton(self.frame_admin, text=texto, font=("Arial", 18, "bold"), width=200, height=40, command=comando)
        botao.grid(row=linha, column=coluna, columnspan=colspan, padx=20, pady=20, sticky="ew")
        return botao

    def mostrar_form_medico(self):
        self.mostrar_formulario("Médico")

    def mostrar_form_recepcionista(self):
        self.mostrar_formulario("Recepcionista")

    def mostrar_formulario(self, tipo_profissional):
        janela_form = ctk.CTkToplevel(self.janela)
        janela_form.title(f"Adicionar {tipo_profissional}")
        janela_form.geometry("400x300")
        janela_form.transient(self.janela)
        janela_form.grab_set()

        frame = ctk.CTkFrame(janela_form)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=f"Adicionar {tipo_profissional}", font=("Arial", 18, "bold")).pack(pady=10)

        entries = {}
        for campo in ["Nome", "CPF", "Senha"]:
            ctk.CTkLabel(frame, text=f"{campo}:").pack(anchor="w")
            entries[campo.lower()] = ctk.CTkEntry(frame)
            entries[campo.lower()].pack(fill="x", padx=5, pady=5)

        if tipo_profissional == "Médico":
            ctk.CTkLabel(frame, text="CRM:").pack(anchor="w")
            entries['crm'] = ctk.CTkEntry(frame)
            entries['crm'].pack(fill="x", padx=5, pady=5)

        btn_adicionar = ctk.CTkButton(frame, text="Adicionar", command=lambda: self.adicionar_profissional(
            tipo_profissional,
            entries['nome'].get(),
            entries['cpf'].get(),
            entries['senha'].get(),
            entries.get('crm', ctk.CTkEntry(frame)).get(),
            janela_form
        ))
        btn_adicionar.pack(pady=10)

    def adicionar_profissional(self, tipo, nome, cpf, senha, crm, janela_form):
        if tipo == "Médico":
            resultado = self.controller.adicionar_medico(nome, cpf, senha, crm)
        else:
            resultado = self.controller.adicionar_recepcionista(nome, cpf, senha)

        if resultado:
            self.mostrar_mensagem("Sucesso", f"{tipo} adicionado com sucesso!")
            janela_form.destroy()
            self.criar_interface_admin()
        else:
            self.mostrar_erro("Erro", f"Não foi possível adicionar o {tipo}.")

    def listar_profissionais(self):
        janela_lista = ctk.CTkToplevel(self.janela)
        janela_lista.title("Lista de Profissionais")
        janela_lista.geometry("600x400")
        janela_lista.transient(self.janela)
        janela_lista.grab_set()

        frame = ctk.CTkFrame(janela_lista)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Lista de Profissionais", font=("Arial", 18, "bold")).pack(pady=10)

        tree = ttk.Treeview(frame, columns=("Nome", "CPF", "Tipo"), show="headings")
        for col in ("Nome", "CPF", "Tipo"):
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill=ctk.BOTH, expand=True)

        profissionais = self.controller.listar_profissionais()
        for prof in profissionais:
            tree.insert("", "end", values=(prof["nome"], prof["cpf"], prof["tipo"]))

    def fazer_logout(self):
        if self.controller.confirmar_acao("Confirmar Logout", "Tem certeza que deseja sair?"):
            self.controller.fazer_logout()

    def confirmar_acao(self, titulo, mensagem):
        return messagebox.askyesno(titulo, mensagem)

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)
