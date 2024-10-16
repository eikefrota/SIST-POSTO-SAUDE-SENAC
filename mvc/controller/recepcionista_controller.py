from model.model import PacienteModel, Paciente
from view.tela_recepcionista import SistemaCadastroView
from validacao.validacoes import (validar_string, validar_cpf, validar_telefone, 
                         validar_email, validar_campos_preenchidos)

class SistemaCadastroController:
    def __init__(self, janela, main_controller):
        self.janela = janela
        self.model = PacienteModel()
        self.main_controller = main_controller
        self.view = SistemaCadastroView(janela, self)

    def cadastrar_paciente(self, nome, cpf, data_nascimento, telefone, email, endereco):
        # Validar campos preenchidos
        campos_preenchidos, msg = validar_campos_preenchidos(
            nome=nome, cpf=cpf, data_nascimento=data_nascimento,
            telefone=telefone, email=email, endereco=endereco
        )
        if not campos_preenchidos:
            self.view.mostrar_erro("Erro de Validação", msg)
            return

        # Validar campos
        validacoes = [
            validar_string(nome, "Nome"),
            validar_cpf(cpf),
            validar_string(data_nascimento, "Data de Nascimento"),
            validar_telefone(telefone),
            validar_email(email),
            validar_string(endereco, "Endereço")
        ]

        for validacao, msg in validacoes:
            if not validacao:
                self.view.mostrar_erro("Erro de Validação", msg)
                return

        # Se todas as validações passarem, cadastrar o paciente
        novo_paciente = Paciente(nome, cpf, data_nascimento, telefone, email, endereco)
        self.model.adicionar_paciente(novo_paciente)
        self.view.mostrar_mensagem("Cadastro Concluído", "Pessoa cadastrada com sucesso!")
        self.view.limpar_campos()

    def fazer_logout(self):
        self.main_controller.fazer_logout()

    def confirmar_acao(self, titulo, mensagem):
        return self.view.confirmar_acao(titulo, mensagem)

    def excluir_paciente(self, item):
        valores = self.view.tabela.item(item, 'values')
        nome = valores[0]  # O nome é o primeiro valor na tupla
        if self.view.confirmar_acao("Confirmar Exclusão", f"Tem certeza que deseja excluir o paciente '{nome}' do sistema?"):
            cpf = valores[1]  # O CPF é o segundo valor na tupla
            self.model.remover_paciente_por_cpf(cpf)
            self.atualizar_tabela()
            self.view.mostrar_mensagem("Exclusão", "Paciente excluído com sucesso.")
    
    def filtrar_pacientes(self, criterio):
        pacientes_filtrados = self.model.filtrar_pacientes(criterio)
        self.view.atualizar_tabela(pacientes_filtrados)
    
    def exibir_tabela_pacientes(self):
        self.view.exibir_tabela_pacientes()
        self.atualizar_tabela()

    def atualizar_tabela(self):
        pacientes = self.model.obter_pacientes()  # Use este método em vez de obter_paciente_por_cpf
        self.view.atualizar_tabela(pacientes)

    def iniciar_alteracao_paciente(self, item, valores):
        # Criar um dicionário com os dados do paciente
        paciente = {
            "nome": valores[0],
            "cpf": valores[1],
            "data_nascimento": valores[2],
            "telefone": valores[3],
            "email": valores[4],
            "endereco": valores[5]
        }
        # Chamar a view para exibir o formulário de alteração
        self.view.exibir_formulario_alteracao(item, paciente)

    def alterar_paciente(self, item, nome, cpf, data_nascimento, telefone, email, endereco):
        # Validar apenas os campos editáveis
        validacoes = [
            validar_telefone(telefone),
            validar_email(email),
            validar_string(endereco, "Endereço")
        ]

        for validacao, msg in validacoes:
            if not validacao:
                self.view.mostrar_erro("Erro de Validação", msg)
                return False

        # Obter o paciente original
        paciente_original = self.model.obter_paciente_por_cpf(cpf)
        if not paciente_original:
            self.view.mostrar_erro("Erro", "Paciente não encontrado.")
            return False

        # Atualizar apenas os campos editáveis
        paciente_atualizado = Paciente(
            paciente_original.nome,
            paciente_original.cpf,
            paciente_original.data_nascimento,
            telefone,
            email,
            endereco
        )

        if self.model.atualizar_paciente(cpf, paciente_atualizado):
            return True
        else:
            self.view.mostrar_erro("Erro", "Não foi possível atualizar o paciente.")
            return False

    def abrir_tela_agendamento(self):
        self.main_controller.mostrar_tela_agendamento()

    def abrir_tela_lista_agendamentos(self):
        self.main_controller.mostrar_tela_lista_agendamentos()

    