import json
import random
import statistics
from tkinter import *
from tkinter import messagebox, filedialog
from datetime import date, datetime, timedelta
from pathlib import Path


LIMITE_EMPRESTIMOS = 3
PRAZO_DIAS = 7
MULTA_POR_DIA = 5.00
PASTA_RELATORIOS = "relatorios"
ARQUIVO_JSON = "dados_biblioteca.json"

livros = []
usuarios = []
emprestimos = []
historico = []
pagamentos = []


def gerar_id(prefixo):
    numero = random.randint(1000, 9999)
    hora = datetime.now().strftime('%H%M%S')
    return prefixo + hora + str(numero)

def registrar_historico(acao):
    hora_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico.append({"data_hora": hora_atual, "acao": acao})

def formatar_moeda(valor):
    texto = "R$ " + str(round(valor, 2))
    return texto.replace(".", ",")

def converter_data(texto):
    texto = texto.strip()
    if texto == "":
        return date.today()
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except:
        return date.today()

def encontrar_usuario(id_usuario):
    resultado = None
    for u in usuarios:
        if u["id"] == id_usuario:
            resultado = u
    return resultado

def encontrar_livro(id_livro):
    resultado = None
    for l in livros:
        if l["id"] == id_livro:
            resultado = l
    return resultado

def encontrar_emprestimo(id_emp):
    resultado = None
    for e in emprestimos:
        if e["id"] == id_emp:
            resultado = e
    return resultado

def contar_ativos(id_usuario):
    total = 0
    for e in emprestimos:
        if e["id_usuario"] == id_usuario and e["status"] == "ativo":
            total = total + 1
    return total

def calcular_multa(data_dev, data_prev):
    dias = (data_dev - data_prev).days
    if dias > 0:
        multa = dias * MULTA_POR_DIA
        return dias, multa
    return 0, 0.0

def atualizar_situacoes():
    hoje = date.today()
    for e in emprestimos:
        if e["status"] == "ativo":
            data_prev = datetime.strptime(e["data_prevista"], "%Y-%m-%d").date()
            if hoje > data_prev:
                e["situacao"] = "atrasado"
            else:
                e["situacao"] = "dentro do prazo"


janela = Tk()
janela.title("Sistema de Biblioteca")
janela.geometry("700x500")


frame_menu = Frame(janela, width=180, bg="#eeeeee")
frame_menu.pack(side=LEFT, fill=Y)
frame_menu.pack_propagate(False)

frame_conteudo = Frame(janela, bg="white")
frame_conteudo.pack(side=LEFT, fill=BOTH, expand=True)

def limpar():
    for widget in frame_conteudo.winfo_children():
        widget.destroy()


