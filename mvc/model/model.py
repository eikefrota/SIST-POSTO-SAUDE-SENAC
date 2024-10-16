from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

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
    consultas = relationship("Consulta", back_populates="paciente")

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

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    crm = Column(String, nullable=False)
    consultas = relationship("Consulta", back_populates="medico")

class DatabaseManager:
    def __init__(self):
        DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost/senac"
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()
    
    def create_tables(self):
        Base.metadata.create_all(self.engine)

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

    def listar_pacientes(self):
        return self.session.query(Paciente).all()

class ProntuarioModel:
    def __init__(self):
        self.session = db_manager.get_session()

    def adicionar_prontuario(self, nome, idade, sintomas, diagnostico):
        novo_prontuario = Prontuario(nome=nome, idade=idade, sintomas=sintomas, diagnostico=diagnostico)
        self.session.add(novo_prontuario)
        self.session.commit()

    def obter_prontuarios(self):
        return self.session.query(Prontuario).all()

class UsuarioModel:
    def __init__(self):
        self.session = db_manager.get_session()

    def adicionar_usuario(self, nome, cpf, senha, tipo, crm=None):
        novo_usuario = Usuario(nome=nome, cpf=cpf, senha=senha, tipo=tipo, crm=crm)
        self.session.add(novo_usuario)
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Erro ao adicionar usuário: {str(e)}")
            return False


    def obter_usuario_por_cpf(self, cpf):
        return self.session.query(Usuario).filter_by(cpf=cpf).first()

    def verificar_credenciais(self, cpf, senha):
        usuario = self.obter_usuario_por_cpf(cpf)
        if usuario and usuario.senha == senha:
            return usuario
        return None

    def listar_profissionais(self):
        return self.session.query(Usuario).filter(Usuario.tipo != 'admin').all()

    def remover_usuario(self, cpf):
        usuario = self.obter_usuario_por_cpf(cpf)
        if usuario:
            self.session.delete(usuario)
            self.session.commit()
            return True
        return False

    def atualizar_usuario(self, cpf, nome=None, senha=None, tipo=None, crm=None):
        usuario = self.obter_usuario_por_cpf(cpf)
        if usuario:
            if nome:
                usuario.nome = nome
            if senha:
                usuario.senha = senha
            if tipo:
                usuario.tipo = tipo
            if crm is not None:
                usuario.crm = crm
            self.session.commit()
            return True
        return False

    def excluir_usuario(self, cpf):
        try:
            # Convertemos o CPF para string, caso não seja
            cpf_str = str(cpf)
            usuario = self.session.query(Usuario).filter_by(cpf=cpf_str).first()
            if usuario:
                self.session.delete(usuario)
                self.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            self.session.rollback()
            return False

    def listar_medicos(self):
        return self.session.query(Usuario).filter(Usuario.tipo == 'medico').all()

    def obter_usuario_por_crm(self, crm):
        return self.session.query(Usuario).filter_by(crm=crm).first()

class Consulta(Base):
    __tablename__ = 'consultas'

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey('pacientes.id'), nullable=False)
    medico_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    data_hora = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default='Agendada')

    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Usuario", back_populates="consultas")

class ConsultaModel:
    def __init__(self):
        self.session = db_manager.get_session()

    def agendar_consulta(self, paciente_id, medico_id, data_hora):
        nova_consulta = Consulta(paciente_id=paciente_id, medico_id=medico_id, data_hora=data_hora)
        self.session.add(nova_consulta)
        self.session.commit()
        return nova_consulta

    def listar_consultas(self):
        return self.session.query(Consulta).all()

    def cancelar_consulta(self, consulta_id):
        consulta = self.session.query(Consulta).get(consulta_id)
        if consulta:
            consulta.status = 'Cancelada'
            self.session.commit()
            return True
        return False

    def filtrar_agendamentos(self, data_inicial, data_final):
        return self.session.query(Consulta).filter(
            Consulta.data_hora.between(data_inicial, data_final)
        ).all()
