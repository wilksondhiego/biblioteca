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