def tela_cadastrar_usuario():
    limpar()
    Label(frame_conteudo, text="Cadastrar Usuário", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="Nome *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_nome = Entry(frame_conteudo, width=35)
    e_nome.grid(row=1, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="CPF *", bg="white").grid(row=2, column=0, sticky=W, padx=10)
    e_cpf = Entry(frame_conteudo, width=35)
    e_cpf.grid(row=2, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="E-mail", bg="white").grid(row=3, column=0, sticky=W, padx=10)
    e_email = Entry(frame_conteudo, width=35)
    e_email.grid(row=3, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Telefone", bg="white").grid(row=4, column=0, sticky=W, padx=10)
    e_tel = Entry(frame_conteudo, width=35)
    e_tel.grid(row=4, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Endereço", bg="white").grid(row=5, column=0, sticky=W, padx=10)
    e_end = Entry(frame_conteudo, width=35)
    e_end.grid(row=5, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Nascimento (dd/mm/aaaa)", bg="white").grid(row=6, column=0, sticky=W, padx=10)
    e_nasc = Entry(frame_conteudo, width=35)
    e_nasc.grid(row=6, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Tipo (aluno/professor/comunidade)", bg="white").grid(row=7, column=0, sticky=W, padx=10)
    e_tipo = Entry(frame_conteudo, width=35)
    e_tipo.grid(row=7, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Observações", bg="white").grid(row=8, column=0, sticky=W, padx=10)
    e_obs = Entry(frame_conteudo, width=35)
    e_obs.grid(row=8, column=1, padx=10, pady=3)

    def salvar():
        nome = e_nome.get().strip()
        cpf = e_cpf.get().strip()

        if nome == "" or cpf == "":
            messagebox.showerror("Erro", "Nome e CPF são obrigatórios.")
            return

        
        for u in usuarios:
            if u["cpf"] == cpf:
                messagebox.showerror("Erro", "Já existe um usuário com esse CPF.")
                return

        novo_usuario = {
            "id": gerar_id("U"),
            "nome": nome,
            "cpf": cpf,
            "email": e_email.get().strip(),
            "telefone": e_tel.get().strip(),
            "endereco": e_end.get().strip(),
            "nascimento": e_nasc.get().strip(),
            "tipo": e_tipo.get().strip(),
            "observacoes": e_obs.get().strip(),
            "multa_total": 0.0,
            "ativo": True
        }
        usuarios.append(novo_usuario)
        registrar_historico("Usuário cadastrado: " + nome)
        messagebox.showinfo("OK", "Usuário cadastrado!\nID: " + novo_usuario["id"])

      
        e_nome.delete(0, END)
        e_cpf.delete(0, END)
        e_email.delete(0, END)
        e_tel.delete(0, END)
        e_end.delete(0, END)
        e_nasc.delete(0, END)
        e_tipo.delete(0, END)
        e_obs.delete(0, END)

    Button(frame_conteudo, text="Salvar", command=salvar, bg="#4CAF50", fg="white", width=15).grid(row=9, column=1, pady=10, sticky=E, padx=10)


def tela_listar_usuarios():
    limpar()
    Label(frame_conteudo, text="Usuários Cadastrados", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    texto = Text(frame_conteudo, width=80, height=22, font=("Courier", 9))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    texto.pack(padx=10, fill=BOTH, expand=True)

    if len(usuarios) == 0:
        texto.insert(END, "Nenhum usuário cadastrado.")
    else:
        for u in usuarios:
            if u["ativo"] == True:
                status = "ativo"
            else:
                status = "removido"
            ativos = contar_ativos(u["id"])
            texto.insert(END, "-" * 60 + "\n")
            texto.insert(END, "ID:       " + u["id"] + "\n")
            texto.insert(END, "Nome:     " + u["nome"] + "\n")
            texto.insert(END, "CPF:      " + u["cpf"] + "   Tipo: " + u["tipo"] + "   Status: " + status + "\n")
            texto.insert(END, "E-mail:   " + u["email"] + "   Tel: " + u["telefone"] + "\n")
            texto.insert(END, "Empréstimos ativos: " + str(ativos) + "/" + str(LIMITE_EMPRESTIMOS) + "\n")
            texto.insert(END, "Multa em aberto:    " + formatar_moeda(u["multa_total"]) + "\n")

    texto.config(state=DISABLED)
def tela_cadastrar_livro():
    limpar()
    Label(frame_conteudo, text="Cadastrar Livro", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="Título *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_titulo = Entry(frame_conteudo, width=35)
    e_titulo.grid(row=1, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Autor *", bg="white").grid(row=2, column=0, sticky=W, padx=10)
    e_autor = Entry(frame_conteudo, width=35)
    e_autor.grid(row=2, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Ano de publicação", bg="white").grid(row=3, column=0, sticky=W, padx=10)
    e_ano = Entry(frame_conteudo, width=35)
    e_ano.grid(row=3, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="ISBN / Código", bg="white").grid(row=4, column=0, sticky=W, padx=10)
    e_isbn = Entry(frame_conteudo, width=35)
    e_isbn.grid(row=4, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Categoria", bg="white").grid(row=5, column=0, sticky=W, padx=10)
    e_categoria = Entry(frame_conteudo, width=35)
    e_categoria.grid(row=5, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Editora", bg="white").grid(row=6, column=0, sticky=W, padx=10)
    e_editora = Entry(frame_conteudo, width=35)
    e_editora.grid(row=6, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Quantidade", bg="white").grid(row=7, column=0, sticky=W, padx=10)
    e_qtd = Entry(frame_conteudo, width=35)
    e_qtd.grid(row=7, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Prateleira", bg="white").grid(row=8, column=0, sticky=W, padx=10)
    e_prat = Entry(frame_conteudo, width=35)
    e_prat.grid(row=8, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Palavras-chave", bg="white").grid(row=9, column=0, sticky=W, padx=10)
    e_palavras = Entry(frame_conteudo, width=35)
    e_palavras.grid(row=9, column=1, padx=10, pady=2)

    Label(frame_conteudo, text="Observações", bg="white").grid(row=10, column=0, sticky=W, padx=10)
    e_obs = Entry(frame_conteudo, width=35)
    e_obs.grid(row=10, column=1, padx=10, pady=2)

    def salvar():
        titulo = e_titulo.get().strip()
        autor = e_autor.get().strip()

        if titulo == "" or autor == "":
            messagebox.showerror("Erro", "Título e autor são obrigatórios.")
            return

        try:
            ano = int(e_ano.get().strip())
        except:
            ano = 0

        try:
            qtd = int(e_qtd.get().strip())
            if qtd < 1:
                qtd = 1
        except:
            qtd = 1

        novo_livro = {
            "id": gerar_id("L"),
            "titulo": titulo,
            "autor": autor,
            "ano": ano,
            "isbn": e_isbn.get().strip(),
            "categoria": e_categoria.get().strip(),
            "editora": e_editora.get().strip(),
            "quantidade_total": qtd,
            "quantidade_disponivel": qtd,
            "prateleira": e_prat.get().strip(),
            "palavras_chave": e_palavras.get().strip(),
            "observacoes": e_obs.get().strip(),
            "ativo": True
        }
        livros.append(novo_livro)
        registrar_historico("Livro cadastrado: " + titulo)
        messagebox.showinfo("OK", "Livro cadastrado!\nID: " + novo_livro["id"])

        e_titulo.delete(0, END)
        e_autor.delete(0, END)
        e_ano.delete(0, END)
        e_isbn.delete(0, END)
        e_categoria.delete(0, END)
        e_editora.delete(0, END)
        e_qtd.delete(0, END)
        e_prat.delete(0, END)
        e_palavras.delete(0, END)
        e_obs.delete(0, END)

    Button(frame_conteudo, text="Salvar", command=salvar, bg="#4CAF50", fg="white", width=15).grid(row=11, column=1, pady=10, sticky=E, padx=10)


def tela_listar_livros():
    limpar()
    Label(frame_conteudo, text="Livros Cadastrados", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    texto = Text(frame_conteudo, width=80, height=22, font=("Courier", 9))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    texto.pack(padx=10, fill=BOTH, expand=True)

    if len(livros) == 0:
        texto.insert(END, "Nenhum livro cadastrado.")
    else:
        for l in livros:
            if l["ativo"] == True:
                status = "ativo"
            else:
                status = "removido"
            texto.insert(END, "-" * 60 + "\n")
            texto.insert(END, "ID:         " + l["id"] + "\n")
            texto.insert(END, "Título:     " + l["titulo"] + "\n")
            texto.insert(END, "Autor:      " + l["autor"] + "   Ano: " + str(l["ano"]) + "\n")
            texto.insert(END, "Categoria:  " + l["categoria"] + "   Editora: " + l["editora"] + "\n")
            texto.insert(END, "Disponível: " + str(l["quantidade_disponivel"]) + "/" + str(l["quantidade_total"]) + "   Prateleira: " + l["prateleira"] + "\n")
            texto.insert(END, "Status:     " + status + "\n")

    texto.config(state=DISABLED)


def tela_buscar_livro():
    limpar()
    Label(frame_conteudo, text="Buscar Livro", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    frame_busca = Frame(frame_conteudo, bg="white")
    frame_busca.pack()
    Label(frame_busca, text="Termo:", bg="white").pack(side=LEFT)
    e_termo = Entry(frame_busca, width=30)
    e_termo.pack(side=LEFT, padx=5)

    texto = Text(frame_conteudo, width=80, height=18, font=("Courier", 9))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    texto.pack(padx=10, pady=5, fill=BOTH, expand=True)

    def buscar():
        termo = e_termo.get().strip().lower()
        texto.config(state=NORMAL)
        texto.delete("1.0", END)

        encontrados = []
        for l in livros:
            campos = l["titulo"] + " " + l["autor"] + " " + l["categoria"] + " " + l["palavras_chave"]
            if termo in campos.lower() and l["ativo"] == True:
                encontrados.append(l)

        if len(encontrados) == 0:
            texto.insert(END, "Nenhum livro encontrado.")
        else:
            texto.insert(END, str(len(encontrados)) + " resultado(s):\n\n")
            for l in encontrados:
                linha = "ID: " + l["id"] + "  |  " + l["titulo"] + " - " + l["autor"] + "  |  Disponível: " + str(l["quantidade_disponivel"]) + "\n"
                texto.insert(END, linha)

        texto.config(state=DISABLED)

    Button(frame_busca, text="Buscar", command=buscar, bg="#2196F3", fg="white").pack(side=LEFT, padx=5)
    e_termo.bind("<Return>", lambda event: buscar())


def tela_emprestar():
    limpar()
    Label(frame_conteudo, text="Realizar Empréstimo", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="ID do Usuário *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_uid = Entry(frame_conteudo, width=35)
    e_uid.grid(row=1, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="ID do Livro *", bg="white").grid(row=2, column=0, sticky=W, padx=10)
    e_lid = Entry(frame_conteudo, width=35)
    e_lid.grid(row=2, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Data do empréstimo (dd/mm/aaaa, vazio=hoje)", bg="white").grid(row=3, column=0, sticky=W, padx=10)
    e_data = Entry(frame_conteudo, width=35)
    e_data.grid(row=3, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Observação", bg="white").grid(row=4, column=0, sticky=W, padx=10)
    e_obs = Entry(frame_conteudo, width=35)
    e_obs.grid(row=4, column=1, padx=10, pady=3)


    texto = Text(frame_conteudo, width=75, height=10, font=("Courier", 8))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.grid(row=6, column=2, sticky=NS)
    texto.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
    texto.insert(END, "Usuários ativos:\n")
    for u in usuarios:
        if u["ativo"] == True:
            texto.insert(END, "  " + u["id"] + "  " + u["nome"] + "  multa:" + formatar_moeda(u["multa_total"]) + "\n")
    texto.insert(END, "\nLivros disponíveis:\n")
    for l in livros:
        if l["ativo"] == True and l["quantidade_disponivel"] > 0:
            texto.insert(END, "  " + l["id"] + "  " + l["titulo"] + "  disp:" + str(l["quantidade_disponivel"]) + "\n")
    texto.config(state=DISABLED)

    def salvar():
        usuario = encontrar_usuario(e_uid.get().strip())
        livro = encontrar_livro(e_lid.get().strip())

        if usuario == None:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return
        if usuario["ativo"] == False:
            messagebox.showerror("Erro", "Usuário inativo.")
            return
        if usuario["multa_total"] > 0:
            messagebox.showerror("Erro", "Usuário tem multa em aberto.")
            return
        if livro == None:
            messagebox.showerror("Erro", "Livro não encontrado.")
            return
        if livro["ativo"] == False:
            messagebox.showerror("Erro", "Livro inativo.")
            return
        if livro["quantidade_disponivel"] <= 0:
            messagebox.showerror("Erro", "Livro indisponível.")
            return
        if contar_ativos(usuario["id"]) >= LIMITE_EMPRESTIMOS:
            messagebox.showerror("Erro", "Limite de " + str(LIMITE_EMPRESTIMOS) + " empréstimos atingido.")
            return

        data_emp = converter_data(e_data.get())
        data_prev = data_emp + timedelta(days=PRAZO_DIAS)

        novo_emp = {
            "id": gerar_id("E"),
            "id_usuario": usuario["id"],
            "nome_usuario": usuario["nome"],
            "id_livro": livro["id"],
            "titulo_livro": livro["titulo"],
            "data_emprestimo": data_emp.isoformat(),
            "data_prevista": data_prev.isoformat(),
            "data_devolucao": "",
            "status": "ativo",
            "situacao": "dentro do prazo",
            "dias_atraso": 0,
            "multa": 0.0,
            "renovacoes": 0,
            "observacao": e_obs.get().strip()
        }
        emprestimos.append(novo_emp)
        livro["quantidade_disponivel"] = livro["quantidade_disponivel"] - 1
        registrar_historico("Empréstimo: " + livro["titulo"] + " para " + usuario["nome"])
        messagebox.showinfo("OK", "Empréstimo realizado!\nID: " + novo_emp["id"] + "\nDevolução prevista: " + data_prev.strftime("%d/%m/%Y"))

        e_uid.delete(0, END)
        e_lid.delete(0, END)
        e_data.delete(0, END)
        e_obs.delete(0, END)

    Button(frame_conteudo, text="Confirmar Empréstimo", command=salvar, bg="#4CAF50", fg="white").grid(row=5, column=1, pady=8, sticky=E, padx=10)


def tela_listar_emprestimos():
    atualizar_situacoes()
    limpar()
    Label(frame_conteudo, text="Empréstimos Registrados", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    texto = Text(frame_conteudo, width=80, height=22, font=("Courier", 9))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    texto.pack(padx=10, fill=BOTH, expand=True)

    if len(emprestimos) == 0:
        texto.insert(END, "Nenhum empréstimo registrado.")
    else:
        for e in emprestimos:
            data_prev = datetime.strptime(e["data_prevista"], "%Y-%m-%d").date().strftime("%d/%m/%Y")
            texto.insert(END, "-" * 60 + "\n")
            texto.insert(END, "ID:        " + e["id"] + "\n")
            texto.insert(END, "Usuário:   " + e["nome_usuario"] + "\n")
            texto.insert(END, "Livro:     " + e["titulo_livro"] + "\n")
            texto.insert(END, "Status:    " + e["status"] + "   Situação: " + e["situacao"] + "\n")
            texto.insert(END, "Prev. dev: " + data_prev + "   Renovações: " + str(e["renovacoes"]) + "\n")
            texto.insert(END, "Multa:     " + formatar_moeda(e["multa"]) + "\n")

    texto.config(state=DISABLED)


def tela_devolver():
    limpar()
    Label(frame_conteudo, text="Devolver Livro", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="ID do Empréstimo *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_id = Entry(frame_conteudo, width=35)
    e_id.grid(row=1, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Data de devolução (dd/mm/aaaa, vazio=hoje)", bg="white").grid(row=2, column=0, sticky=W, padx=10)
    e_data = Entry(frame_conteudo, width=35)
    e_data.grid(row=2, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Observação", bg="white").grid(row=3, column=0, sticky=W, padx=10)
    e_obs = Entry(frame_conteudo, width=35)
    e_obs.grid(row=3, column=1, padx=10, pady=3)

    def devolver():
        emp = encontrar_emprestimo(e_id.get().strip())

        if emp == None:
            messagebox.showerror("Erro", "Empréstimo não encontrado.")
            return
        if emp["status"] != "ativo":
            messagebox.showerror("Erro", "Esse empréstimo já foi devolvido.")
            return
        if not messagebox.askyesno("Confirmar", "Confirmar devolução?"):
            return

        livro = encontrar_livro(emp["id_livro"])
        usuario = encontrar_usuario(emp["id_usuario"])
        data_dev = converter_data(e_data.get())
        data_prev = datetime.strptime(emp["data_prevista"], "%Y-%m-%d").date()
        dias, multa = calcular_multa(data_dev, data_prev)

        emp["data_devolucao"] = data_dev.isoformat()
        emp["status"] = "devolvido"
        emp["dias_atraso"] = dias
        emp["multa"] = multa

        if dias > 0:
            emp["situacao"] = "devolvido com atraso"
        else:
            emp["situacao"] = "devolvido no prazo"

        emp["observacao"] = emp["observacao"] + " | " + e_obs.get().strip()

        if livro != None:
            livro["quantidade_disponivel"] = livro["quantidade_disponivel"] + 1
        if usuario != None:
            usuario["multa_total"] = usuario["multa_total"] + multa

        registrar_historico("Devolução: " + emp["titulo_livro"] + " por " + emp["nome_usuario"])

        msg = "Devolução registrada!"
        if multa > 0:
            msg = msg + "\nAtraso: " + str(dias) + " dia(s) — Multa: " + formatar_moeda(multa)
        else:
            msg = msg + "\nDentro do prazo, sem multa."

        messagebox.showinfo("OK", msg)
        e_id.delete(0, END)
        e_data.delete(0, END)
        e_obs.delete(0, END)

    Button(frame_conteudo, text="Registrar Devolução", command=devolver, bg="#4CAF50", fg="white").grid(row=4, column=1, pady=10, sticky=E, padx=10)


def tela_renovar():
    limpar()
    Label(frame_conteudo, text="Renovar Empréstimo", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="ID do Empréstimo *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_id = Entry(frame_conteudo, width=35)
    e_id.grid(row=1, column=1, padx=10, pady=3)

    def renovar():
        emp = encontrar_emprestimo(e_id.get().strip())

        if emp == None:
            messagebox.showerror("Erro", "Empréstimo não encontrado.")
            return
        if emp["status"] != "ativo":
            messagebox.showerror("Erro", "Não é possível renovar um empréstimo devolvido.")
            return
        if emp["renovacoes"] >= 2:
            messagebox.showerror("Erro", "Limite de 2 renovações atingido.")
            return
        if not messagebox.askyesno("Confirmar", "Confirmar renovação por mais 7 dias?"):
            return

        data_prev = datetime.strptime(emp["data_prevista"], "%Y-%m-%d").date()
        nova_data = data_prev + timedelta(days=PRAZO_DIAS)
        emp["data_prevista"] = nova_data.isoformat()
        emp["renovacoes"] = emp["renovacoes"] + 1
        emp["situacao"] = "dentro do prazo"

        registrar_historico("Renovação do empréstimo: " + emp["id"])
        messagebox.showinfo("OK", "Renovado!\nNova data prevista: " + nova_data.strftime("%d/%m/%Y"))
        e_id.delete(0, END)

    Button(frame_conteudo, text="Renovar", command=renovar, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10, sticky=E, padx=10)
def tela_consultar_multas():
    limpar()
    Label(frame_conteudo, text="Consultar Multas do Usuário", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    frame_top = Frame(frame_conteudo, bg="white")
    frame_top.pack()
    Label(frame_top, text="ID do Usuário:", bg="white").pack(side=LEFT)
    e_id = Entry(frame_top, width=30)
    e_id.pack(side=LEFT, padx=5)

    texto = Text(frame_conteudo, width=80, height=18, font=("Courier", 9))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    texto.pack(padx=10, pady=5, fill=BOTH, expand=True)

    def consultar():
        u = encontrar_usuario(e_id.get().strip())
        texto.config(state=NORMAL)
        texto.delete("1.0", END)

        if u == None:
            texto.insert(END, "Usuário não encontrado.")
        else:
            texto.insert(END, "Usuário: " + u["nome"] + "\n")
            texto.insert(END, "Multa total em aberto: " + formatar_moeda(u["multa_total"]) + "\n\n")
            texto.insert(END, "Empréstimos com multa:\n")
            achou = False
            for e in emprestimos:
                if e["id_usuario"] == u["id"] and e["multa"] > 0:
                    achou = True
                    linha = "  " + e["titulo_livro"] + "  |  Atraso: " + str(e["dias_atraso"]) + " dia(s)  |  " + formatar_moeda(e["multa"]) + "\n"
                    texto.insert(END, linha)
            if achou == False:
                texto.insert(END, "  Nenhum empréstimo com multa.\n")

        texto.config(state=DISABLED)

    Button(frame_top, text="Consultar", command=consultar, bg="#2196F3", fg="white").pack(side=LEFT, padx=5)
    e_id.bind("<Return>", lambda event: consultar())


def tela_pagar_multa():
    limpar()
    Label(frame_conteudo, text="Pagar Multa", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="ID do Usuário *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_id = Entry(frame_conteudo, width=35)
    e_id.grid(row=1, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Valor pago (R$) *", bg="white").grid(row=2, column=0, sticky=W, padx=10)
    e_valor = Entry(frame_conteudo, width=35)
    e_valor.grid(row=2, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Forma de pagamento (dinheiro/pix/cartão)", bg="white").grid(row=3, column=0, sticky=W, padx=10)
    e_forma = Entry(frame_conteudo, width=35)
    e_forma.grid(row=3, column=1, padx=10, pady=3)

    Label(frame_conteudo, text="Observação", bg="white").grid(row=4, column=0, sticky=W, padx=10)
    e_obs = Entry(frame_conteudo, width=35)
    e_obs.grid(row=4, column=1, padx=10, pady=3)

    def pagar():
        u = encontrar_usuario(e_id.get().strip())
        if u == None:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return
        try:
            valor = float(e_valor.get().replace(",", ".").strip())
        except:
            messagebox.showerror("Erro", "Valor inválido.")
            return
        if valor <= 0:
            messagebox.showerror("Erro", "O valor deve ser maior que zero.")
            return
        if u["multa_total"] <= 0:
            messagebox.showerror("Erro", "Esse usuário não tem multa em aberto.")
            return

        
        if valor > u["multa_total"]:
            abatido = u["multa_total"]
        else:
            abatido = valor
        u["multa_total"] = u["multa_total"] - abatido

        novo_pag = {
            "id": gerar_id("P"),
            "id_usuario": u["id"],
            "nome_usuario": u["nome"],
            "valor": abatido,
            "forma_pagamento": e_forma.get().strip(),
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "observacao": e_obs.get().strip()
        }
        pagamentos.append(novo_pag)
        registrar_historico("Pagamento: " + u["nome"] + " - " + formatar_moeda(abatido))
        messagebox.showinfo("OK", "Pagamento registrado: " + formatar_moeda(abatido) + "\nSaldo restante: " + formatar_moeda(u["multa_total"]))

        e_id.delete(0, END)
        e_valor.delete(0, END)
        e_forma.delete(0, END)
        e_obs.delete(0, END)

    Button(frame_conteudo, text="Registrar Pagamento", command=pagar, bg="#4CAF50", fg="white").grid(row=5, column=1, pady=10, sticky=E, padx=10)

def tela_remover_livro():
    limpar()
    Label(frame_conteudo, text="Remover Livro", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="ID do Livro *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_id = Entry(frame_conteudo, width=35)
    e_id.grid(row=1, column=1, padx=10, pady=3)

    def remover():
        livro = encontrar_livro(e_id.get().strip())
        if livro == None:
            messagebox.showerror("Erro", "Livro não encontrado.")
            return
        
        for emp in emprestimos:
            if emp["id_livro"] == livro["id"] and emp["status"] == "ativo":
                messagebox.showerror("Erro", "Livro tem empréstimo ativo, não pode ser removido.")
                return
        if not messagebox.askyesno("Confirmar", "Remover o livro:\n" + livro["titulo"] + "?"):
            return
        livro["ativo"] = False
        registrar_historico("Livro removido: " + livro["titulo"])
        messagebox.showinfo("OK", "Livro removido do acervo ativo.")
        e_id.delete(0, END)

    Button(frame_conteudo, text="Remover", command=remover, bg="#f44336", fg="white").grid(row=2, column=1, pady=10, sticky=E, padx=10)


def tela_remover_usuario():
    limpar()
    Label(frame_conteudo, text="Remover Usuário", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="ID do Usuário *", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_id = Entry(frame_conteudo, width=35)
    e_id.grid(row=1, column=1, padx=10, pady=3)

    def remover():
        u = encontrar_usuario(e_id.get().strip())
        if u == None:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return
        if contar_ativos(u["id"]) > 0:
            messagebox.showerror("Erro", "Usuário tem empréstimos ativos, não pode ser removido.")
            return
        if not messagebox.askyesno("Confirmar", "Remover o usuário:\n" + u["nome"] + "?"):
            return
        u["ativo"] = False
        registrar_historico("Usuário removido: " + u["nome"])
        messagebox.showinfo("OK", "Usuário removido do cadastro ativo.")
        e_id.delete(0, END)

    Button(frame_conteudo, text="Remover", command=remover, bg="#f44336", fg="white").grid(row=2, column=1, pady=10, sticky=E, padx=10)

def montar_relatorio(incluir_hist=True):
    atualizar_situacoes()

    total_livros = len(livros)
    total_usuarios = len(usuarios)
    total_emps = len(emprestimos)
    total_ativos = 0
    for e in emprestimos:
        if e["status"] == "ativo":
            total_ativos = total_ativos + 1

    lista_multas = []
    for e in emprestimos:
        if e["multa"] > 0:
            lista_multas.append(e["multa"])

    soma_multas = sum(lista_multas)
    if len(lista_multas) > 0:
        media_multas = statistics.mean(lista_multas)
    else:
        media_multas = 0.0

    linhas = []
    linhas.append("-" * 60)
    linhas.append("RELATÓRIO GERAL - Biblioteca RA")
    linhas.append("Gerado em: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    linhas.append("-" * 60)
    linhas.append("Livros: " + str(total_livros) + "  |  Usuários: " + str(total_usuarios))
    linhas.append("Empréstimos: " + str(total_emps) + "  |  Ativos: " + str(total_ativos))
    linhas.append("Total de multas: " + formatar_moeda(soma_multas) + "  |  Média: " + formatar_moeda(media_multas))
    linhas.append("")

    linhas.append("LIVROS:")
    if len(livros) == 0:
        linhas.append("  Nenhum livro.")
    for l in livros:
        linhas.append("  " + l["id"] + "  " + l["titulo"] + " - " + l["autor"] + "  disp:" + str(l["quantidade_disponivel"]) + "/" + str(l["quantidade_total"]))

    linhas.append("\nUSUÁRIOS:")
    if len(usuarios) == 0:
        linhas.append("  Nenhum usuário.")
    for u in usuarios:
        linhas.append("  " + u["id"] + "  " + u["nome"] + "  multa:" + formatar_moeda(u["multa_total"]) + "  ativo:" + str(u["ativo"]))

    linhas.append("\nEMPRÉSTIMOS:")
    if len(emprestimos) == 0:
        linhas.append("  Nenhum empréstimo.")
    for e in emprestimos:
        linhas.append("  " + e["id"] + "  " + e["nome_usuario"] + " -> " + e["titulo_livro"] + "  " + e["status"] + "  " + e["situacao"] + "  multa:" + formatar_moeda(e["multa"]))

    linhas.append("\nPAGAMENTOS:")
    if len(pagamentos) == 0:
        linhas.append("  Nenhum pagamento.")
    for p in pagamentos:
        linhas.append("  " + p["data_hora"] + "  " + p["nome_usuario"] + "  " + formatar_moeda(p["valor"]) + "  " + p["forma_pagamento"])

    linhas.append("\nHISTÓRICO:")
    if incluir_hist == False:
        linhas.append("  (ocultado)")
    elif len(historico) == 0:
        linhas.append("  Nenhuma ação.")
    else:
        for h in historico[-30:]:
            linhas.append("  " + h["data_hora"] + "  " + h["acao"])

    linhas.append("\nFim do relatório.")
    return "\n".join(linhas)


def tela_relatorio():
    limpar()
    Label(frame_conteudo, text="Relatório Geral", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    texto = Text(frame_conteudo, width=80, height=22, font=("Courier", 9))
    scroll = Scrollbar(frame_conteudo, command=texto.yview)
    texto.configure(yscrollcommand=scroll.set)
    scroll.pack(side=RIGHT, fill=Y)
    texto.pack(padx=10, fill=BOTH, expand=True)
    texto.insert(END, montar_relatorio())
    texto.config(state=DISABLED)


def tela_salvar_relatorio():
    limpar()
    Label(frame_conteudo, text="Salvar Relatório em .txt", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="Nome do arquivo (vazio = automático)", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_nome = Entry(frame_conteudo, width=35)
    e_nome.grid(row=1, column=1, padx=10, pady=3)

    var_hist = BooleanVar(value=True)
    Checkbutton(frame_conteudo, text="Incluir histórico", variable=var_hist, bg="white").grid(row=2, column=1, sticky=W, padx=10)

    def salvar():
        if not messagebox.askyesno("Confirmar", "Confirmar geração do relatório?"):
            return

        Path(PASTA_RELATORIOS).mkdir(exist_ok=True)
        nome = e_nome.get().strip()
        if nome == "":
            nome = "relatorio_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
        if not nome.endswith(".txt"):
            nome = nome + ".txt"

        caminho = Path(PASTA_RELATORIOS) / nome
        conteudo = montar_relatorio(incluir_hist=var_hist.get())

        arquivo = open(caminho, "w", encoding="utf-8")
        arquivo.write(conteudo)
        arquivo.close()

        registrar_historico("Relatório salvo: " + str(caminho))
        messagebox.showinfo("OK", "Relatório salvo em:\n" + str(caminho))

    Button(frame_conteudo, text="Salvar", command=salvar, bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10, sticky=E, padx=10)


def tela_salvar_json():
    limpar()
    Label(frame_conteudo, text="Salvar Dados em JSON", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="Nome do arquivo (vazio = padrão)", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_nome = Entry(frame_conteudo, width=35)
    e_nome.grid(row=1, column=1, padx=10, pady=3)

    def salvar():
        nome = e_nome.get().strip()
        if nome == "":
            nome = ARQUIVO_JSON
        if not nome.endswith(".json"):
            nome = nome + ".json"

        dados = {
            "livros": livros,
            "usuarios": usuarios,
            "emprestimos": emprestimos,
            "historico": historico,
            "pagamentos": pagamentos
        }

        arquivo = open(nome, "w", encoding="utf-8")
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        arquivo.close()

        registrar_historico("Dados salvos: " + nome)
        messagebox.showinfo("OK", "Dados salvos em:\n" + nome)

    Button(frame_conteudo, text="Salvar JSON", command=salvar, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10, sticky=E, padx=10)


def tela_carregar_json():
    limpar()
    Label(frame_conteudo, text="Carregar Dados de JSON", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    Label(frame_conteudo, text="Nome do arquivo (vazio = padrão)", bg="white").grid(row=1, column=0, sticky=W, padx=10)
    e_nome = Entry(frame_conteudo, width=35)
    e_nome.grid(row=1, column=1, padx=10, pady=3)

    def procurar():
        arq = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if arq:
            e_nome.delete(0, END)
            e_nome.insert(0, arq)

    Button(frame_conteudo, text="Procurar...", command=procurar).grid(row=2, column=1, sticky=W, padx=10)

    def carregar():
        nome = e_nome.get().strip()
        if nome == "":
            nome = ARQUIVO_JSON

        if not Path(nome).exists():
            messagebox.showerror("Erro", "Arquivo não encontrado:\n" + nome)
            return

        arquivo = open(nome, "r", encoding="utf-8")
        dados = json.load(arquivo)
        arquivo.close()

        livros.clear()
        usuarios.clear()
        emprestimos.clear()
        historico.clear()
        pagamentos.clear()

        livros.extend(dados.get("livros", []))
        usuarios.extend(dados.get("usuarios", []))
        emprestimos.extend(dados.get("emprestimos", []))
        historico.extend(dados.get("historico", []))
        pagamentos.extend(dados.get("pagamentos", []))

        registrar_historico("Dados carregados: " + nome)
        messagebox.showinfo("OK", "Dados carregados com sucesso!")

    Button(frame_conteudo, text="Carregar", command=carregar, bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10, sticky=E, padx=10)


def tela_estatisticas():
    limpar()
    Label(frame_conteudo, text="Estatísticas", font=("Arial", 13, "bold"), bg="white").pack(pady=10)

    total_ativos = 0
    for e in emprestimos:
        if e["status"] == "ativo":
            total_ativos = total_ativos + 1

    lista_multas = []
    for e in emprestimos:
        if e["multa"] > 0:
            lista_multas.append(e["multa"])

    soma_multas = sum(lista_multas)
    if len(lista_multas) > 0:
        media_multas = statistics.mean(lista_multas)
    else:
        media_multas = 0.0

    
    f1 = Frame(frame_conteudo, bg="white")
    f1.pack(fill=X, padx=30, pady=4)
    Label(f1, text="Total de livros:", font=("Arial", 10), bg="white", width=28, anchor=W).pack(side=LEFT)
    Label(f1, text=str(len(livros)), font=("Arial", 10, "bold"), bg="white").pack(side=LEFT)

    f2 = Frame(frame_conteudo, bg="white")
    f2.pack(fill=X, padx=30, pady=4)
    Label(f2, text="Total de usuários:", font=("Arial", 10), bg="white", width=28, anchor=W).pack(side=LEFT)
    Label(f2, text=str(len(usuarios)), font=("Arial", 10, "bold"), bg="white").pack(side=LEFT)

    f3 = Frame(frame_conteudo, bg="white")
    f3.pack(fill=X, padx=30, pady=4)
    Label(f3, text="Total de empréstimos:", font=("Arial", 10), bg="white", width=28, anchor=W).pack(side=LEFT)
    Label(f3, text=str(len(emprestimos)), font=("Arial", 10, "bold"), bg="white").pack(side=LEFT)

    f4 = Frame(frame_conteudo, bg="white")
    f4.pack(fill=X, padx=30, pady=4)
    Label(f4, text="Empréstimos ativos:", font=("Arial", 10), bg="white", width=28, anchor=W).pack(side=LEFT)
    Label(f4, text=str(total_ativos), font=("Arial", 10, "bold"), bg="white").pack(side=LEFT)

    f5 = Frame(frame_conteudo, bg="white")
    f5.pack(fill=X, padx=30, pady=4)
    Label(f5, text="Total de multas geradas:", font=("Arial", 10), bg="white", width=28, anchor=W).pack(side=LEFT)
    Label(f5, text=formatar_moeda(soma_multas), font=("Arial", 10, "bold"), bg="white").pack(side=LEFT)

    f6 = Frame(frame_conteudo, bg="white")
    f6.pack(fill=X, padx=30, pady=4)
    Label(f6, text="Média das multas:", font=("Arial", 10), bg="white", width=28, anchor=W).pack(side=LEFT)
    Label(f6, text=formatar_moeda(media_multas), font=("Arial", 10, "bold"), bg="white").pack(side=LEFT)


def tela_dados_exemplo():
    limpar()
    Label(frame_conteudo, text="Criar Dados de Exemplo", font=("Arial", 13, "bold"), bg="white").pack(pady=10)
    Label(frame_conteudo, text="Cria 2 usuários e 2 livros de exemplo para testar o sistema.", bg="white").pack(pady=5)

    def criar():
        if not messagebox.askyesno("Confirmar", "Criar dados de exemplo?"):
            return

        u1 = {
            "id": gerar_id("U"),
            "nome": "Ana Souza",
            "cpf": "111.111.111-11",
            "email": "ana@email.com",
            "telefone": "(41) 99999-1111",
            "endereco": "Rua das Flores, 100",
            "nascimento": "10/05/2005",
            "tipo": "aluno",
            "observacoes": "",
            "multa_total": 0.0,
            "ativo": True
        }
        u2 = {
            "id": gerar_id("U"),
            "nome": "Bruno Lima",
            "cpf": "222.222.222-22",
            "email": "bruno@email.com",
            "telefone": "(41) 99999-2222",
            "endereco": "Av. Central, 200",
            "nascimento": "22/08/2004",
            "tipo": "aluno",
            "observacoes": "",
            "multa_total": 0.0,
            "ativo": True
        }
        l1 = {
            "id": gerar_id("L"),
            "titulo": "Python para Iniciantes",
            "autor": "Carlos Silva",
            "ano": 2022,
            "isbn": "978-0000-1",
            "categoria": "Programação",
            "editora": "Editora Tech",
            "quantidade_total": 3,
            "quantidade_disponivel": 3,
            "prateleira": "A1",
            "palavras_chave": "python",
            "observacoes": "",
            "ativo": True
        }
        l2 = {
            "id": gerar_id("L"),
            "titulo": "Algoritmos e Estruturas",
            "autor": "Maria Costa",
            "ano": 2021,
            "isbn": "978-0000-2",
            "categoria": "Computação",
            "editora": "Ed. Academica",
            "quantidade_total": 2,
            "quantidade_disponivel": 2,
            "prateleira": "B2",
            "palavras_chave": "algoritmos",
            "observacoes": "",
            "ativo": True
        }

        usuarios.append(u1)
        usuarios.append(u2)
        livros.append(l1)
        livros.append(l2)

        registrar_historico("Dados de exemplo criados")
        messagebox.showinfo("OK", "Dados de exemplo criados!\nUse 'Listar Usuários' e 'Listar Livros' para ver.")

    Button(frame_conteudo, text="Criar Dados de Exemplo", command=criar, bg="#4CAF50", fg="white").pack(pady=10)


