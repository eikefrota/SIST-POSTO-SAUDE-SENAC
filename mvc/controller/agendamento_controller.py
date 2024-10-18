from model.model import ConsultaModel, UsuarioModel, PacienteModel
from view.tela_agendamento import TelaAgendamento
from view.tabela_agendamentos import TelaListaAgendamentos
from tkinter import messagebox
from view.tela_recepcionista import SistemaCadastroView

class AgendamentoController:
    def __init__(self, janela, main_controller):
        self.janela = janela
        self.main_controller = main_controller
        self.consulta_model = ConsultaModel()
        self.usuario_model = UsuarioModel()
        self.paciente_model = PacienteModel()
        self.view = None  # Inicialize como None
        self.view_lista_agendamentos = None

    def iniciar(self):
        if self.view is None:
            self.view = TelaAgendamento(self.janela, self)
        self.view.mostrar()
        if self.view_lista_agendamentos:
            self.view_lista_agendamentos.esconder()

    def listar_pacientes(self):
        return self.paciente_model.listar_pacientes()

    def listar_medicos(self):
        return self.usuario_model.listar_medicos()

    def agendar_consulta(self, paciente_cpf, medico_crm, data_hora):
        try:
            paciente = self.paciente_model.obter_paciente_por_cpf(paciente_cpf)
            medico = self.usuario_model.obter_usuario_por_crm(medico_crm)
            if paciente and medico:
                consulta = self.consulta_model.agendar_consulta(paciente.id, medico.id, data_hora)
                return consulta is not None
            else:
                print("Paciente ou médico não encontrado")
                return False
        except Exception as e:
            print(f"Erro ao agendar consulta: {str(e)}")
            return False

    def listar_consultas(self):
        return self.consulta_model.listar_consultas()

    def cancelar_consulta(self, consulta_id):
        return self.consulta_model.cancelar_consulta(consulta_id)

    def mostrar_mensagem(self, titulo, mensagem):
        self.main_controller.mostrar_mensagem(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        self.main_controller.mostrar_erro(titulo, mensagem)

    def abrir_tela_lista_agendamentos(self):
        if self.view:
            self.view.esconder()
        if self.view_lista_agendamentos is None or not self.view_lista_agendamentos.winfo_exists():
            self.view_lista_agendamentos = TelaListaAgendamentos(self.janela, self)
        self.view_lista_agendamentos.mostrar()
        self.listar_agendamentos()

    def filtrar_agendamentos(self, data_inicial, data_final):
        try:
            agendamentos = self.consulta_model.filtrar_agendamentos(data_inicial, data_final)
            if self.view_lista_agendamentos:
                self.view_lista_agendamentos.atualizar_tabela(agendamentos)
            else:
                print("Erro: view_lista_agendamentos não está inicializada")
        except Exception as e:
            print(f"Erro ao filtrar agendamentos: {e}")
            # Aqui você pode adicionar um messagebox para mostrar o erro ao usuário

    def listar_agendamentos(self):
        agendamentos = self.consulta_model.listar_consultas()
        if self.view_lista_agendamentos:
            self.view_lista_agendamentos.atualizar_tabela(agendamentos)
        else:
            print("Erro: view_lista_agendamentos não está inicializada")

    def cancelar_agendamento(self, agendamento_id):
        if self.consulta_model.cancelar_consulta(agendamento_id):
            messagebox.showinfo("Sucesso", "Agendamento cancelado com sucesso.")
            self.listar_agendamentos()  # Atualiza a tabela
        else:
            messagebox.showerror("Erro", "Não foi possível cancelar o agendamento.")

    def voltar_tela_recepcionista(self):
        if self.view:
            self.view.esconder()
        if self.view_lista_agendamentos:
            self.view_lista_agendamentos.esconder()
        self.main_controller.mostrar_tela_recepcionista()

    def set_view(self, view):
        self.view = view

    def pesquisar_pacientes(self, cpf):
        pacientes = self.paciente_model.pesquisar_pacientes(cpf)
        if not pacientes:
            print(f"Nenhum paciente encontrado com o CPF: {cpf}")  # Para debug
        return pacientes

    def abrir_cadastro_paciente(self):
        self.view.esconder()
        self.main_controller.recepcionista_controller.cadastrar_paciente_da_tela_agendamento()

    def voltar_para_recepcionista(self):
        if self.view:
            self.view.esconder()
        self.main_controller.mostrar_tela_recepcionista()
