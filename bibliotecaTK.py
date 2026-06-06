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
