import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class TelaListaAgendamentos(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.tree_agendamentos = None
        self.entry_data_inicial = None
        self.entry_data_final = None
        self.criar_widgets()

    def criar_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Título
        self.label_titulo = ctk.CTkLabel(self, text="Lista de Agendamentos", font=("Arial", 24, "bold"))
        self.label_titulo.grid(row=0, column=0, pady=20, sticky="ew")

        # Frame para filtros
        self.frame_filtros = ctk.CTkFrame(self)
        self.frame_filtros.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Data inicial
        self.label_data_inicial = ctk.CTkLabel(self.frame_filtros, text="Data Inicial:")
        self.label_data_inicial.grid(row=0, column=0, padx=5, pady=5)
        self.entry_data_inicial = DateEntry(self.frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.entry_data_inicial.grid(row=0, column=1, padx=5, pady=5)

        # Data final
        self.label_data_final = ctk.CTkLabel(self.frame_filtros, text="Data Final:")
        self.label_data_final.grid(row=0, column=2, padx=5, pady=5)
        self.entry_data_final = DateEntry(self.frame_filtros, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.entry_data_final.grid(row=0, column=3, padx=5, pady=5)

        # Botão de filtrar
        self.btn_filtrar = ctk.CTkButton(self.frame_filtros, text="Filtrar", command=self.filtrar_agendamentos)
        self.btn_filtrar.grid(row=0, column=4, padx=5, pady=5)

        # Tabela de agendamentos
        self.criar_tabela()

        # Scrollbar
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree_agendamentos.yview)
        self.scrollbar_y.grid(row=2, column=1, sticky="ns")
        self.tree_agendamentos.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree_agendamentos.xview)
        self.scrollbar_x.grid(row=3, column=0, sticky="ew")
        self.tree_agendamentos.configure(xscrollcommand=self.scrollbar_x.set)

        # Botões de ação
        self.frame_acoes = ctk.CTkFrame(self)
        self.frame_acoes.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_cancelar = ctk.CTkButton(self.frame_acoes, text="Cancelar Agendamento", command=self.cancelar_agendamento)
        self.btn_cancelar.pack(side="left", padx=5)

        self.btn_voltar = ctk.CTkButton(self.frame_acoes, text="Voltar", command=self.voltar)
        self.btn_voltar.pack(side="right", padx=5)

    def criar_tabela(self):
        colunas = ("ID", "Paciente", "Médico", "Data/Hora", "Status")
        self.tree_agendamentos = ttk.Treeview(self, columns=colunas, show="headings")
        
        # Configurar cabeçalhos e colunas
        for col in colunas:
            self.tree_agendamentos.heading(col, text=col, anchor="center")
            self.tree_agendamentos.column(col, anchor="center", width=150)

        self.tree_agendamentos.column("Paciente", width=200)
        self.tree_agendamentos.column("Médico", width=200)
        self.tree_agendamentos.column("Data/Hora", width=150)

        # Configurar estilo
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 12))
        
        # Configurar cores alternadas para as linhas
        self.tree_agendamentos.tag_configure('evenrow', background='#E8E8E8')
        self.tree_agendamentos.tag_configure('oddrow', background='#FFFFFF')

        self.tree_agendamentos.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def filtrar_agendamentos(self):
        if hasattr(self, 'entry_data_inicial') and hasattr(self, 'entry_data_final'):
            data_inicial = self.entry_data_inicial.get_date()
            data_final = self.entry_data_final.get_date()
            self.controller.filtrar_agendamentos(data_inicial, data_final)
        else:
            print("Erro: Widgets de data não estão inicializados")

    def atualizar_tabela(self, agendamentos):
        self.tree_agendamentos.delete(*self.tree_agendamentos.get_children())
        for i, agendamento in enumerate(agendamentos):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            data_hora_formatada = agendamento.data_hora.strftime("%d/%m/%Y %H:%M")
            self.tree_agendamentos.insert("", "end", values=(
                agendamento.id,
                agendamento.paciente.nome,
                agendamento.medico.nome,
                data_hora_formatada,
                agendamento.status
            ), tags=(tag,))

    def cancelar_agendamento(self):
        selected_item = self.tree_agendamentos.selection()
        if selected_item:
            agendamento_id = self.tree_agendamentos.item(selected_item)['values'][0]
            self.controller.cancelar_agendamento(agendamento_id)
        else:
            self.controller.mostrar_erro("Erro", "Selecione um agendamento para cancelar.")

    def voltar(self):
        self.controller.voltar_tela_recepcionista()

    def esconder(self):
        self.pack_forget()

    def pack_forget(self):
        super().pack_forget()

    def mostrar(self):
        self.pack(fill="both", expand=True)
        self.master.update_idletasks()
        if hasattr(self, 'entry_data_inicial') and self.entry_data_inicial.winfo_exists():
            self.entry_data_inicial.focus_set()

    def destruir(self):
        self.destroy()
