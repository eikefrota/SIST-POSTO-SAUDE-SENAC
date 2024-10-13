import customtkinter as ctk
from controller.controller import SistemaCadastroController

if __name__ == "__main__":
    janela = ctk.CTk()
    app = SistemaCadastroController(janela)
    janela.mainloop()