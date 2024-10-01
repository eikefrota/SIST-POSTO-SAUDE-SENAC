import customtkinter as ctk
from tela_cadastro import SistemaCadastro

def main():
    ctk.set_appearance_mode("light")

    janela = ctk.CTk()  # Criação da janela
    app = SistemaCadastro(janela)  # Passa a janela para a classe SistemaCadastro
    janela.mainloop()  # Inicia o loop da aplicação

if __name__ == '__main__':
    main()

        
