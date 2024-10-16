import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class TelaAgendamento(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.criar_widgets()

    def criar_widgets(self):
        self.label_titulo = ctk.CTkLabel(self, text="Agendamento de Consultas", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=20)

        self.frame_formulario = ctk.CTkFrame(self)
        self.frame_formulario.pack(pady=10, padx=10, fill="both", expand=True)

        self.label_paciente = ctk.CTkLabel(self.frame_formulario, text="Paciente:")
        self.label_paciente.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.combo_paciente = ttk.Combobox(self.frame_formulario, state="readonly")
        self.combo_paciente.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.label_medico = ctk.CTkLabel(self.frame_formulario, text="Médico:")
        self.label_medico.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_medico = ttk.Combobox(self.frame_formulario, state="readonly")
        self.combo_medico.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.label_data = ctk.CTkLabel(self.frame_formulario, text="Data:")
        self.label_data.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_data = DateEntry(self.frame_formulario, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.entry_data.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.label_hora = ctk.CTkLabel(self.frame_formulario, text="Hora:")
        self.label_hora.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_hora = ctk.CTkEntry(self.frame_formulario, width=100)
        self.entry_hora.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.btn_agendar = ctk.CTkButton(self, text="Agendar Consulta", command=self.agendar_consulta)
        self.btn_agendar.pack(pady=20)

        self.btn_listar = ctk.CTkButton(self, text="Listar Consultas", command=self.listar_consultas)
        self.btn_listar.pack(pady=10)

        self.tree_consultas = ttk.Treeview(self, columns=("ID", "Paciente", "Médico", "Data/Hora", "Status"), show="headings")
        self.tree_consultas.heading("ID", text="ID")
        self.tree_consultas.heading("Paciente", text="Paciente")
        self.tree_consultas.heading("Médico", text="Médico")
        self.tree_consultas.heading("Data/Hora", text="Data/Hora")
        self.tree_consultas.heading("Status", text="Status")
        self.tree_consultas.pack(pady=10, fill="both", expand=True)

        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar Consulta", command=self.cancelar_consulta)
        self.btn_cancelar.pack(pady=10)

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", command=self.voltar_tela_recepcionista)
        self.btn_voltar.pack(pady=10)

        self.carregar_dados()

    def carregar_dados(self):
        pacientes = self.controller.listar_pacientes()
        self.combo_paciente['values'] = [f"{p.nome} ({p.cpf})" for p in pacientes]

        medicos = self.controller.listar_medicos()
        self.combo_medico['values'] = [f"{m.nome} ({m.crm})" for m in medicos]

    def agendar_consulta(self):
        paciente_info = self.combo_paciente.get()
        medico_info = self.combo_medico.get()
        
        paciente_cpf = paciente_info.split('(')[1].split(')')[0]
        medico_crm = medico_info.split('(')[1].split(')')[0]
        
        data = self.entry_data.get_date()
        hora = self.entry_hora.get()
        try:
            data_hora = datetime.combine(data, datetime.strptime(hora, "%H:%M").time())
        except ValueError:
            self.controller.mostrar_erro("Erro", "Formato de hora inválido. Use HH:MM.")
            return

        if self.controller.agendar_consulta(paciente_cpf, medico_crm, data_hora):
            self.controller.mostrar_mensagem("Sucesso", "Consulta agendada com sucesso!")
            self.listar_consultas()
        else:
            self.controller.mostrar_erro("Erro", "Não foi possível agendar a consulta.")

    def listar_consultas(self):
        self.tree_consultas.delete(*self.tree_consultas.get_children())
        consultas = self.controller.listar_consultas()
        for consulta in consultas:
            self.tree_consultas.insert("", "end", values=(
                consulta.id,
                consulta.paciente.nome,
                consulta.medico.nome,
                consulta.data_hora.strftime("%d/%m/%Y %H:%M"),
                consulta.status
            ))

    def cancelar_consulta(self):
        selected_item = self.tree_consultas.selection()
        if selected_item:
            consulta_id = self.tree_consultas.item(selected_item)['values'][0]
            if self.controller.cancelar_consulta(consulta_id):
                self.controller.mostrar_mensagem("Sucesso", "Consulta cancelada com sucesso!")
                self.listar_consultas()
            else:
                self.controller.mostrar_erro("Erro", "Não foi possível cancelar a consulta.")
        else:
            self.controller.mostrar_erro("Erro", "Selecione uma consulta para cancelar.")

    def voltar_tela_recepcionista(self):
        self.controller.voltar_tela_recepcionista()
