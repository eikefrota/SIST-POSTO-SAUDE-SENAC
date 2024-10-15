from model.model import ProntuarioModel
from view.tela_medico import MedicoInterface

class MedicoController:
    def __init__(self, janela):
        self.janela = janela
        self.model = ProntuarioModel()
        self.view = None

    def salvar_prontuario(self, nome, idade, sintomas, diagnostico):
        self.model.adicionar_prontuario(nome, idade, sintomas, diagnostico)

    def listar_prontuarios(self):
        return self.model.obter_prontuarios()

    def iniciar(self):
        self.view = MedicoInterface(self.janela, self)
        self.view.pack(fill="both", expand=True)