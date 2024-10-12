class MedicoModel:
    def __init__(self, nome, especialidade, crm):
        self.nome = nome
        self.especialidade = especialidade
        self.crm = crm
<<<<<<< HEAD
        self.consultas = []
=======
        self.consultas = []  # Lista de consultas atribuídas ao médico
    
    def getNome(self) -> str:
        return self.nome
>>>>>>> 58680b12208034c652772976a196b7ddd3cb5670

    def adicionar_consulta(self, consulta):
        self.consultas.append(consulta)

    def listar_consultas(self):
        return self.consultas


class ConsultaModel:
<<<<<<< HEAD
    def __init__(self, paciente, data, horario, observacoes=""):
=======
    def __init__(self, paciente, data, horario, observacoes=None):
>>>>>>> 58680b12208034c652772976a196b7ddd3cb5670
        self.paciente = paciente
        self.data = data
        self.horario = horario
        self.observacoes = observacoes

<<<<<<< HEAD
    def adicionar_observacao(self, observacao):
=======
    def adicionar_observacoes(self, observacao):
>>>>>>> 58680b12208034c652772976a196b7ddd3cb5670
        self.observacoes = observacao
