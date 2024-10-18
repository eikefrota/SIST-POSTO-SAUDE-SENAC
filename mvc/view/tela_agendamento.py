import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from PIL import Image, ImageTk
import os

class TelaAgendamento:
    def __init__(self, janela, controller):
        self.janela = janela
        self.controller = controller
        self.configurar_janela()
        self.logo_path = os.path.abspath("mvc/imagens/logo.png")
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        self.criar_interface_agendamento()

    def configurar_janela(self):
        self.janela.title("Agendamento de Consultas")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        self.janela.resizable(True, True)

    def carregar_imagem(self, caminho, tamanho):
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        return ctk.CTkImage(light_image=imagem, dark_image=imagem, size=tamanho)

    def criar_interface_agendamento(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)
        
        self.criar_widgets_agendamento()

    def criar_widgets_agendamento(self):
        self.frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame.grid_rowconfigure((1, 10), weight=1)

        # Logo e título
        self.criar_logo()
        self.criar_titulo("Agendamento de Consultas")

        # Campo de pesquisa
        self.criar_label("Pesquisar Paciente:", 2, 1, sticky="e")
        self.entry_pesquisa = ctk.CTkEntry(self.frame, placeholder_text="Digite o nome ou CPF", width=200, height=30, font=("Arial", 12))
        self.entry_pesquisa.grid(row=2, column=2, padx=(20, 0), pady=(10, 5), sticky="w")
        self.entry_pesquisa.bind("<KeyRelease>", self.formatar_cpf_ou_texto)
        self.botao_pesquisar = ctk.CTkButton(self.frame, text="Pesquisar", font=("Arial", 12, "bold"), width=100, height=30, command=self.pesquisar_paciente)
        self.botao_pesquisar.grid(row=2, column=2, padx=(225, 20), pady=(10, 5), sticky="w")

        # Paciente
        self.criar_label("Paciente:", 3, 1, sticky="e")
        self.combo_paciente = ttk.Combobox(self.frame, state="readonly", width=30, font=("Arial", 12))
        self.combo_paciente.grid(row=3, column=2, padx=20, pady=5, sticky="w")

        # Médico
        self.criar_label("Médico:", 4, 1, sticky="e")
        self.combo_medico = ttk.Combobox(self.frame, state="readonly", width=30, font=("Arial", 12))
        self.combo_medico.grid(row=4, column=2, padx=20, pady=5, sticky="w")

        # Data
        self.criar_label("Data:", 5, 1, sticky="e")
        self.entry_data = DateEntry(self.frame, width=12, background='darkblue', foreground='white', 
                                    borderwidth=2, font=("Arial", 12), date_pattern='dd/mm/yyyy',
                                    locale='pt_BR')
        self.entry_data.grid(row=5, column=2, padx=20, pady=5, sticky="w")
        self.entry_data.bind("<<DateEntrySelected>>", self.formatar_data)

        # Hora
        self.criar_label("Hora:", 6, 1, sticky="e")
        self.entry_hora = ctk.CTkEntry(self.frame, width=100, height=30, font=("Arial", 12))
        self.entry_hora.grid(row=6, column=2, padx=20, pady=5, sticky="w")
        self.entry_hora.bind("<KeyRelease>", self.formatar_hora)

        # Botões
        self.botao_agendar = ctk.CTkButton(self.frame, text="Agendar Consulta", font=("Arial", 18, "bold"), width=200, height=40, command=self.agendar_consulta)
        self.botao_agendar.grid(row=8, column=1, padx=20, pady=20)

        self.botao_voltar = ctk.CTkButton(self.frame, text="Voltar", font=("Arial", 18, "bold"), width=200, height=40, command=self.voltar_tela_recepcionista)
        self.botao_voltar.grid(row=8, column=2, padx=20, pady=20)

        # Adicione este novo botão após os outros botões
        self.botao_cadastrar_paciente = ctk.CTkButton(self.frame, text="Cadastrar Novo Paciente", font=("Arial", 18, "bold"), width=200, height=40, command=self.abrir_cadastro_paciente)
        self.botao_cadastrar_paciente.grid(row=9, column=1, columnspan=2, padx=20, pady=20)

        self.carregar_dados()

    def criar_label(self, texto, linha, coluna, sticky="w"):
        label = ctk.CTkLabel(self.frame, text=texto, font=("Arial", 14, "bold"))
        label.grid(row=linha, column=coluna, padx=20, pady=(0, 0), sticky=sticky)
        return label

    def criar_logo(self):
        self.label_logo = ctk.CTkLabel(self.frame, image=self.logo_image, text="")
        self.label_logo.grid(row=1, column=1, padx=(0, 20), pady=(10, 5), sticky="w")

    def criar_titulo(self, texto):
        self.label_titulo = ctk.CTkLabel(self.frame, text=texto, font=("Montserrat", 20, "bold"))
        self.label_titulo.grid(row=1, column=1, padx=(20, 0), pady=(10, 5), sticky="e")

    def formatar_hora(self, event):
        hora = self.entry_hora.get()
        hora = ''.join(filter(str.isdigit, hora))
        hora = hora[:4]  # Limita a 4 dígitos
        
        if len(hora) > 2:
            hora = f"{hora[:2]}:{hora[2:]}"
        
        self.entry_hora.delete(0, ctk.END)
        self.entry_hora.insert(0, hora)

    def formatar_data(self, event=None):
        data = self.entry_data.get_date()
        data_formatada = data.strftime("%d/%m/%Y")
        self.entry_data.set_date(data_formatada)

    def carregar_dados(self):
        pacientes = self.controller.listar_pacientes()
        self.atualizar_combo_pacientes(pacientes)

        medicos = self.controller.listar_medicos()
        self.combo_medico['values'] = [f"{m.nome} ({m.crm})" for m in medicos]

    def agendar_consulta(self):
        paciente_info = self.combo_paciente.get()
        medico_info = self.combo_medico.get()
        
        if not paciente_info or not medico_info:
            self.controller.mostrar_erro("Erro", "Selecione um paciente e um médico.")
            return

        paciente_cpf = paciente_info.split('(')[1].split(')')[0]
        medico_crm = medico_info.split('(')[1].split(')')[0]
        
        data_str = self.entry_data.get()
        hora = self.entry_hora.get()
        try:
            data_hora = datetime.strptime(f"{data_str} {hora}", "%d/%m/%Y %H:%M")
        except ValueError:
            self.controller.mostrar_erro("Erro", "Formato de data ou hora inválido. Use DD/MM/AAAA e HH:MM.")
            return

        if self.controller.agendar_consulta(paciente_cpf, medico_crm, data_hora):
            self.controller.mostrar_mensagem("Sucesso", "Consulta agendada com sucesso!")
            self.limpar_campos()
        else:
            self.controller.mostrar_erro("Erro", "Não foi possível agendar a consulta.")

    def limpar_campos(self):
        if hasattr(self, 'entry_pesquisa') and self.entry_pesquisa.winfo_exists():
            self.entry_pesquisa.delete(0, ctk.END)
        if hasattr(self, 'combo_paciente') and self.combo_paciente.winfo_exists():
            self.combo_paciente.set('')
        if hasattr(self, 'combo_medico') and self.combo_medico.winfo_exists():
            self.combo_medico.set('')
        if hasattr(self, 'entry_data') and self.entry_data.winfo_exists():
            self.entry_data.set_date(datetime.now().strftime("%d/%m/%Y"))
        if hasattr(self, 'entry_hora') and self.entry_hora.winfo_exists():
            self.entry_hora.delete(0, ctk.END)

    def voltar_tela_recepcionista(self):
        self.controller.voltar_tela_recepcionista()

    def mostrar(self):
        if not hasattr(self, 'frame') or not self.frame.winfo_exists():
            self.criar_interface_agendamento()
        else:
            self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

    def esconder(self):
        self.frame.place_forget()

    def pesquisar_paciente(self):
        termo_pesquisa = self.entry_pesquisa.get().strip()
        if termo_pesquisa:
            pacientes = self.controller.pesquisar_pacientes(termo_pesquisa)
            self.atualizar_combo_pacientes(pacientes)
        else:
            self.carregar_dados()  # Recarrega todos os pacientes se o campo de pesquisa estiver vazio

    def atualizar_combo_pacientes(self, pacientes):
        self.combo_paciente['values'] = [f"{p.nome} ({p.cpf})" for p in pacientes]
        if pacientes:
            self.combo_paciente.set(self.combo_paciente['values'][0])  # Seleciona o primeiro paciente encontrado
        else:
            self.combo_paciente.set('')  # Limpa a seleção se nenhum paciente for encontrado

    def formatar_cpf_ou_texto(self, event):
        texto = self.entry_pesquisa.get().strip()
        if texto.isdigit() or (texto.replace('.', '').replace('-', '').isdigit() and len(texto) <= 14):
            # Se for apenas dígitos ou um CPF parcialmente formatado
            cpf = ''.join(filter(str.isdigit, texto))
            if len(cpf) <= 11:
                formatado = self.formatar_cpf(cpf)
                self.entry_pesquisa.delete(0, ctk.END)
                self.entry_pesquisa.insert(0, formatado)
        # Se não for apenas dígitos ou CPF formatado, não faz nada (mantém o texto como está)

    def formatar_cpf(self, cpf):
        cpf = cpf[:11]  # Limita a 11 dígitos
        if len(cpf) <= 3:
            return cpf
        elif len(cpf) <= 6:
            return f"{cpf[:3]}.{cpf[3:]}"
        elif len(cpf) <= 9:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
        else:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def abrir_cadastro_paciente(self):
        self.controller.abrir_cadastro_paciente()
