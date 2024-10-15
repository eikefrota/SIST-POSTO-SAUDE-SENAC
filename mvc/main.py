import customtkinter as ctk
from controller.controller import SistemaCadastroController
from controller.medico_controller import MedicoController


def iniciar_sistema_cadastro():
    janela = ctk.CTk()
    app = SistemaCadastroController(janela)
    janela.mainloop()

def iniciar_interface_medico():
    app = MedicoController()
    app.iniciar()

if __name__ == "__main__":
    janela_principal = ctk.CTk()
    janela_principal.title("Sistema Hospitalar")
    janela_principal.geometry("300x200")

    btn_cadastro = ctk.CTkButton(janela_principal, text="Sistema de Cadastro", command=iniciar_sistema_cadastro)
    btn_cadastro.pack(pady=20)

    btn_medico = ctk.CTkButton(janela_principal, text="Interface Médica", command=iniciar_interface_medico)
    btn_medico.pack(pady=20)

    janela_principal.mainloop()