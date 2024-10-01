from tela_login import SistemaLogin
import tkinter as tk
import customtkinter as ctk

def main():
    ctk.set_appearance_mode("light")
    
    janela = ctk.CTk()
    app = SistemaLogin(janela)
    janela.mainloop()

if __name__ == '__main__':
    main()


