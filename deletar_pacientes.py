from mvc.model.model import db_manager, Paciente

def deletar_todos_pacientes():
    session = db_manager.get_session()
    try:
        # Conta o número de pacientes antes da deleção
        num_pacientes = session.query(Paciente).count()
        
        # Deleta todos os pacientes
        session.query(Paciente).delete()
        session.commit()
        
        print(f"Todos os {num_pacientes} pacientes foram deletados com sucesso.")
    except Exception as e:
        session.rollback()
        print(f"Ocorreu um erro ao deletar os pacientes: {str(e)}")
    finally:
        session.close()

if __name__ == "__main__":
    confirmacao = input("Você tem certeza que deseja deletar TODOS os pacientes? Esta ação é irreversível. (s/n): ")
    if confirmacao.lower() == 's':
        deletar_todos_pacientes()
    else:
        print("Operação cancelada.")