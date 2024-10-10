class MedicoController:
    def __init__(self, medico_model):
        self.medico_model = medico_model

    def obter_consultas(self):
        return self.medico_model.listar_consultas()

    def registrar_observacao(self, consulta, observacao):
        consulta.adicionar_observacoes(observacao)

    def adicionar_consulta(self, consulta):
        self.medico_model.adicionar_consulta(consulta)
