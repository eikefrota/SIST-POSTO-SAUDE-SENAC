import customtkinter as ctk
from controller.recepcionista_controller import SistemaCadastroController
from controller.medico_controller import MedicoController
from controller.admin_controller import AdminController
from view.tela_login import TelaLogin
from model.model import UsuarioModel

class MainController:
    def __init__(self):
        self.janela = ctk.CTk()
        self.usuario_model = UsuarioModel()
        self.tela_login = TelaLogin(self.janela, self)

    def verificar_login(self, cpf, senha):
        return self.usuario_model.verificar_credenciais(cpf, senha)

    def abrir_painel(self, tipo_usuario):
        if tipo_usuario == 'admin':
            self.mostrar_tela_admin()
        elif tipo_usuario == 'medico':
            self.mostrar_tela_medico()
        elif tipo_usuario == 'recepcionista':
            self.mostrar_tela_recepcionista()

    def mostrar_tela_admin(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        AdminController(self.janela, self)

    def mostrar_tela_medico(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        medico_controller = MedicoController(self.janela, self)
        medico_controller.iniciar()

    def mostrar_tela_recepcionista(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        self.tela_recepcionista = SistemaCadastroController(self.janela, self)

    def mostrar_tela_login(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        self.tela_login = TelaLogin(self.janela, self)

    def iniciar(self):
        self.mostrar_tela_login()
        self.janela.mainloop()

if __name__ == "__main__":
    app = MainController()
    app.iniciar()