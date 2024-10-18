import customtkinter as ctk
from controller.recepcionista_controller import RecepcionistaController
from controller.medico_controller import MedicoController
from controller.admin_controller import AdminController
from controller.agendamento_controller import AgendamentoController
from view.tela_login import TelaLogin
from model.model import UsuarioModel
from tkinter import messagebox
import tkinter.ttk as ttk
from view.tela_prontuario import TelaProntuario

class MainController:
    def __init__(self):
        self.janela = ctk.CTk()
        self.usuario_atual = None
        self.usuario_model = UsuarioModel()
        self.tela_login = None
        self.recepcionista_controller = None
        self.agendamento_controller = None
        self.medico_controller = None
        self.tela_prontuario = None

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
        self.limpar_janela()
        AdminController(self.janela, self)

    def mostrar_tela_medico(self):
        self.limpar_janela()
        if not self.medico_controller:
            self.medico_controller = MedicoController(self.janela, self)
        self.medico_controller.iniciar()

    def mostrar_tela_recepcionista(self):
        self.limpar_janela()
        if not self.recepcionista_controller:
            self.recepcionista_controller = RecepcionistaController(self.janela, self)
        self.recepcionista_controller.view.mostrar()

    def mostrar_tela_agendamento(self):
        self.limpar_janela()
        if not self.agendamento_controller:
            self.agendamento_controller = AgendamentoController(self.janela, self)
        self.agendamento_controller.iniciar()

    def mostrar_tela_lista_agendamentos(self):
        self.limpar_janela()
        if not hasattr(self, 'agendamento_controller') or self.agendamento_controller is None:
            self.agendamento_controller = AgendamentoController(self.janela, self)
        self.agendamento_controller.abrir_tela_lista_agendamentos()

    def mostrar_tela_login(self):
        self.limpar_janela()
        self.tela_login = TelaLogin(self.janela, self)

    def iniciar(self):
        self.mostrar_tela_login()
        self.janela.mainloop()

    def fazer_logout(self):
        self.usuario_atual = None
        self.mostrar_tela_login()

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def voltar_para_agendamento(self):
        if self.agendamento_controller:
            self.agendamento_controller.iniciar()
        else:
            print("Erro: AgendamentoController não está inicializado")

    def limpar_janela(self):
        for widget in self.janela.winfo_children():
            if isinstance(widget, (ctk.CTkBaseClass, ttk.Widget)):
                widget.destroy()
        self.janela.update_idletasks()

    def mostrar_tela_prontuario(self, prontuario):
        self.limpar_janela()
        if not hasattr(self, 'tela_prontuario'):
            self.tela_prontuario = TelaProntuario(self.janela, self, prontuario)
        else:
            self.tela_prontuario.prontuario = prontuario
            self.tela_prontuario.criar_interface_prontuario()
        self.tela_prontuario.mostrar()

    def voltar_tela_medico(self):
        self.limpar_janela()
        self.medico_controller.iniciar()

    def obter_tipo_usuario_atual(self):
        if self.usuario_atual:
            return self.usuario_atual.tipo
        return None

    def fazer_login(self, cpf, senha):
        usuario = self.usuario_model.verificar_credenciais(cpf, senha)
        if usuario:
            self.usuario_atual = usuario
            tipo_usuario = self.obter_tipo_usuario_atual()
            if tipo_usuario == 'medico':
                self.mostrar_tela_medico()
            elif tipo_usuario == 'recepcionista':
                self.mostrar_tela_recepcionista()
            elif tipo_usuario == 'admin':
                self.mostrar_tela_admin()
            else:
                self.mostrar_erro("Erro", "Tipo de usuário não reconhecido")
            return True
        else:
            self.mostrar_erro("Erro de Login", "Credenciais inválidas")
            return False

    def voltar_para_tela_principal(self):
        tipo_usuario = self.obter_tipo_usuario_atual()
        if tipo_usuario == 'medico':
            self.mostrar_tela_medico()
        elif tipo_usuario == 'recepcionista':
            self.mostrar_tela_recepcionista()
        elif tipo_usuario == 'admin':
            self.mostrar_tela_admin()
        else:
            self.mostrar_tela_login()

if __name__ == "__main__":
    app = MainController()
    app.iniciar()
    
