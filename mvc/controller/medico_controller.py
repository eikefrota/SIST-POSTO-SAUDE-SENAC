from model.model import ProntuarioModel, ConsultaModel, PacienteModel
from view.tela_medico import TelaMedico
from view.tela_prontuario import TelaProntuario
from tkinter import messagebox

class MedicoController:
    def __init__(self, janela, main_controller):
        self.janela = janela
        self.prontuario_model = ProntuarioModel()
        self.consulta_model = ConsultaModel()
        self.paciente_model = PacienteModel()
        self.view = None
        self.main_controller = main_controller

    def iniciar(self):
        self.view = TelaMedico(self.janela, self)
        self.view.mostrar()

    def pesquisar_pacientes(self, termo_pesquisa):
        consultas = self.consulta_model.pesquisar_consultas_por_paciente(termo_pesquisa)
        return [self.formatar_consulta(consulta) for consulta in consultas if consulta.status != 'Atendido']

    def formatar_consulta(self, consulta):
        return {
            'id': consulta.id,
            'nome': consulta.paciente.nome,
            'cpf': consulta.paciente.cpf,
            'data': consulta.data_hora.strftime("%d/%m/%Y"),
            'hora': consulta.data_hora.strftime("%H:%M"),
            'status': consulta.status
        }

    def selecionar_paciente(self, paciente):
        # Implementar a lógica de seleção de paciente
        pass

    def atender_paciente(self, consulta_id):
        consulta = self.consulta_model.obter_consulta_por_id(consulta_id)
        if consulta and consulta.paciente:
            self.abrir_tela_prontuario(consulta.paciente.cpf, consulta_id)
        else:
            self.mostrar_erro("Erro", "Não foi possível abrir o prontuário do paciente.")

    def abrir_tela_prontuario(self, cpf, consulta_id):
        paciente = self.paciente_model.obter_paciente_por_cpf(cpf)
        prontuario = self.prontuario_model.obter_prontuario_por_cpf(cpf)
        self.view.esconder()
        self.tela_prontuario = TelaProntuario(self.janela, self, paciente, prontuario, consulta_id)
        self.tela_prontuario.mostrar()

    def salvar_prontuario(self, cpf, dados_prontuario, consulta_id):
        if self.prontuario_model.adicionar_ou_atualizar_prontuario(cpf, dados_prontuario):
            if self.consulta_model.atualizar_status_consulta(consulta_id, "Atendido"):
                messagebox.showinfo("Sucesso", "Prontuário salvo com sucesso! Paciente atendido.")
            else:
                messagebox.showwarning("Atenção", "Prontuário salvo, mas não foi possível atualizar o status da consulta.")
            self.voltar_tela_medico()
        else:
            messagebox.showerror("Erro", "Não foi possível salvar o prontuário.")

    def voltar_tela_medico(self):
        print("Voltando para a tela do médico")
        if hasattr(self, 'tela_prontuario'):
            self.tela_prontuario.frame.destroy()
            delattr(self, 'tela_prontuario')
        self.view.frame.destroy()
        self.view.criar_interface_medico()
        self.view.mostrar()
        consultas = self.listar_consultas_do_dia()
        print(f"Consultas do dia: {consultas}")
        self.view.atualizar_tabela_pacientes(consultas)

    def fazer_logout(self):
        self.main_controller.mostrar_tela_login()

    def mostrar_erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    def confirmar_acao(self, titulo, mensagem):
        return messagebox.askyesno(titulo, mensagem)

    def listar_consultas_do_dia(self):
        consultas = self.consulta_model.listar_consultas_do_dia()
        return [self.formatar_consulta(consulta) for consulta in consultas if consulta.status != 'Atendido']

    def voltar_tela_principal(self):
        self.main_controller.voltar_para_tela_principal()

    def mostrar_mensagem(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)
