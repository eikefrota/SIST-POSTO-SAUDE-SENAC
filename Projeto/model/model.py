# model.py

class Paciente:
    def __init__(self, nome, cpf, data_nascimento, telefone, email, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.endereco = endereco


class SistemaCadastro:
    def __init__(self):
        self.pacientes = []

    def adicionar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def remover_paciente(self, index):
        if 0 <= index < len(self.pacientes):
            del self.pacientes[index]

    def obter_pacientes(self):
        return self.pacientes
