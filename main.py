from model.medico_model import MedicoModel, ConsultaModel
from controller.medical_controller import MedicoController
from view.medico_view import MedicoView
import customtkinter as ctk

# Inicializar a interface do médico
if __name__ == "__main__":
    medico_model = MedicoModel("Dr. João", "Cardiologista", "123456")
    controller = MedicoController(medico_model)

    # Adicionando consultas de exemplo
    consulta1 = ConsultaModel("Paciente 1", "03/10/2024", "14:00")
    consulta2 = ConsultaModel("Paciente 2", "04/10/2024", "10:00")
    controller.adicionar_consulta(consulta1)
    controller.adicionar_consulta(consulta2)

    root = ctk.CTk()
    app = MedicoView(root, controller)
    root.mainloop() 