from model.model import UsuarioModel
from view.tela_admin import TelaAdmin

class AdminController:
    def __init__(self, janela, main_controller):
        self.model = UsuarioModel()
        self.view = TelaAdmin(janela, self)
        self.main_controller = main_controller

    def adicionar_medico(self, nome, cpf, senha, crm):
        return self.model.adicionar_usuario(nome, cpf, senha, 'medico', crm)

    def adicionar_recepcionista(self, nome, cpf, senha):
        return self.model.adicionar_usuario(nome, cpf, senha, 'recepcionista')

    def listar_profissionais(self):
        profissionais = self.model.listar_profissionais()
        return [{"nome": p.nome, "cpf": p.cpf, "tipo": p.tipo} for p in profissionais]

    def voltar_para_login(self):
        self.main_controller.mostrar_tela_login()