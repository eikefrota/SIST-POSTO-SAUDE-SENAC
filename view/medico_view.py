import customtkinter as ctk
from tkinter import ttk, messagebox

# import customtkinter as ctk
# from controllers import cadastrar_prontuario, editar_prontuario, visualizar_prontuario, ver_pacientes
# from tkinter import messagebox

# class SistemaHospitalarApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Sistema de Cadastro Hospitalar")
#         self.master.geometry("600x400")
        
#         self.frame_pacientes = ctk.CTkFrame(self.master)
#         self.frame_pacientes.pack(pady=20, padx=20, fill="both", expand=True)

#         self.btn_ver_pacientes = ctk.CTkButton(self.master, text="Ver Pacientes", command=self.mostrar_pacientes)
#         self.btn_ver_pacientes.pack(pady=20)

#     def mostrar_pacientes(self):
#         # Limpa o frame antes de mostrar a lista de pacientes
#         for widget in self.frame_pacientes.winfo_children():
#             widget.destroy()

#         pacientes = ver_pacientes()
#         for paciente in pacientes:
#             label = ctk.CTkLabel(self.frame_pacientes, text=f"{paciente.nome} ({paciente.idade} anos)")
#             label.pack(pady=5)
            
#             btn_cadastrar = ctk.CTkButton(self.frame_pacientes, text="Cadastrar Prontuário", command=lambda p=paciente: self.abrir_tela_cadastro(p.id))
#             btn_cadastrar.pack(pady=5)

#             if paciente.prontuarios:
#                 btn_visualizar = ctk.CTkButton(self.frame_pacientes, text="Ver Prontuário", command=lambda p=paciente: self.abrir_tela_visualizacao(p.prontuarios[0].id))
#                 btn_visualizar.pack(pady=5)

#     def abrir_tela_cadastro(self, paciente_id):
#         janela_cadastro = ctk.CTkToplevel(self.master)
#         janela_cadastro.title("Cadastrar Prontuário")
#         janela_cadastro.geometry("400x300")

#         label = ctk.CTkLabel(janela_cadastro, text="Descrição do Prontuário")
#         label.pack(pady=10)

#         prontuario_entry = ctk.CTkEntry(janela_cadastro, width=300, height=100)
#         prontuario_entry.pack(pady=10)

#         def cadastrar():
#             descricao = prontuario_entry.get()
#             if descricao:
#                 cadastrar_prontuario(paciente_id, descricao)
#                 messagebox.showinfo("Sucesso", "Prontuário cadastrado com sucesso!")
#                 janela_cadastro.destroy()
#             else:
#                 messagebox.showerror("Erro", "Descrição não pode ser vazia")

#         btn_cadastrar = ctk.CTkButton(janela_cadastro, text="Cadastrar", command=cadastrar)
#         btn_cadastrar.pack(pady=10)

#     def abrir_tela_visualizacao(self, prontuario_id):
#         prontuario = visualizar_prontuario(prontuario_id)

#         janela_visualizacao = ctk.CTkToplevel(self.master)
#         janela_visualizacao.title("Visualizar Prontuário")
#         janela_visualizacao.geometry("400x300")

#         label = ctk.CTkLabel(janela_visualizacao, text="Descrição do Prontuário:")
#         label.pack(pady=10)

#         prontuario_label = ctk.CTkLabel(janela_visualizacao, text=prontuario.descricao)
#         prontuario_label.pack(pady=10)

#         btn_editar = ctk.CTkButton(janela_visualizacao, text="Editar Prontuário", command=lambda: self.abrir_tela_editar(prontuario.id))
#         btn_editar.pack(pady=10)

#     def abrir_tela_editar(self, prontuario_id):
#         prontuario = visualizar_prontuario(prontuario_id)

#         janela_editar = ctk.CTkToplevel(self.master)
#         janela_editar.title("Editar Prontuário")
#         janela_editar.geometry("400x300")

#         label = ctk.CTkLabel(janela_editar, text="Descrição do Prontuário")
#         label.pack(pady=10)

#         prontuario_entry = ctk.CTkEntry(janela_editar, width=300, height=100)
#         prontuario_entry.insert(0, prontuario.descricao)
#         prontuario_entry.pack(pady=10)

#         def editar():
#             nova_descricao = prontuario_entry.get()
#             if nova_descricao:
#                 editar_prontuario(prontuario_id, nova_descricao)
#                 messagebox.showinfo("Sucesso", "Prontuário editado com sucesso!")
#                 janela_editar.destroy()
#             else:
#                 messagebox.showerror("Erro", "Descrição não pode ser vazia")

#         btn_salvar = ctk.CTkButton(janela_editar, text="Salvar", command=editar)
#         btn_salvar.pack(pady=10)

# if __name__ == "__main__":
#     app = ctk.CTk()
#     SistemaHospitalarApp(app)
#     app.mainloop()

class MedicoView:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.janela.title("Área do Médico")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        
        # Criar o frame centralizado
        self.frame = ctk.CTkFrame(self.janela, width=500, height=500, border_width=2, fg_color='white', border_color='#00CED1')
        self.frame.grid(row=0, column=0, padx=(self.janela.winfo_screenwidth()//2-250), pady=(self.janela.winfo_screenheight()//2-250))
        self.frame.grid_propagate(False)
        self.frame_nome = ctk.CTkFrame(self.frame, width=600,  height=50, border_width=500, fg_color='#00CED1',  border_color='#00CED1')
        self.frame_nome.grid(row=0, column=0, columnspan=2, padx=0, pady=0)
        self.frame.grid_propagate(False)


        # Configuração do layout grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.criar_interface()
        
    def criar_interface(self):
        # Botão para exibir consultas
        self.botao_ver_consultas = ctk.CTkButton(self.frame, text="Ver Consultas", command=self.mostrar_consultas, width=70, height=50)
        self.botao_ver_consultas.grid(row=3, column=0, padx=0, pady=100)

        # Botão para registrar observações
        self.botao_registrar_observacao = ctk.CTkButton(self.frame, text="Registrar Observação", command=self.registrar_observacao, width=50, height=50)
        self.botao_registrar_observacao.grid(row=3, column=1, padx=0, pady=100)
        




    def mostrar_consultas(self):
        consultas = self.controller.obter_consultas()

        if not consultas:
            messagebox.showinfo("Informação", "Nenhuma consulta disponível.")
        else:
            self.janela.attributes('-fullscreen', True)  # Colocar em tela cheia
            self.mostrar_tabela_consultas(consultas)

    def mostrar_tabela_consultas(self, consultas):
        # Limpar a tela para mostrar a tabela
        for widget in self.janela.winfo_children(self.janela):
            widget.pack_forget()

        # Criar a Tabela (Treeview)
        self.tabela_frame = ctk.CTkFrame(self.janela, fg_color="white")
        self.tabela_frame.grid(row=0, column=0, sticky="nsew")

        self.tabela_frame.grid_columnconfigure(0, weight=1)
        self.tabela_frame.grid_rowconfigure(0, weight=1)

        # Criar a tabela com grid, configurada para expandir conforme a janela é redimensionada
        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 9, "bold")) # Nomes maiores e negrito

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



        # Usar grid para a tabela, ocupando toda a área disponível
        self.tabela.grid(row=0, column=0, sticky="nsew")




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
        for widget in self.janela.winfo_children():
            widget.pack_forget()
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
