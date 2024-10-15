import customtkinter as ctk
from tkinter import ttk, messagebox

class TelaAdmin:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.janela.title("Painel do Administrador")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        self.criar_interface_admin()

    def criar_interface_admin(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.frame = ctk.CTkFrame(self.janela)
        self.frame.pack(fill=ctk.BOTH, expand=True)

        # Título
        titulo = ctk.CTkLabel(self.frame, text="Painel do Administrador", font=("Arial", 24, "bold"))
        titulo.pack(pady=20)

        # Botões
        btn_adicionar_medico = ctk.CTkButton(self.frame, text="Adicionar Médico", command=self.mostrar_form_medico)
        btn_adicionar_medico.pack(pady=10)

        btn_adicionar_recepcionista = ctk.CTkButton(self.frame, text="Adicionar Recepcionista", command=self.mostrar_form_recepcionista)
        btn_adicionar_recepcionista.pack(pady=10)

        btn_listar_profissionais = ctk.CTkButton(self.frame, text="Listar Profissionais", command=self.listar_profissionais)
        btn_listar_profissionais.pack(pady=10)

        btn_sair = ctk.CTkButton(self.frame, text="Sair", command=self.controller.voltar_para_login)
        btn_sair.pack(pady=10)

    def mostrar_form_medico(self):
        self.mostrar_formulario("Médico")

    def mostrar_form_recepcionista(self):
        self.mostrar_formulario("Recepcionista")

    def mostrar_formulario(self, tipo_profissional):
        janela_form = ctk.CTkToplevel(self.janela)
        janela_form.title(f"Adicionar {tipo_profissional}")
        janela_form.geometry("400x300")

        frame = ctk.CTkFrame(janela_form)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text=f"Adicionar {tipo_profissional}", font=("Arial", 18, "bold")).pack(pady=10)

        ctk.CTkLabel(frame, text="Nome:").pack(anchor="w")
        entry_nome = ctk.CTkEntry(frame)
        entry_nome.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(frame, text="CPF:").pack(anchor="w")
        entry_cpf = ctk.CTkEntry(frame)
        entry_cpf.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(frame, text="Senha:").pack(anchor="w")
        entry_senha = ctk.CTkEntry(frame, show="*")
        entry_senha.pack(fill="x", padx=5, pady=5)

        if tipo_profissional == "Médico":
            ctk.CTkLabel(frame, text="CRM:").pack(anchor="w")
            entry_crm = ctk.CTkEntry(frame)
            entry_crm.pack(fill="x", padx=5, pady=5)

        btn_adicionar = ctk.CTkButton(frame, text="Adicionar", command=lambda: self.adicionar_profissional(
            tipo_profissional,
            entry_nome.get(),
            entry_cpf.get(),
            entry_senha.get(),
            entry_crm.get() if tipo_profissional == "Médico" else None
        ))
        btn_adicionar.pack(pady=10)

    def adicionar_profissional(self, tipo, nome, cpf, senha, crm=None):
        if tipo == "Médico":
            resultado = self.controller.adicionar_medico(nome, cpf, senha, crm)
        else:
            resultado = self.controller.adicionar_recepcionista(nome, cpf, senha)

        if resultado:
            messagebox.showinfo("Sucesso", f"{tipo} adicionado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Não foi possível adicionar o {tipo}.")

    def listar_profissionais(self):
        janela_lista = ctk.CTkToplevel(self.janela)
        janela_lista.title("Lista de Profissionais")
        janela_lista.geometry("600x400")

        frame = ctk.CTkFrame(janela_lista)
        frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Lista de Profissionais", font=("Arial", 18, "bold")).pack(pady=10)

        tree = ttk.Treeview(frame, columns=("Nome", "CPF", "Tipo"), show="headings")
        tree.heading("Nome", text="Nome")
        tree.heading("CPF", text="CPF")
        tree.heading("Tipo", text="Tipo")
        tree.pack(fill=ctk.BOTH, expand=True)

        profissionais = self.controller.listar_profissionais()
        for prof in profissionais:
            tree.insert("", "end", values=(prof["nome"], prof["cpf"], prof["tipo"]))

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)