# controller.py

from model.model import Paciente, SistemaCadastro
from view.view import SistemaCadastroView
import customtkinter as ctk


class SistemaCadastroController:
    def __init__(self, view):
        self.view = view
        self.sistema_cadastro = SistemaCadastro()

        self.view.botao_cadastrar.configure(command=self.cadastrar_paciente)
        self.view.btn_mostrar_tabela.configure(command=self.exibir_tabela)

    def cadastrar_paciente(self):
        dados = self.view.obter_dados_formulario()

        if all(dados.values()):
            try:
                # Valida CPF e Telefone
                if len(dados["cpf"]) != 11 or not dados["cpf"].isdigit():
                    raise ValueError("O CPF deve conter 11 dígitos numéricos.")
                if len(dados["telefone"]) < 10 or not dados["telefone"].isdigit():
                    raise ValueError("O telefone deve conter apenas números e ter pelo menos 10 dígitos.")
                if "@" not in dados["email"] or "." not in dados["email"]:
                    raise ValueError("O e-mail informado é inválido.")

                paciente = Paciente(**dados)
                self.sistema_cadastro.adicionar_paciente(paciente)
                self.view.limpar_campos()
                self.view.mostrar_mensagem("Cadastro Concluído", "Pessoa cadastrada com sucesso!")

            except ValueError as e:
                self.view.mostrar_erro("Erro", str(e))
        else:
            self.view.mostrar_erro("Erro", "Por favor, preencha todos os campos!")

    def exibir_tabela(self):
        self.view.criar_tabela()
        self.view.atualizar_tabela(self.sistema_cadastro.obter_pacientes())
