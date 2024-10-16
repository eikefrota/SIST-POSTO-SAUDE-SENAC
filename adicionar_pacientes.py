from mvc.model.model import PacienteModel, Paciente
from sqlalchemy.exc import IntegrityError

def adicionar_pacientes_em_massa():
    paciente_model = PacienteModel()

    pacientes = [
        Paciente("João Silva", "12345678901", "1980-01-15", "(11) 98765-4321", "joao@email.com", "Rua A, 123"),
        Paciente("Maria Santos", "23456789012", "1992-05-20", "(11) 97654-3210", "maria@email.com", "Av. B, 456"),
        Paciente("Pedro Oliveira", "34567890123", "1975-11-30", "(11) 96543-2109", "pedro@email.com", "Praça C, 789"),
        Paciente("Ana Rodrigues", "45678901234", "1988-07-10", "(11) 95432-1098", "ana@email.com", "Alameda D, 1011"),
        Paciente("Carlos Ferreira", "56789012345", "1995-03-25", "(11) 94321-0987", "carlos@email.com", "Travessa E, 1213"),
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