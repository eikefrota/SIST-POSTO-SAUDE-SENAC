from tkinter import messagebox
from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import ttk
from tkinter import Menu
from tkinter import Toplevel

class SistemaCadastro:
    
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro")
        self.janela.geometry(f"{self.janela.winfo_screenwidth()}x{self.janela.winfo_screenheight()}+0+0")
        self.janela.resizable(True, True)

        self.logo_path = "imagens/file.png"
        self.logo_image = self.carregar_imagem(self.logo_path, (150, 150))
        
        self.pacientes = [
            {
                "nome": "Teste Paciente",
                "cpf": "12345678901",
                "data_nascimento": "01/01/1980",
                "telefone": "1234567890",
                "email": "teste@dominio.com",
                "endereco": "Rua de Teste, 123"
            }
        ]
        
        self.criar_interface_cadastro()
    
    def carregar_imagem(self, caminho, tamanho, ctk_image=True):
        """Carrega e redimensiona uma imagem."""
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.LANCZOS)
        if ctk_image:
            return ctk.CTkImage(imagem, size=tamanho)
        return ImageTk.PhotoImage(imagem)
    
    def criar_label(self, texto, linha, coluna, frame=None):
        """Cria e retorna um label em um frame específico ou no frame principal se não especificado."""
        if frame is None:
            frame = self.frame  # Default para o frame principal
        label = ctk.CTkLabel(frame, text=texto, font=("Arial", 14, "bold"))
        label.grid(row=linha, column=coluna, padx=(30, 30), pady=(0, 0), sticky="w")
        return label

    def criar_entry(self, linha, coluna, placeholder, frame=None):
        """Cria um campo de entrada com placeholder em um frame específico ou no frame principal se não especificado."""
        if frame is None:
            frame = self.frame  # Default para o frame principal
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=300, height=30, font=("Montserrat", 16))
        entry.grid(row=linha, column=coluna, padx=(30, 30), pady=(0, 10), sticky="ns")
        return entry
    
    def criar_logo(self, frame=None):
        if frame is None:
            frame = self.frame  # Default para o frame principal
        self.label_logo = ctk.CTkLabel(frame, image=self.logo_image, text="")
        self.label_logo.grid(row=1, column=1, padx=(0, 20), pady=(10, 5), sticky="w")
        
        

    def criar_titulo(self, texto, frame=None):
        if frame is None:
            frame = self.frame  # Default para o frame principal
        self.label_titulo = ctk.CTkLabel(frame, text=texto, font=("Montserrat", 20, "bold"))
        self.label_titulo.grid(row=1, column=1, padx=(20, 0), pady=(10, 5), sticky="e")

    def retornar_logo(self, frame=None):
        return self.criar_logo(frame)
    
    def retornar_titulo(self, info_titulo, frame=None):
        return self.criar_titulo(info_titulo, frame)

    def retornar_label(self, label_info, linha, coluna, frame=None):
        """Retorna um label criado em um frame específico ou no frame principal se não especificado."""
        return self.criar_label(label_info, linha, coluna, frame)

    def retornar_entry(self, linha, coluna, placeholder_inf, frame=None):
        """Retorna um campo de entrada criado em um frame específico ou no frame principal se não especificado."""
        return self.criar_entry(linha, coluna, placeholder_inf, frame)

    #--------------------------------MODELO FORMULARIO--------------------------------------------------------------
    def criar_widgets_formulario(self, frame, valores=None):
        """Cria os widgets do formulário no frame especificado.
        
        Args:
            frame: Frame onde os widgets serão criados.
            valores: Dicionário com os valores iniciais para preenchimento dos campos.
        """
        self.retornar_logo(frame)
        self.retornar_titulo("Cadastro de Paciente" if not valores else "Atualização de Cadastro", frame)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(10, weight=2)

        # Nome e CPF
        self.retornar_label("Nome:", 2, 1, frame)
        entry_nome = self.retornar_entry(3, 1, "Digite o nome completo", frame)
        if valores: entry_nome.insert(0, valores.get("nome", ""))

        self.retornar_label("CPF:", 2, 2, frame)
        entry_cpf = self.retornar_entry(3, 2, "XXX.XXX.XXX-XX", frame)
        if valores: entry_cpf.insert(0, valores.get("cpf", ""))

        # Data de Nascimento e Telefone
        self.retornar_label("Data de Nascimento:", 4, 1, frame)
        entry_datanasc = self.retornar_entry(5, 1, "DD/MM/AAAA", frame)
        if valores: entry_datanasc.insert(0, valores.get("data_nascimento", ""))

        self.retornar_label("Telefone:", 4, 2, frame)
        entry_telefone = self.retornar_entry(5, 2, "(DDD) 91234-5678", frame)
        if valores: entry_telefone.insert(0, valores.get("telefone", ""))

        # Email e Endereço
        self.retornar_label("Email:", 6, 1, frame)
        entry_email = self.retornar_entry(7, 1, "exemplo@dominio.com", frame)
        if valores: entry_email.insert(0, valores.get("email", ""))

        self.retornar_label("Endereço:", 6, 2, frame)
        entry_endereco = self.retornar_entry(7, 2, "Digite o endereço", frame)
        if valores: entry_endereco.insert(0, valores.get("endereco", ""))

        return entry_nome, entry_cpf, entry_datanasc, entry_telefone, entry_email, entry_endereco
    
    def criar_interface_cadastro(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Frame centralizado
        self.frame = ctk.CTkFrame(self.janela, border_width=3, border_color="#00CED1", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=0)
        self.frame.grid_columnconfigure(3, weight=1)

        # Criar widgets de cadastro
        self.entry_nome, self.entry_cpf, self.entry_datanasc, self.entry_telefone, self.entry_email, self.entry_endereco = self.criar_widgets_formulario(self.frame)

        # Botões
        self.botao_cadastrar = ctk.CTkButton(self.frame, text="Cadastrar", font=("Arial", 14, "bold"), command=self.cadastrar_paciente)
        self.botao_cadastrar.grid(row=9, column=1, padx=(5, 5), pady=20, sticky="e")

        self.btn_mostrar_tabela = ctk.CTkButton(self.frame, text="Mostrar tabela", font=("Arial", 14, "bold"), command=self.exibir_tabela_pacientes)
        self.btn_mostrar_tabela.grid(row=9, column=2, padx=(5, 5), pady=20, sticky="w")


    def cadastrar_paciente(self):
        nome = self.entry_nome.get()
        cpf = self.entry_cpf.get()
        datanasc = self.entry_datanasc.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        endereco = self.entry_endereco.get()

        # Verifica se todos os campos estão preenchidos
        if nome and cpf and datanasc and telefone and email and endereco:
            try:
                # Valida o CPF e o telefone
                if len(cpf) != 11 or not cpf.isdigit():
                    raise ValueError("O CPF deve conter 11 dígitos numéricos.")
                
                if len(telefone) < 10 or not telefone.isdigit():
                    raise ValueError("O telefone deve conter apenas números e ter pelo menos 10 dígitos.")

                # Aqui não estamos convertendo datanasc, mas você pode adicionar lógica para validar a data
                # Para o email, uma validação simples:
                if "@" not in email or "." not in email:
                    raise ValueError("O e-mail informado é inválido.")

                # Criar dicionário para o paciente
                paciente = {
                    "nome": nome,
                    "cpf": cpf,
                    "data_nascimento": datanasc,
                    "telefone": telefone,
                    "email": email,
                    "endereco": endereco
                }

                # Armazenar paciente na lista
                self.pacientes.append(paciente)

                # Limpar os campos após o cadastro
                self.limpar_campos()

                messagebox.showinfo("Cadastro Concluído", "Pessoa cadastrada com sucesso!")

                if hasattr(self, 'tabela'):
                    self.atualizar_tabela()

            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos!")


    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_cpf.delete(0, ctk.END)
        self.entry_datanasc.delete(0, ctk.END)
        self.entry_telefone.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_endereco.delete(0, ctk.END)

    def exibir_tabela_pacientes(self):
        # Limpar a tela para mostrar a tabela
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        # Criar a Tabela (Treeview)
        self.tabela_frame = ctk.CTkFrame(self.janela, fg_color="white")
        self.tabela_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.8)


        # Configurando o grid para redimensionar dinamicamente
        self.tabela_frame.grid_columnconfigure(0, weight=1)  # Permitir que a tabela expanda
        self.tabela_frame.grid_rowconfigure(0, weight=1)     # Permitir que a tabela expanda verticalmente

        # Criar a tabela com grid, configurada para expandir conforme a janela é redimensionada
        self.tabela = ttk.Treeview(self.tabela_frame, columns=("Nome", "CPF", "Data de Nascimento", "Telefone", "Email", "Endereço"), show="headings")
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold")) # Nomes maiores e negrito
        
        # Definir as colunas
        self.tabela.heading("Nome", text="Nome")
        self.tabela.heading("CPF", text="CPF")
        self.tabela.heading("Data de Nascimento", text="Data de Nascimento")
        self.tabela.heading("Telefone", text="Telefone")
        self.tabela.heading("Email", text="Email")
        self.tabela.heading("Endereço", text="Endereço")

        # Aplicar larguras sugeridas e alinhamento
        self.tabela.column("Nome", anchor="center", width=250)
        self.tabela.column("CPF", anchor="center", width=150)
        self.tabela.column("Data de Nascimento", anchor="center", width=160)
        self.tabela.column("Telefone", anchor="center", width=150)
        self.tabela.column("Email", anchor="center", width=250)
        self.tabela.column("Endereço", anchor="center", width=300)

        self.tabela.tag_configure('evenrow', background='#E8E8E8')  # Cor clara (linhas pares)
        self.tabela.tag_configure('oddrow', background='#FFFFFF')

        # Adicionar botões de contexto para exclusão e alteração
        self.tabela.bind("<Button-3>", self.mostrar_menu_contexto)  # Clique com o botão direito para mostrar o menu

        # Usar grid para a tabela, ocupando toda a área disponível
        self.tabela.grid(row=0, column=0, sticky="nsew")  # Expande em todas as direções
        
        # Scrollbars para caso a tabela tenha muitos itens
        scrollbar_y = ttk.Scrollbar(self.tabela_frame, orient="vertical", command=self.tabela.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")  # Posiciona a scrollbar no lado direito da tabela
        
        scrollbar_x = ttk.Scrollbar(self.tabela_frame, orient="horizontal", command=self.tabela.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")  # Posiciona a scrollbar abaixo da tabela

        self.tabela.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Sempre atualiza a tabela após a criação
        self.atualizar_tabela()

        # Botão para retornar à tela de cadastro
        self.botao_voltar = ctk.CTkButton(self.tabela_frame, text="Voltar", command=self.criar_interface_cadastro)
        self.botao_voltar.grid(row=2, column=0, columnspan=2, pady=10)
    
    def mostrar_menu_contexto(self, event):
        """Exibe um menu de contexto na linha selecionada."""
        item = self.tabela.identify_row(event.y)
        if item:
            menu = Menu(self.janela, tearoff=0)
            menu.add_command(label="Alterar", command=lambda: self.alterar_paciente(item))
            menu.add_command(label="Excluir", command=lambda: self.excluir_paciente(item))
            menu.post(event.x_root, event.y_root)

    def excluir_paciente(self, item):
        """Remove o paciente da lista após confirmação e atualiza a tabela."""
        paciente_idx = self.tabela.index(item)
        paciente = self.pacientes[paciente_idx]

        # Caixa de diálogo para confirmar a exclusão
        confirmacao = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir o paciente '{paciente['nome']}' do sistema?"
        )

        if confirmacao:
            self.pacientes.pop(paciente_idx)
            self.atualizar_tabela()
            messagebox.showinfo("Exclusão", "Paciente excluído com sucesso.")
        else:
            messagebox.showinfo("Cancelado", "A exclusão foi cancelada.")

    def alterar_paciente(self, item):
        """Abre uma janela para alteração dos dados do paciente com a interface replicada."""
        paciente_idx = self.tabela.index(item)
        paciente = self.pacientes[paciente_idx]

        # Criar uma nova janela para alteração, semelhante à interface de cadastro
        janela_alteracao = ctk.CTkToplevel()
        janela_alteracao.title("Alterar Paciente")
        janela_alteracao.geometry(f"{janela_alteracao.winfo_screenwidth()}x{janela_alteracao.winfo_screenheight()}+0+0")
        janela_alteracao.resizable(True, True)
        janela_alteracao.grab_set()

        frame_alteracao = ctk.CTkFrame(janela_alteracao, border_width=3, border_color="#00CED1", fg_color="white")
        frame_alteracao.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.6, relheight=0.7)

        frame_alteracao.grid_columnconfigure(0, weight=1)
        frame_alteracao.grid_columnconfigure(1, weight=0)
        frame_alteracao.grid_columnconfigure(2, weight=0)
        frame_alteracao.grid_columnconfigure(3, weight=1)

        # Criar widgets de alteração com valores preenchidos
        entry_nome, entry_cpf, entry_datanasc, entry_telefone, entry_email, entry_endereco = self.criar_widgets_formulario(frame_alteracao, paciente)

        # Botão de salvar as alterações
        botao_salvar = ctk.CTkButton(
            frame_alteracao, text="Salvar Alterações", 
            font=("Arial", 14, "bold"), 
            command=lambda: self.salvar_alteracoes(
                paciente_idx, 
                entry_nome.get(), 
                entry_cpf.get(), 
                entry_datanasc.get(), 
                entry_telefone.get(), 
                entry_email.get(), 
                entry_endereco.get(), 
                janela_alteracao
            )
        )
        botao_salvar.grid(row=9, column=1, pady=20, padx=10, sticky="e")

        botao_descartar = ctk.CTkButton(
        frame_alteracao, text="Descartar Alterações", 
        font=("Arial", 14, "bold"), 
        command=lambda: self.descartar_alteracoes(janela_alteracao)
    )
        botao_descartar.grid(row=9, column=2, pady=20, padx=10, sticky="w")

    def salvar_alteracoes(self, paciente_idx, nome, cpf, datanasc, telefone, email, endereco, janela):
        """Salva as alterações feitas no paciente e atualiza a tabela."""
        # Atualizar os dados do paciente
        self.pacientes[paciente_idx] = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": datanasc,
            "telefone": telefone,
            "email": email,
            "endereco": endereco
        }

        # Atualizar a tabela com as novas informações
        self.atualizar_tabela()
        janela.destroy()
        messagebox.showinfo("Alteração", "Paciente alterado com sucesso.")

    def descartar_alteracoes(self, janela):
        """Descarta as alterações e fecha a janela de alteração."""
        janela.destroy()
        messagebox.showinfo("Alteração Descartada", "As alterações foram descartadas com sucesso.")


    def atualizar_tabela(self):
        """Inserir os pacientes cadastrados na tabela, com cores alternadas."""
    
        # Limpar a tabela antes de inserir novos dados
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Inserir os pacientes cadastrados na tabela com cores alternadas
        for i, paciente in enumerate(self.pacientes):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'  # Define a tag com base no índice (par/ímpar)
            self.tabela.insert("", "end", values=(paciente["nome"], paciente["cpf"], paciente["data_nascimento"], paciente["telefone"], paciente["email"], paciente["endereco"]), tags=(tag,))

        
