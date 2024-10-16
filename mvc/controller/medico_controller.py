from model.model import ProntuarioModel
from view.tela_medico import MedicoInterface
from tkinter import messagebox

class MedicoController:
    def __init__(self, janela, main_controller):
        self.janela = janela
        self.model = ProntuarioModel()
        self.view = None
        self.main_controller = main_controller

    def salvar_prontuario(self, nome, idade, sintomas, diagnostico):
        self.model.adicionar_prontuario(nome, idade, sintomas, diagnostico)

    def listar_prontuarios(self):
        return self.model.obter_prontuarios()

    def iniciar(self):
        self.view = MedicoInterface(self.janela, self)
        self.view.pack(fill="both", expand=True)

    def fazer_logout(self):
        self.main_controller.mostrar_tela_login()

    def confirmar_acao(self, titulo, mensagem):
        return messagebox.askyesno(titulo, mensagem)