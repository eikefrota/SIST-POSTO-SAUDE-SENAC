from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    data_nascimento = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    def __init__(self, nome, cpf, data_nascimento, telefone, email, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

class Prontuario(Base):
    __tablename__ = 'prontuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)
    sintomas = Column(Text, nullable=False)
    diagnostico = Column(Text, nullable=False)

class DatabaseManager:
    def __init__(self):
        DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/senac"
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

db_manager = DatabaseManager()

class PacienteModel:
    def __init__(self):
        self.session = db_manager.get_session()

    def adicionar_paciente(self, paciente):
        self.session.add(paciente)
        self.session.commit()

    def remover_paciente_por_cpf(self, cpf):
        paciente = self.session.query(Paciente).filter_by(cpf=cpf).first()
        if paciente:
            self.session.delete(paciente)
            self.session.commit()

    def atualizar_paciente(self, cpf, paciente_atualizado):
        paciente = self.session.query(Paciente).filter_by(cpf=cpf).first()
        if paciente:
            paciente.nome = paciente_atualizado.nome
            paciente.data_nascimento = paciente_atualizado.data_nascimento
            paciente.telefone = paciente_atualizado.telefone
            paciente.email = paciente_atualizado.email
            paciente.endereco = paciente_atualizado.endereco
            self.session.commit()
            return True
        return False

    def obter_pacientes(self):
        return self.session.query(Paciente).all()

    def obter_paciente_por_cpf(self, cpf):
        return self.session.query(Paciente).filter_by(cpf=cpf).first()

    def filtrar_pacientes(self, criterio):
        return self.session.query(Paciente).filter(
            (Paciente.nome.ilike(f"%{criterio}%")) | (Paciente.cpf.ilike(f"%{criterio}%"))
        ).all()

class ProntuarioModel:
    def __init__(self):
        self.session = db_manager.get_session()

    def adicionar_prontuario(self, nome, idade, sintomas, diagnostico):
        novo_prontuario = Prontuario(nome=nome, idade=idade, sintomas=sintomas, diagnostico=diagnostico)
        self.session.add(novo_prontuario)
        self.session.commit()

    def obter_prontuarios(self):
        return self.session.query(Prontuario).all()