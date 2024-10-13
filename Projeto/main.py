# main.py

import customtkinter as ctk
from view.view import SistemaCadastroView
from controller.controler import SistemaCadastroController


def main():
    ctk.set_appearance_mode("light")
    janela = ctk.CTk()

    view = SistemaCadastroView(janela)
    controller = SistemaCadastroController(view)

    janela.mainloop()


if __name__ == "__main__":
    main()
