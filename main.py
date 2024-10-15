import customtkinter as ctk
from login import TelaLogin

# Define o modo de aparência
ctk.set_appearance_mode("light")  # Muda para o modo claro

# Cria a janela principal
root = ctk.CTk()
TelaLogin(root)  # Inicia a interface de login
root.mainloop()
