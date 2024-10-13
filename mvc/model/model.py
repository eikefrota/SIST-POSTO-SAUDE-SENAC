class Paciente:
    def __init__(self, nome, cpf, data_nascimento, telefone, email, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

class PacienteModel:
    def __init__(self):
        self.pacientes = [
            Paciente("Teste Paciente", "12345678901", "01/01/1980", "1234567890", "teste@dominio.com", "Rua de Teste, 123")
        ]

    def adicionar_paciente(self, paciente):
        self.pacientes.append(paciente)

    def remover_paciente(self, index):
        if 0 <= index < len(self.pacientes):
            del self.pacientes[index]

    def atualizar_paciente(self, cpf, paciente_atualizado):
        for i, paciente in enumerate(self.pacientes):
            if paciente.cpf == cpf:
                self.pacientes[i] = paciente_atualizado
                return True
        return False

    def obter_pacientes(self):
        return self.pacientes

    def obter_paciente_por_cpf(self, cpf):
        for paciente in self.pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None

    def filtrar_pacientes(self, criterio):
        criterio = criterio.lower()
        return [p for p in self.pacientes if criterio in p.nome.lower() or criterio in p.cpf]
    