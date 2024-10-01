class Paciente():
    def __init__(self, nome, cpf, dataNasc, telefone, email, endereco):
        self.nome = nome
        self.cpf = cpf
        self.dataNasc = dataNasc
        self.telefone = telefone
        self.email = email
        self.endereco = endereco

    def getNome(self):
        return self.nome
    def setNome(self, nome):
        self.nome = nome
    
    def getCpf(self):
        return self.cpf
    def setCpf(self, cpf):
        self.cpf = cpf
    
    def getDataNasc(self):
        return self.dataNasc
    def setDataNasc(self, dataNasc):
        self.dataNasc = dataNasc
    
    def getTelefone(self):
        return self.telefone
    def setTelefone(self, telefone):
        self.telefone = telefone
    
    def getEmail(self):
        return self.email
    def setEmail(self, email):
        self.email = email
    
    def getEndereco(self):
        return self.endereco
    def setEndereco(self, endereco):
        self.endereco = endereco
