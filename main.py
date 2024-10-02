import customtkinter as ctk
from tela_cadastro import SistemaCadastro  # Importar a classe do outro arquivo

def main():

    ctk.set_appearance_mode("light")
    # Criar a janela principal
    janela = ctk.CTk()
    
    # Instanciar o sistema de cadastro
    app = SistemaCadastro(janela)
    
    # Iniciar o loop principal da interface
    janela.mainloop()

if __name__ == "__main__":
    main()