import customtkinter as ctk
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/senac"
# Criando a conexão com o banco de dados
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Definindo o modelo do prontuário
class Prontuario(Base):
    __tablename__ = 'prontuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    sintomas = Column(Text, nullable=False)
    diagnostico = Column(Text, nullable=False)

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

# Criar a classe de sessão
Session = sessionmaker(bind=engine)
session = Session()

# Classe para a interface do médico
class MedicoInterface(ctk.CTk):
    def __init__(self):
        # Inicializa a classe CTk
        ctk.CTk.__init__(self)  # Corrigido para garantir que a classe pai seja inicializada
        self.title("Interface Médica")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        
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
        # Labels e Entradas para os dados do paciente
        self.label_nome = ctk.CTkLabel(self.frame_principal, text="Nome do Paciente:")
        self.label_nome.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_nome = ctk.CTkEntry(self.frame_principal)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.label_idade = ctk.CTkLabel(self.frame_principal, text="Idade:")
        self.label_idade.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_idade = ctk.CTkEntry(self.frame_principal)
        self.entry_idade.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        self.label_sintomas = ctk.CTkLabel(self.frame_principal, text="Sintomas:")
        self.label_sintomas.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        
        self.entry_sintomas = ctk.CTkTextbox(self.frame_principal, height=70)
        self.entry_sintomas.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.label_diagnostico = ctk.CTkLabel(self.frame_principal, text="Diagnóstico:")
        self.label_diagnostico.grid(row=3, column=0, padx=10, pady=10, sticky="nw")
        
        self.entry_diagnostico = ctk.CTkTextbox(self.frame_principal, height=70)
        self.entry_diagnostico.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
        
        # Botão para salvar os dados do prontuário
        self.btn_salvar = ctk.CTkButton(self.frame_principal, text="Salvar Prontuário", command=self.salvar_prontuario, width=190,height=30 )
        self.btn_salvar.grid(row=4, column=0, columnspan=2, padx=0, pady=20)
        
        # Botão para listar os prontuários
        self.btn_listar = ctk.CTkButton(self.frame_principal, text="Listar Prontuários", command=self.listar_prontuarios, width=190,height=30 )
        self.btn_listar.grid(row=5, column=0, columnspan=2, padx=10, pady=5,)
        
        # Label para exibir status ou mensagens
        self.label_status = ctk.CTkLabel(self.frame_principal, text="")
        self.label_status.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        # Textbox para mostrar a lista de prontuários
        self.txt_prontuarios = ctk.CTkTextbox(self.frame_principal, height=150)
        self.txt_prontuarios.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
    def salvar_prontuario(self):
        nome = self.entry_nome.get()
        idade = self.entry_idade.get()
        sintomas = self.entry_sintomas.get("1.0", "end-1c")
        diagnostico = self.entry_diagnostico.get("1.0", "end-1c")
        
        if nome and idade and sintomas and diagnostico:
            # Cria um novo prontuário
            novo_prontuario = Prontuario(nome=nome, idade=int(idade), sintomas=sintomas, diagnostico=diagnostico)
            session.add(novo_prontuario)  # Adiciona à sessão
            session.commit()  # Comita a sessão para o banco de dados
            
            self.label_status.configure(text="Prontuário salvo com sucesso!", fg="green")
            
            # Limpar campos
            self.entry_nome.delete(0, ctk.END)
            self.entry_idade.delete(0, ctk.END)
            self.entry_sintomas.delete("1.0", ctk.END)
            self.entry_diagnostico.delete("1.0", ctk.END)
        else:
            self.label_status.configure(text="Por favor, preencha todos os campos!", fg="red")

    def listar_prontuarios(self):
        # Limpa a textbox antes de listar
        self.txt_prontuarios.delete("1.0", ctk.END)
        
        # Consulta todos os prontuários
        prontuarios = session.query(Prontuario).all()
        
        # Adiciona os prontuários na textbox
        if prontuarios:
            for prontuario in prontuarios:
                self.txt_prontuarios.insert(ctk.END, f"ID: {prontuario.id}\nNome: {prontuario.nome}\nIdade: {prontuario.idade}\nSintomas: {prontuario.sintomas}\nDiagnóstico: {prontuario.diagnostico}\n\n")
        else:
            self.txt_prontuarios.insert(ctk.END, "Nenhum prontuário encontrado.")

