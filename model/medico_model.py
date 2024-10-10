class MedicoModel:
    def __init__(self, nome, especialidade, crm):
        self.nome = nome
        self.especialidade = especialidade
        self.crm = crm
        self.consultas = []  # Lista de consultas atribuídas ao médico
    
    def getNome(self) -> str:
        return self.nome

    def adicionar_consulta(self, consulta):
        self.consultas.append(consulta)

    def listar_consultas(self):
        return self.consultas


class ConsultaModel:
    def __init__(self, paciente, data, horario, observacoes=None):
        self.paciente = paciente
        self.data = data
        self.horario = horario
        self.observacoes = observacoes

    def adicionar_observacoes(self, observacao):
        self.observacoes = observacao
