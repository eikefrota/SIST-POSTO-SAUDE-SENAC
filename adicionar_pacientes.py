from mvc.model.model import PacienteModel, Paciente
from sqlalchemy.exc import IntegrityError

def adicionar_pacientes_em_massa():
    paciente_model = PacienteModel()

    pacientes = [
        Paciente("João Silva", "123.456.789-01", "11/09/1980", "(11) 98765-4321", "joao@email.com", "Rua A, 123"),
        Paciente("Maria Santos", "234.567.890-12", "11/05/1992", "(11) 97654-3210", "maria@email.com", "Av. B, 456"),
        Paciente("Pedro Oliveira", "345.678.901-23", "11/11/1975", "(11) 96543-2109", "pedro@email.com", "Praça C, 789"),
        Paciente("Ana Rodrigues", "456.789.012-34", "11/07/1988", "(11) 95432-1098", "ana@email.com", "Alameda D, 1011"),
        Paciente("Carlos Ferreira", "567.890.123-45", "11/03/1995", "(11) 94321-0987", "carlos@email.com", "Travessa E, 1213"),
        # Adicione mais pacientes conforme necessário
    ]

    for paciente in pacientes:
        try:
            paciente_model.adicionar_paciente(paciente)
            print(f"Paciente {paciente.nome} adicionado com sucesso.")
        except IntegrityError:
            print(f"Erro ao adicionar paciente {paciente.nome}. CPF já existe.")
            paciente_model.session.rollback()
        except Exception as e:
            print(f"Erro ao adicionar paciente {paciente.nome}: {str(e)}")
            paciente_model.session.rollback()

    print("Processo de adição em massa concluído.")

if __name__ == "__main__":
    adicionar_pacientes_em_massa()