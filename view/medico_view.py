import customtkinter as ctk
from tkinter import ttk, messagebox

class MedicoView:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.janela.title("Área do Médico")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        # Criar o frame centralizado
        self.frame = ctk.CTkFrame(self.janela, width=500, height=500, border_width=2)
        self.frame.grid(row=0, column=0, padx=(self.janela.winfo_screenwidth()//2-250), pady=(self.janela.winfo_screenheight()//2-250))
        self.frame.grid_propagate(False)

        # Configuração do layout grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.criar_interface()

        # Tecla de atalho para sair do modo fullscreen
        self.janela.bind("<Escape>", self.sair_tela_cheia)

    def criar_interface(self):
        # Título
        self.label_titulo = ctk.CTkLabel(self.frame, text="Área do Médico", font=("Arial", 20))
        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=20)

        # Botão para exibir consultas
        self.botao_ver_consultas = ctk.CTkButton(self.frame, text="Ver Consultas", command=self.mostrar_consultas)
        self.botao_ver_consultas.grid(row=1, column=0, padx=20, pady=10)

        # Botão para registrar observações
        self.botao_registrar_observacao = ctk.CTkButton(self.frame, text="Registrar Observação", command=self.registrar_observacao)
        self.botao_registrar_observacao.grid(row=1, column=1, padx=20, pady=10)

    def mostrar_consultas(self):
        consultas = self.controller.obter_consultas()

        if not consultas:
            messagebox.showinfo("Informação", "Nenhuma consulta disponível.")
        else:
            self.janela.attributes('-fullscreen', True)  # Colocar em tela cheia
            self.mostrar_tabela_consultas(consultas)

    def mostrar_tabela_consultas(self, consultas):
        # Limpar a tela para mostrar a tabela
        for widget in self.janela.winfo_children(consultas):
            widget.pack_forget()

        # Criar a Tabela (Treeview)
        self.tabela_frame = ctk.CTkFrame(self.janela, fg_color="white")
        self.tabela_frame.grid(row=0, column=0, sticky="nsew")

        # Configurar grid para redimensionar dinamicamente
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)
        self.tabela_frame.grid_columnconfigure(0, weight=1)
        self.tabela_frame.grid_rowconfigure(0, weight=1)

        # Criar a tabela com grid, configurada para expandir conforme a janela é redimensionada
        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold")) # Nomes maiores e negrito

        # Definir as colunas
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Data de Nascimento", text="Data de Nascimento")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")
        self.tabela.heading("Endereço", text="Endereço")

        # Aplicar larguras adaptáveis
        self.tabela.column("Nome", anchor="center", width=200)
        self.tabela.column("CPF", anchor="center", width=150)
        self.tabela.column("Data de Nascimento", anchor="center", width=150)
        self.tabela.column("Telefone", anchor="center", width=150)
        self.tabela.column("Email", anchor="center", width=200)
        self.tabela.column("Endereço", anchor="center", width=250)

        # Tags para linhas alternadas
        self.tabela.tag_configure('evenrow', background='#E8E8E8')
        self.tabela.tag_configure('oddrow', background='#FFFFFF')

        # Adicionar botões de contexto para exclusão e alteração
        self.tabela.bind("<Button-3>", self.mostrar_menu_contexto)

        # Usar grid para a tabela, ocupando toda a área disponível
        self.tabela.grid(row=0, column=0, sticky="nsew")

        # Scrollbars para caso a tabela tenha muitos itens
        scrollbar_y = ttk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tabela.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        scrollbar_x = ttk.Scrollbar(self.tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Atualiza a tabela
        self.atualizar_tabela()

        # Botão para voltar à tela anterior
        self.botao_voltar = ctk.CTkButton(self.tabela_frame, text="Voltar", command=self.voltar_tela_anterior)
        self.botao_voltar.grid(row=2, column=0, columnspan=2, pady=10)

    def sair_tela_cheia(self, event=None):
        self.janela.attributes('-fullscreen', False)

    def voltar_tela_anterior(self):
        self.sair_tela_cheia()  # Sair do modo tela cheia
        for widget in self.janela.winfo_children():
            widget.pack_forget()  # Esconder widgets da tabela
        self.criar_interface()  # Voltar para a interface inicial

    def registrar_observacao(self):
        # Janela para registrar observações
        self.janela_observacao = ctk.CTkToplevel(self.janela)
        self.janela_observacao.title("Registrar Observação")
        self.janela_observacao.geometry("400x300")

        self.label_consulta = ctk.CTkLabel(self.janela_observacao, text="Consulta (Digite o índice):")
        self.label_consulta.pack(pady=5)

        self.entry_consulta = ctk.CTkEntry(self.janela_observacao)
        self.entry_consulta.pack(pady=5)

        self.label_observacao = ctk.CTkLabel(self.janela_observacao, text="Observações:")
        self.label_observacao.pack(pady=5)

        self.entry_observacao = ctk.CTkEntry(self.janela_observacao)
        self.entry_observacao.pack(pady=5)

        self.botao_salvar = ctk.CTkButton(self.janela_observacao, text="Salvar", command=self.salvar_observacao)
        self.botao_salvar.pack(pady=10)

    def salvar_observacao(self):
        try:
            idx_consulta = int(self.entry_consulta.get())
            observacao = self.entry_observacao.get()

            if not observacao:
                messagebox.showerror("Erro", "Observação não pode estar vazia.")
                return

            consultas = self.controller.obter_consultas()

            if 0 <= idx_consulta < len(consultas):
                consulta = consultas[idx_consulta]
                self.controller.registrar_observacao(consulta, observacao)
                messagebox.showinfo("Sucesso", "Observação registrada com sucesso!")
                self.janela_observacao.destroy()
            else:
                messagebox.showerror("Erro", "Consulta não encontrada.")
        except ValueError:
            messagebox.showerror("Erro", "Índice inválido.")
