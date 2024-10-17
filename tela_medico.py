import customtkinter as ctk
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image, ImageTk


# Configuração do banco de dados
DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/senac"
# Criando a conexão com o banco de dados
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Definindo o modelo do prontuário
class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    sintomas = Column(Text)
    diagnostico = Column(Text)

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)

# Criar a classe de sessão
Session = sessionmaker(bind=engine)
session = Session()

# Classe para a interface do médico
class MedicoInterface(ctk.CTk):
    def __init__(self):

                # Constantes
        self.logo_path = "imagens/logo.png"

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

        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        
        # Widgets da interface
        self.create_widgets()

    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)
    
    def create_widgets(self):
     
        
        self.label_sintomas = ctk.CTkLabel(self.frame_principal, text="Sintomas:")
        self.label_sintomas.grid(row=3, column=0, padx=(10,0), pady=10, sticky="w")
        
        self.entry_sintomas = ctk.CTkTextbox(self.frame_principal, height=120, width=200)
        self.entry_sintomas.grid(row=3, column=1, padx=0, pady=10, sticky="w")
        
        self.label_diagnostico = ctk.CTkLabel(self.frame_principal, text="Diagnóstico:")
        self.label_diagnostico.grid(row=3, column=2, padx=10, pady=10, sticky="e")
        
        self.entry_diagnostico = ctk.CTkTextbox(self.frame_principal, height=120, width=200)
        self.entry_diagnostico.grid(row=3, column=3, padx=(5,50), pady=10, sticky="e")
        
        
        # Botão para listar os prontuários
        self.btn_listar = ctk.CTkButton(self.frame_principal, text="Listar Pacientes", command=self.listar_pacientes, width=190,height=30 )
        self.btn_listar.grid(row=5, column=2, columnspan=2, padx=(0,10), pady=5)
        
        # Label para exibir status ou mensagens
        self.label_status = ctk.CTkLabel(self.frame_principal, text="")
        self.label_status.grid(row=6, column=0,  padx=10, pady=5)
        
        # Textbox para mostrar a lista de prontuários
        self.txt_pacientes = ctk.CTkTextbox(self.frame_principal, height=150, width=190)
        self.txt_pacientes.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Botão para editar sintomas
        self.btn_editar_sintomas = ctk.CTkButton(self.frame_principal, text="Editar Sintomas", command=self.editar_sintomas, width=190, height=30)
        self.btn_editar_sintomas.grid(row=5, column=0, padx=(50, 0),pady=5)
        
        # Botão para editar diagnóstico
        self.btn_editar_diagnostico = ctk.CTkButton(self.frame_principal, text="Editar Diagnóstico", command=self.editar_diagnostico, width=190, height=30)
        self.btn_editar_diagnostico.grid(row=5, column=1, columnspan=2, padx=10, pady=5)
        
        # Adicione estes campos de entrada
        self.entry_id_editar = ctk.CTkEntry(self.frame_principal, placeholder_text="ID do Paciente")
        self.entry_id_editar.grid(row=6, column=1, columnspan=2, padx=10, pady=5)

    # ... outras funções existentes ...

    def editar_sintomas(self):
        id_paciente = self.entry_id_editar.get()
        if not id_paciente:
            self.label_status.configure(text="Por favor, insira o ID do paciente!", fg="red")
            return
        
        paciente = session.query(Paciente).filter_by(id=id_paciente).first()
        if paciente:
            novos_sintomas = self.entry_sintomas.get("1.0", "end-1c")
            paciente.sintomas = novos_sintomas
            session.commit()
            self.label_status.configure(text="Sintomas atualizados com sucesso!", fg="green")
            self.listar_pacientes()  # Atualiza a lista de pacientes
        else:
            self.label_status.configure(text="Paciente não encontrado!", fg="red")

    def editar_diagnostico(self):
        id_paciente = self.entry_id_editar.get()
        if not id_paciente:
            self.label_status.configure(text="Por favor, insira o ID do paciente!", fg="red")
            return
        
        paciente = session.query(Paciente).filter_by(id=id_paciente).first()
        if paciente:
            novo_diagnostico = self.entry_diagnostico.get("1.0", "end-1c")
            paciente.diagnostico = novo_diagnostico
            session.commit()
            self.label_status.configure(text="Diagnóstico atualizado com sucesso!", fg="green")
            self.listar_pacientes()  # Atualiza a lista de pacientes
        else:
            self.label_status.configure(text="Paciente não encontrado!", fg="red")
        
    
    def listar_pacientes(self):
        # Limpa a textbox antes de listar
        self.txt_pacientes.delete("1.0", ctk.END)
        
        # Consulta todos os prontuários
        pacientes = session.query(Paciente).all()
        
        # Adiciona os prontuários na textbox
        if pacientes:
            for paciente in pacientes:
                self.txt_pacientes.insert(ctk.END, f"ID: {paciente.id}\nNome: {paciente.nome}\nData_nascimento: {paciente.data_nascimento}\nTelefone: {paciente.telefone}\nEmail: {paciente.email}\nEndereco: {paciente.endereco}\n Sintomas: {paciente.sintomas}\nDiagnóstico: {paciente.diagnostico}\n\n")
        else:
            self.txt_paciente.insert(ctk.END, "Nenhum prontuário encontrado.")

