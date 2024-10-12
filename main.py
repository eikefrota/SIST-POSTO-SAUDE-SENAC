from tela_medico import MedicoInterface
import customtkinter as ctk


def main():
    ctk.set_appearance_mode("light")

    app = MedicoInterface()
    app.mainloop()

if __name__ == "__main__":
    main()
