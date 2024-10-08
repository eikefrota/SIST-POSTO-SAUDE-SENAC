class MedicoModel:
    def __init__(self, nome, especialidade, crm):
        self.nome = nome
        self.especialidade = especialidade
        self.crm = crm
        self.consultas = []

    def adicionar_consulta(self, consulta):
        self.consultas.append(consulta)

    def listar_consultas(self):
        return self.consultas


class ConsultaModel:
    def __init__(self, paciente, data, horario, observacoes=""):
        self.paciente = paciente
        self.data = data
        self.horario = horario
        self.observacoes = observacoes

    def adicionar_observacao(self, observacao):
        self.observacoes = observacao
