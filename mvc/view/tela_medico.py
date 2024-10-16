import customtkinter as ctk

class MedicoInterface(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.pack(fill=ctk.BOTH, expand=True)
        
        # Configuração do layout principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame_principal.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.7, relheight=0.9)
        
        # Configuração do grid dentro do frame
        self.frame_principal.grid_columnconfigure(1, weight=1)
        
        # Widgets da interface
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        self.label_titulo = ctk.CTkLabel(self.frame_principal, text="Prontuário Médico", font=("Arial", 24, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=20)

        # Nome do paciente
        self.label_nome = ctk.CTkLabel(self.frame_principal, text="Nome do Paciente:", font=("Arial", 14))
        self.label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_nome = ctk.CTkEntry(self.frame_principal, width=300)
        self.entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Idade do paciente
        self.label_idade = ctk.CTkLabel(self.frame_principal, text="Idade:", font=("Arial", 14))
        self.label_idade.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entry_idade = ctk.CTkEntry(self.frame_principal, width=100)
        self.entry_idade.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Sintomas
        self.label_sintomas = ctk.CTkLabel(self.frame_principal, text="Sintomas:", font=("Arial", 14))
        self.label_sintomas.grid(row=3, column=0, padx=10, pady=5, sticky="ne")
        self.entry_sintomas = ctk.CTkTextbox(self.frame_principal, width=300, height=100)
        self.entry_sintomas.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Diagnóstico
        self.label_diagnostico = ctk.CTkLabel(self.frame_principal, text="Diagnóstico:", font=("Arial", 14))
        self.label_diagnostico.grid(row=4, column=0, padx=10, pady=5, sticky="ne")
        self.entry_diagnostico = ctk.CTkTextbox(self.frame_principal, width=300, height=100)
        self.entry_diagnostico.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self.frame_principal, text="Salvar Prontuário", command=self.salvar_prontuario)
        self.btn_salvar.grid(row=5, column=0, columnspan=2, pady=20)

        # Status
        self.label_status = ctk.CTkLabel(self.frame_principal, text="", font=("Arial", 12))
        self.label_status.grid(row=6, column=0, columnspan=2, pady=10)

        # Botão Listar Prontuários
        self.btn_listar = ctk.CTkButton(self.frame_principal, text="Listar Prontuários", command=self.listar_prontuarios)
        self.btn_listar.grid(row=7, column=0, columnspan=2, pady=10)

        # Área para exibir prontuários
        self.txt_prontuarios = ctk.CTkTextbox(self.frame_principal, width=500, height=200)
        self.txt_prontuarios.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.btn_sair = ctk.CTkButton(self.frame_principal, text="Sair", command=self.fazer_logout)
        self.btn_sair.grid(row=9, column=0, columnspan=2, pady=10)

    def salvar_prontuario(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        sintomas = self.entry_sintomas.get("1.0", "end-1c")
        diagnostico = self.entry_diagnostico.get("1.0", "end-1c")
        
        if nome and idade and sintomas and diagnostico:
            self.controller.salvar_prontuario(nome, idade, sintomas, diagnostico)
            self.label_status.configure(text="Prontuário salvo com sucesso!", text_color="green")
            self.limpar_campos()
        else:
            self.label_status.configure(text="Por favor, preencha todos os campos!", text_color="red")

    def listar_prontuarios(self):
        self.txt_prontuarios.delete("1.0", ctk.END)
        prontuarios = self.controller.listar_prontuarios()
        if prontuarios:
            for prontuario in prontuarios:
                self.txt_prontuarios.insert(ctk.END, f"ID: {prontuario.id}\nNome: {prontuario.nome}\nIdade: {prontuario.idade}\nSintomas: {prontuario.sintomas}\nDiagnóstico: {prontuario.diagnostico}\n\n")
        else:
            self.txt_prontuarios.insert(ctk.END, "Nenhum prontuário encontrado.")

    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_idade.delete(0, ctk.END)
        self.entry_sintomas.delete("1.0", ctk.END)
        self.entry_diagnostico.delete("1.0", ctk.END)


    def fazer_logout(self):
        if self.controller.confirmar_acao("Confirmar Logout", "Tem certeza que deseja sair?"):
            self.controller.fazer_logout()