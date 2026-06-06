
import os
import json
import random
import statistics
import textwrap
from datetime import date, datetime, timedelta
from pathlib import Path
from tkinter import*

LIMITE_EMPRESTIMOS = 3
PRAZO_EMPRESTIMO_DIAS = 7
MULTA_POR_DIA = 5.00
NOME_BIBLIOTECA = "Biblioteca RA"
ARQUIVO_DADOS_PADRAO = "dados_biblioteca.json"
PASTA_RELATORIOS = "relatorios"

livros = []
usuarios = []
emprestimos = []
historico = []
pagamentos = []


def limpar_tela():
    """Limpa a tela do terminal quando possível."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa para o usuário conseguir ler as mensagens."""
    input("\nPressione ENTER para continuar...")


def mostrar_introducao():
    """Mostra a introdução do sistema."""
    print("=" * 70)
    print(f"Bem-vindo ao sistema {NOME_BIBLIOTECA}!")
    print("=" * 70)
    print(textwrap.dedent(f"""
    Você é o bibliotecário responsável por organizar a biblioteca.
    O sistema permite cadastrar usuários, cadastrar livros, realizar empréstimos,
    controlar devoluções, calcular multas por atraso, registrar pagamentos e
    gerar relatórios em arquivo .txt.

    Regras principais:
    - Cada usuário pode ter até {LIMITE_EMPRESTIMOS} empréstimos ativos.
    - O prazo de empréstimo é de {PRAZO_EMPRESTIMO_DIAS} dias.
    - A multa por atraso é de R$ {MULTA_POR_DIA:.2f} por dia.
    """))


def mostrar_menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 70)
    print("MENU PRINCIPAL - SISTEMA DE BIBLIOTECA")
    print("=" * 70)
    print("1  - Cadastrar usuário")
    print("2  - Listar usuários")
    print("3  - Cadastrar livro")
    print("4  - Listar livros")
    print("5  - Buscar livro")
    print("6  - Realizar empréstimo")
    print("7  - Listar empréstimos")
    print("8  - Devolver livro")
    print("9  - Renovar empréstimo")
    print("10 - Consultar multas de usuário")
    print("11 - Pagar multa")
    print("12 - Remover livro")
    print("13 - Remover usuário")
    print("14 - Mostrar relatório na tela")
    print("15 - Salvar relatório em .txt")
    print("16 - Salvar dados em JSON")
    print("17 - Carregar dados de JSON")
    print("18 - Ver estatísticas")
    print("19 - Criar dados de exemplo")
    print("0  - Finalizar sistema")


def gerar_id(prefixo):
    """Gera um ID simples com prefixo, data e número aleatório."""
    numero = random.randint(1000, 9999)
    instante = datetime.now().strftime("%H%M%S")
    return f"{prefixo}{instante}{numero}"


def registrar_historico(acao):
    """Guarda uma ação feita pelo usuário no histórico."""
    historico.append({
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "acao": acao
    })


def converter_data(texto, usar_hoje_se_vazio=True):
    """Converte uma data no formato dd/mm/aaaa para date."""
    texto = texto.strip()
    if texto == "" and usar_hoje_se_vazio:
        return date.today()
    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except ValueError:
        print("Data inválida. Será usada a data de hoje.")
        return date.today()


def formatar_moeda(valor):
    """Formata um número como valor em reais."""
    return f"R$ {valor:.2f}".replace(".", ",")


def encontrar_usuario(id_usuario):
    """Procura um usuário pelo ID."""
    for usuario in usuarios:
        if usuario["id"] == id_usuario:
            return usuario
    return None


def encontrar_livro(id_livro):
    """Procura um livro pelo ID."""
    for livro in livros:
        if livro["id"] == id_livro:
            return livro
    return None


def encontrar_emprestimo(id_emprestimo):
    """Procura um empréstimo pelo ID."""
    for emprestimo in emprestimos:
        if emprestimo["id"] == id_emprestimo:
            return emprestimo
    return None


def contar_emprestimos_ativos(id_usuario):
    """Conta quantos empréstimos ativos um usuário possui."""
    total = 0
    for emprestimo in emprestimos:
        if emprestimo["id_usuario"] == id_usuario and emprestimo["status"] == "ativo":
            total += 1
    return total


def calcular_multa(data_devolucao, data_prevista):
    """Calcula multa de acordo com a quantidade de dias de atraso."""
    dias_atraso = (data_devolucao - data_prevista).days
    if dias_atraso > 0:
        return dias_atraso, dias_atraso * MULTA_POR_DIA
    return 0, 0.0


def atualizar_situacao_emprestimos():
    """Atualiza empréstimos ativos para indicar atraso quando o prazo venceu."""
    hoje = date.today()
    for emprestimo in emprestimos:
        if emprestimo["status"] == "ativo":
            data_prevista = datetime.strptime(emprestimo["data_prevista"], "%Y-%m-%d").date()
            if hoje > data_prevista:
                emprestimo["situacao"] = "atrasado"
            else:
                emprestimo["situacao"] = "dentro do prazo"


def cadastrar_usuario():
    """Cadastra um novo usuário da biblioteca."""
    print("\nCADASTRO DE USUÁRIO")
    nome = input("Digite o nome completo do usuário: ").strip()
    cpf = input("Digite o CPF do usuário: ").strip()
    email = input("Digite o e-mail do usuário: ").strip()
    telefone = input("Digite o telefone do usuário: ").strip()
    endereco = input("Digite o endereço do usuário: ").strip()
    nascimento = input("Digite a data de nascimento do usuário (dd/mm/aaaa): ").strip()
    tipo = input("Digite o tipo de usuário (aluno/professor/comunidade): ").strip().lower()
    observacoes = input("Digite observações sobre o usuário (ou deixe vazio): ").strip()

    if nome == "" or cpf == "":
        print("Nome e CPF são obrigatórios. Cadastro cancelado.")
        return

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe um usuário cadastrado com esse CPF.")
            return

    usuario = {
        "id": gerar_id("U"),
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "telefone": telefone,
        "endereco": endereco,
        "nascimento": nascimento,
        "tipo": tipo,
        "observacoes": observacoes,
        "multa_total": 0.0,
        "ativo": True
    }
    usuarios.append(usuario)
    registrar_historico(f"Usuário cadastrado: {nome}")
    print(f"Usuário cadastrado com sucesso! ID: {usuario['id']}")


def listar_usuarios():
    """Lista todos os usuários cadastrados."""
    print("\nUSUÁRIOS CADASTRADOS")
    if len(usuarios) == 0:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:
        status = "ativo" if usuario["ativo"] else "removido"
        ativos = contar_emprestimos_ativos(usuario["id"])
        print("-" * 70)
        print(f"ID: {usuario['id']}")
        print(f"Nome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf']} | Tipo: {usuario['tipo']} | Status: {status}")
        print(f"E-mail: {usuario['email']} | Telefone: {usuario['telefone']}")
        print(f"Empréstimos ativos: {ativos}/{LIMITE_EMPRESTIMOS}")
        print(f"Multa em aberto: {formatar_moeda(usuario['multa_total'])}")


def cadastrar_livro():
    """Cadastra um novo livro no acervo."""
    print("\nCADASTRO DE LIVRO")
    titulo = input("Digite o título do livro: ").strip()
    autor = input("Digite o autor do livro: ").strip()
    ano_texto = input("Digite o ano de publicação: ").strip()
    isbn = input("Digite o ISBN ou código do livro: ").strip()
    categoria = input("Digite a categoria/gênero do livro: ").strip()
    editora = input("Digite a editora do livro: ").strip()
    quantidade_texto = input("Digite a quantidade de exemplares: ").strip()
    prateleira = input("Digite a prateleira/localização: ").strip()
    palavras_chave = input("Digite palavras-chave separadas por vírgula: ").strip()
    observacoes = input("Digite observações do livro (ou deixe vazio): ").strip()

    if titulo == "" or autor == "":
        print("Título e autor são obrigatórios. Cadastro cancelado.")
        return

    try:
        ano = int(ano_texto)
    except ValueError:
        ano = 0

    try:
        quantidade = int(quantidade_texto)
    except ValueError:
        quantidade = 1

    if quantidade < 1:
        quantidade = 1

    livro = {
        "id": gerar_id("L"),
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "isbn": isbn,
        "categoria": categoria,
        "editora": editora,
        "quantidade_total": quantidade,
        "quantidade_disponivel": quantidade,
        "prateleira": prateleira,
        "palavras_chave": palavras_chave,
        "observacoes": observacoes,
        "ativo": True
    }
    livros.append(livro)
    registrar_historico(f"Livro cadastrado: {titulo}")
    print(f"Livro cadastrado com sucesso! ID: {livro['id']}")


def listar_livros():
    """Lista todos os livros cadastrados."""
    print("\nLIVROS CADASTRADOS")
    if len(livros) == 0:
        print("Nenhum livro cadastrado.")
        return

    for livro in livros:
        status = "ativo" if livro["ativo"] else "removido"
        print("-" * 70)
        print(f"ID: {livro['id']}")
        print(f"Título: {livro['titulo']} | Autor: {livro['autor']} | Ano: {livro['ano']}")
        print(f"Categoria: {livro['categoria']} | Editora: {livro['editora']} | Status: {status}")
        print(f"Disponíveis: {livro['quantidade_disponivel']}/{livro['quantidade_total']}")
        print(f"Prateleira: {livro['prateleira']} | ISBN: {livro['isbn']}")


def buscar_livro():
    """Busca livros por título, autor, categoria ou palavra-chave."""
    print("\nBUSCAR LIVRO")
    termo = input("Digite o termo de busca: ").strip().lower()
    encontrados = []

    for livro in livros:
        texto = f"{livro['titulo']} {livro['autor']} {livro['categoria']} {livro['palavras_chave']}".lower()
        if termo in texto and livro["ativo"]:
            encontrados.append(livro)

    if len(encontrados) == 0:
        print("Nenhum livro encontrado.")
    else:
        print(f"Foram encontrados {len(encontrados)} livro(s):")
        for livro in encontrados:
            print("-" * 70)
            print(f"ID: {livro['id']} | {livro['titulo']} - {livro['autor']}")
            print(f"Disponíveis: {livro['quantidade_disponivel']}")


def emprestar_livro():
    """Realiza empréstimo de livro para usuário."""
    print("\nREALIZAR EMPRÉSTIMO")
    if len(usuarios) == 0 or len(livros) == 0:
        print("É necessário ter pelo menos um usuário e um livro cadastrados.")
        return

    id_usuario = input("Digite o ID do usuário: ").strip()
    id_livro = input("Digite o ID do livro: ").strip()
    data_texto = input("Digite a data do empréstimo (dd/mm/aaaa) ou deixe vazio para hoje: ").strip()
    observacao = input("Digite uma observação para o empréstimo (ou deixe vazio): ").strip()

    usuario = encontrar_usuario(id_usuario)
    livro = encontrar_livro(id_livro)

    if usuario is None:
        print("Usuário não encontrado.")
        return
    elif not usuario["ativo"]:
        print("Usuário removido/inativo. Empréstimo não permitido.")
        return
    elif usuario["multa_total"] > 0:
        print("Usuário possui multa em aberto. Quite a multa antes de emprestar.")
        return

    if livro is None:
        print("Livro não encontrado.")
        return
    elif not livro["ativo"]:
        print("Livro removido/inativo. Empréstimo não permitido.")
        return
    elif livro["quantidade_disponivel"] <= 0:
        print("Livro indisponível no momento.")
        return

    total_ativos = contar_emprestimos_ativos(id_usuario)
    if total_ativos >= LIMITE_EMPRESTIMOS:
        print(f"Limite de {LIMITE_EMPRESTIMOS} empréstimos atingido.")
        return

    data_emprestimo = converter_data(data_texto)
    data_prevista = data_emprestimo + timedelta(days=PRAZO_EMPRESTIMO_DIAS)

    emprestimo = {
        "id": gerar_id("E"),
        "id_usuario": usuario["id"],
        "nome_usuario": usuario["nome"],
        "id_livro": livro["id"],
        "titulo_livro": livro["titulo"],
        "data_emprestimo": data_emprestimo.isoformat(),
        "data_prevista": data_prevista.isoformat(),
        "data_devolucao": "",
        "status": "ativo",
        "situacao": "dentro do prazo",
        "dias_atraso": 0,
        "multa": 0.0,
        "renovacoes": 0,
        "observacao": observacao
    }
    emprestimos.append(emprestimo)
    livro["quantidade_disponivel"] -= 1
    registrar_historico(f"Empréstimo realizado: {livro['titulo']} para {usuario['nome']}")
    print("Empréstimo realizado com sucesso!")
    print(f"ID do empréstimo: {emprestimo['id']}")
    print(f"Devolução prevista: {data_prevista.strftime('%d/%m/%Y')}")


def listar_emprestimos():
    """Lista todos os empréstimos registrados."""
    atualizar_situacao_emprestimos()
    print("\nEMPRÉSTIMOS REGISTRADOS")
    if len(emprestimos) == 0:
        print("Nenhum empréstimo registrado.")
        return

    for emprestimo in emprestimos:
        data_prevista = datetime.strptime(emprestimo["data_prevista"], "%Y-%m-%d").date()
        print("-" * 70)
        print(f"ID: {emprestimo['id']}")
        print(f"Usuário: {emprestimo['nome_usuario']} | Livro: {emprestimo['titulo_livro']}")
        print(f"Status: {emprestimo['status']} | Situação: {emprestimo['situacao']}")
        print(f"Data prevista: {data_prevista.strftime('%d/%m/%Y')}")
        print(f"Renovações: {emprestimo['renovacoes']} | Multa: {formatar_moeda(emprestimo['multa'])}")


def devolver_livro():
    """Registra devolução de livro e calcula multa, se houver."""
    print("\nDEVOLVER LIVRO")
    id_emprestimo = input("Digite o ID do empréstimo: ").strip()
    data_texto = input("Digite a data da devolução (dd/mm/aaaa) ou deixe vazio para hoje: ").strip()
    confirmar = input("Confirmar devolução? (s/n): ").strip().lower()
    observacao = input("Digite uma observação da devolução (ou deixe vazio): ").strip()

    if confirmar != "s":
        print("Devolução cancelada.")
        return

    emprestimo = encontrar_emprestimo(id_emprestimo)
    if emprestimo is None:
        print("Empréstimo não encontrado.")
        return
    elif emprestimo["status"] != "ativo":
        print("Esse empréstimo já foi devolvido.")
        return

    livro = encontrar_livro(emprestimo["id_livro"])
    usuario = encontrar_usuario(emprestimo["id_usuario"])
    data_devolucao = converter_data(data_texto)
    data_prevista = datetime.strptime(emprestimo["data_prevista"], "%Y-%m-%d").date()
    dias_atraso, multa = calcular_multa(data_devolucao, data_prevista)

    emprestimo["data_devolucao"] = data_devolucao.isoformat()
    emprestimo["status"] = "devolvido"
    emprestimo["situacao"] = "devolvido com atraso" if dias_atraso > 0 else "devolvido no prazo"
    emprestimo["dias_atraso"] = dias_atraso
    emprestimo["multa"] = multa
    emprestimo["observacao"] += f" | Devolução: {observacao}"

    if livro is not None:
        livro["quantidade_disponivel"] += 1

    if usuario is not None:
        usuario["multa_total"] += multa

    registrar_historico(f"Livro devolvido: {emprestimo['titulo_livro']} por {emprestimo['nome_usuario']}")
    print("Devolução registrada com sucesso!")
    if multa > 0:
        print(f"Atraso de {dias_atraso} dia(s). Multa gerada: {formatar_moeda(multa)}")
    else:
        print("Livro devolvido dentro do prazo. Nenhuma multa gerada.")


def renovar_emprestimo():
    """Renova o prazo de um empréstimo ativo."""
    print("\nRENOVAR EMPRÉSTIMO")
    id_emprestimo = input("Digite o ID do empréstimo que deseja renovar: ").strip()
    confirmar = input("Confirmar renovação por mais 7 dias? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Renovação cancelada.")
        return

    emprestimo = encontrar_emprestimo(id_emprestimo)
    if emprestimo is None:
        print("Empréstimo não encontrado.")
        return
    elif emprestimo["status"] != "ativo":
        print("Não é possível renovar um empréstimo já devolvido.")
        return
    elif emprestimo["renovacoes"] >= 2:
        print("Limite de 2 renovações atingido.")
        return

    data_prevista = datetime.strptime(emprestimo["data_prevista"], "%Y-%m-%d").date()
    nova_data = data_prevista + timedelta(days=PRAZO_EMPRESTIMO_DIAS)
    emprestimo["data_prevista"] = nova_data.isoformat()
    emprestimo["renovacoes"] += 1
    emprestimo["situacao"] = "dentro do prazo"
    registrar_historico(f"Empréstimo renovado: {emprestimo['id']}")
    print(f"Empréstimo renovado! Nova data prevista: {nova_data.strftime('%d/%m/%Y')}")


def consultar_multas():
    """Mostra as multas de um usuário."""
    print("\nCONSULTAR MULTAS")
    id_usuario = input("Digite o ID do usuário: ").strip()
    usuario = encontrar_usuario(id_usuario)

    if usuario is None:
        print("Usuário não encontrado.")
        return

    print(f"Usuário: {usuario['nome']}")
    print(f"Multa total em aberto: {formatar_moeda(usuario['multa_total'])}")
    print("Empréstimos com multa:")
    achou = False
    for emprestimo in emprestimos:
        if emprestimo["id_usuario"] == id_usuario and emprestimo["multa"] > 0:
            achou = True
            print(f"- {emprestimo['titulo_livro']} | Dias de atraso: {emprestimo['dias_atraso']} | Multa: {formatar_moeda(emprestimo['multa'])}")
    if not achou:
        print("Nenhum empréstimo com multa registrado.")


def pagar_multa():
    """Registra pagamento de multa de usuário."""
    print("\nPAGAR MULTA")
    id_usuario = input("Digite o ID do usuário: ").strip()
    valor_texto = input("Digite o valor pago: R$ ").replace(",", ".").strip()
    forma_pagamento = input("Digite a forma de pagamento (dinheiro/pix/cartão): ").strip()
    observacao = input("Digite uma observação do pagamento (ou deixe vazio): ").strip()

    usuario = encontrar_usuario(id_usuario)
    if usuario is None:
        print("Usuário não encontrado.")
        return

    try:
        valor = float(valor_texto)
    except ValueError:
        print("Valor inválido.")
        return

    if valor <= 0:
        print("O valor precisa ser maior que zero.")
        return
    elif usuario["multa_total"] <= 0:
        print("Esse usuário não possui multa em aberto.")
        return

    valor_abatido = min(valor, usuario["multa_total"])
    usuario["multa_total"] -= valor_abatido
    pagamento = {
        "id": gerar_id("P"),
        "id_usuario": usuario["id"],
        "nome_usuario": usuario["nome"],
        "valor": valor_abatido,
        "forma_pagamento": forma_pagamento,
        "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "observacao": observacao
    }
    pagamentos.append(pagamento)
    registrar_historico(f"Pagamento de multa: {usuario['nome']} - {formatar_moeda(valor_abatido)}")
    print(f"Pagamento registrado: {formatar_moeda(valor_abatido)}")
    print(f"Saldo de multa restante: {formatar_moeda(usuario['multa_total'])}")


def remover_livro():
    """Remove logicamente um livro do acervo."""
    print("\nREMOVER LIVRO")
    id_livro = input("Digite o ID do livro: ").strip()
    confirmar = input("Confirmar remoção do livro? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Remoção cancelada.")
        return

    livro = encontrar_livro(id_livro)
    if livro is None:
        print("Livro não encontrado.")
        return

    for emprestimo in emprestimos:
        if emprestimo["id_livro"] == id_livro and emprestimo["status"] == "ativo":
            print("Não é possível remover um livro com empréstimo ativo.")
            return

    livro["ativo"] = False
    registrar_historico(f"Livro removido: {livro['titulo']}")
    print("Livro removido do acervo ativo.")


def remover_usuario():
    """Remove logicamente um usuário."""
    print("\nREMOVER USUÁRIO")
    id_usuario = input("Digite o ID do usuário: ").strip()
    confirmar = input("Confirmar remoção do usuário? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Remoção cancelada.")
        return

    usuario = encontrar_usuario(id_usuario)
    if usuario is None:
        print("Usuário não encontrado.")
        return

    if contar_emprestimos_ativos(id_usuario) > 0:
        print("Não é possível remover usuário com empréstimos ativos.")
        return

    usuario["ativo"] = False
    registrar_historico(f"Usuário removido: {usuario['nome']}")
    print("Usuário removido do cadastro ativo.")


def calcular_estatisticas():
    """Calcula estatísticas gerais da biblioteca."""
    total_livros = len(livros)
    total_usuarios = len(usuarios)
    total_emprestimos = len(emprestimos)
    emprestimos_ativos = 0
    multas = []

    for emprestimo in emprestimos:
        if emprestimo["status"] == "ativo":
            emprestimos_ativos += 1
        if emprestimo["multa"] > 0:
            multas.append(emprestimo["multa"])

    total_multas = sum(multas)
    media_multas = statistics.mean(multas) if len(multas) > 0 else 0.0

    return {
        "total_livros": total_livros,
        "total_usuarios": total_usuarios,
        "total_emprestimos": total_emprestimos,
        "emprestimos_ativos": emprestimos_ativos,
        "total_multas": total_multas,
        "media_multas": media_multas
    }


def mostrar_estatisticas():
    """Mostra as estatísticas calculadas."""
    estatisticas = calcular_estatisticas()
    print("\nESTATÍSTICAS DA BIBLIOTECA")
    print("-" * 70)
    print(f"Total de livros cadastrados: {estatisticas['total_livros']}")
    print(f"Total de usuários cadastrados: {estatisticas['total_usuarios']}")
    print(f"Total de empréstimos registrados: {estatisticas['total_emprestimos']}")
    print(f"Empréstimos ativos: {estatisticas['emprestimos_ativos']}")
    print(f"Total de multas geradas: {formatar_moeda(estatisticas['total_multas'])}")
    print(f"Média das multas geradas: {formatar_moeda(estatisticas['media_multas'])}")


def montar_relatorio():
    """Monta o texto do relatório geral da biblioteca."""
    atualizar_situacao_emprestimos()
    estatisticas = calcular_estatisticas()
    linhas = []
    linhas.append("=" * 80)
    linhas.append(f"RELATÓRIO GERAL - {NOME_BIBLIOTECA}")
    linhas.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    linhas.append("=" * 80)
    linhas.append("")
    linhas.append("1. ESTATÍSTICAS GERAIS")
    linhas.append(f"Total de livros: {estatisticas['total_livros']}")
    linhas.append(f"Total de usuários: {estatisticas['total_usuarios']}")
    linhas.append(f"Total de empréstimos: {estatisticas['total_emprestimos']}")
    linhas.append(f"Empréstimos ativos: {estatisticas['emprestimos_ativos']}")
    linhas.append(f"Total de multas geradas: {formatar_moeda(estatisticas['total_multas'])}")
    linhas.append(f"Média das multas: {formatar_moeda(estatisticas['media_multas'])}")
    linhas.append("")

    linhas.append("2. LIVROS")
    if len(livros) == 0:
        linhas.append("Nenhum livro cadastrado.")
    else:
        for livro in livros:
            linhas.append(f"- {livro['id']} | {livro['titulo']} | {livro['autor']} | Disponíveis: {livro['quantidade_disponivel']}/{livro['quantidade_total']}")
    linhas.append("")

    linhas.append("3. USUÁRIOS")
    if len(usuarios) == 0:
        linhas.append("Nenhum usuário cadastrado.")
    else:
        for usuario in usuarios:
            linhas.append(f"- {usuario['id']} | {usuario['nome']} | Multa: {formatar_moeda(usuario['multa_total'])} | Ativo: {usuario['ativo']}")
    linhas.append("")

    linhas.append("4. EMPRÉSTIMOS")
    if len(emprestimos) == 0:
        linhas.append("Nenhum empréstimo registrado.")
    else:
        for emprestimo in emprestimos:
            linhas.append(f"- {emprestimo['id']} | {emprestimo['nome_usuario']} pegou '{emprestimo['titulo_livro']}' | Status: {emprestimo['status']} | Situação: {emprestimo['situacao']} | Multa: {formatar_moeda(emprestimo['multa'])}")
    linhas.append("")

    linhas.append("5. PAGAMENTOS DE MULTA")
    if len(pagamentos) == 0:
        linhas.append("Nenhum pagamento registrado.")
    else:
        for pagamento in pagamentos:
            linhas.append(f"- {pagamento['data_hora']} | {pagamento['nome_usuario']} | {formatar_moeda(pagamento['valor'])} | {pagamento['forma_pagamento']}")
    linhas.append("")

    linhas.append("6. HISTÓRICO DO SISTEMA")
    if len(historico) == 0:
        linhas.append("Nenhuma ação registrada.")
    else:
        for item in historico[-30:]:
            linhas.append(f"- {item['data_hora']} | {item['acao']}")

    linhas.append("\nFim do relatório.")
    return "\n".join(linhas)


def mostrar_relatorio():
    """Mostra o relatório na tela."""
    print("\n" + montar_relatorio())


def salvar_relatorio_txt():
    """Salva o relatório em um arquivo .txt."""
    print("\nSALVAR RELATÓRIO")
    nome_arquivo = input("Digite o nome do arquivo .txt ou deixe vazio para automático: ").strip()
    incluir_historico = input("Deseja incluir histórico das últimas ações? (s/n): ").strip().lower()
    confirmar = input("Confirmar geração do relatório? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Geração de relatório cancelada.")
        return None

    Path(PASTA_RELATORIOS).mkdir(exist_ok=True)
    if nome_arquivo == "":
        nome_arquivo = f"relatorio_biblioteca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    if not nome_arquivo.endswith(".txt"):
        nome_arquivo += ".txt"

    caminho = Path(PASTA_RELATORIOS) / nome_arquivo
    relatorio = montar_relatorio()
    if incluir_historico != "s":
        partes = relatorio.split("6. HISTÓRICO DO SISTEMA")
        relatorio = partes[0] + "\n6. HISTÓRICO DO SISTEMA\nHistórico ocultado por escolha do usuário.\n"

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)

    registrar_historico(f"Relatório salvo em {caminho}")
    print(f"Relatório salvo com sucesso em: {caminho}")
    return caminho


def salvar_relatorio_automatico():
    """Salva um relatório automaticamente no encerramento do sistema."""
    Path(PASTA_RELATORIOS).mkdir(exist_ok=True)
    caminho = Path(PASTA_RELATORIOS) / f"relatorio_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(montar_relatorio())
    return caminho


def salvar_dados_json():
    """Salva os dados do sistema em JSON."""
    print("\nSALVAR DADOS")
    nome_arquivo = input("Digite o nome do arquivo JSON ou deixe vazio para padrão: ").strip()
    if nome_arquivo == "":
        nome_arquivo = ARQUIVO_DADOS_PADRAO
    if not nome_arquivo.endswith(".json"):
        nome_arquivo += ".json"

    dados = {
        "livros": livros,
        "usuarios": usuarios,
        "emprestimos": emprestimos,
        "historico": historico,
        "pagamentos": pagamentos
    }
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    registrar_historico(f"Dados salvos em {nome_arquivo}")
    print(f"Dados salvos com sucesso em {nome_arquivo}.")


def carregar_dados_json():
    """Carrega os dados do sistema a partir de JSON."""
    print("\nCARREGAR DADOS")
    nome_arquivo = input("Digite o nome do arquivo JSON ou deixe vazio para padrão: ").strip()
    if nome_arquivo == "":
        nome_arquivo = ARQUIVO_DADOS_PADRAO

    if not Path(nome_arquivo).exists():
        print("Arquivo não encontrado.")
        return

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

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

    registrar_historico(f"Dados carregados de {nome_arquivo}")
    print("Dados carregados com sucesso!")


def criar_dados_exemplo():
    """Cria dados de exemplo para testar o sistema rapidamente."""
    print("\nCRIAR DADOS DE EXEMPLO")
    confirmar = input("Deseja criar usuários, livros e empréstimos de exemplo? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Operação cancelada.")
        return

    usuario1 = {
        "id": gerar_id("U"),
        "nome": "Ana Souza",
        "cpf": "111.111.111-11",
        "email": "ana@email.com",
        "telefone": "(41) 99999-1111",
        "endereco": "Rua das Flores, 100",
        "nascimento": "10/05/2005",
        "tipo": "aluno",
        "observacoes": "Usuária exemplo",
        "multa_total": 0.0,
        "ativo": True
    }
    usuario2 = {
        "id": gerar_id("U"),
        "nome": "Bruno Lima",
        "cpf": "222.222.222-22",
        "email": "bruno@email.com",
        "telefone": "(41) 99999-2222",
        "endereco": "Av. Central, 200",
        "nascimento": "22/08/2004",
        "tipo": "aluno",
        "observacoes": "Usuário exemplo",
        "multa_total": 0.0,
        "ativo": True
    }
    livro1 = {
        "id": gerar_id("L"),
        "titulo": "Python para Iniciantes",
        "autor": "Carlos Silva",
        "ano": 2022,
        "isbn": "978-1-0000-0000-1",
        "categoria": "Programação",
        "editora": "Editora Tech",
        "quantidade_total": 3,
        "quantidade_disponivel": 3,
        "prateleira": "A1",
        "palavras_chave": "python, programação, lógica",
        "observacoes": "Livro exemplo",
        "ativo": True
    }
    livro2 = {
        "id": gerar_id("L"),
        "titulo": "Algoritmos e Estruturas",
        "autor": "Maria Costa",
        "ano": 2021,
        "isbn": "978-1-0000-0000-2",
        "categoria": "Computação",
        "editora": "Editora Acadêmica",
        "quantidade_total": 2,
        "quantidade_disponivel": 2,
        "prateleira": "B2",
        "palavras_chave": "algoritmos, listas, dicionários",
        "observacoes": "Livro exemplo",
        "ativo": True
    }
    usuarios.extend([usuario1, usuario2])
    livros.extend([livro1, livro2])
    registrar_historico("Dados de exemplo criados")
    print("Dados de exemplo criados com sucesso!")
    print("Use a opção 2 para ver usuários e a opção 4 para ver livros.")


def executar_sistema():
    """Executa o loop principal do sistema."""
    mostrar_introducao()

    while True:
        mostrar_menu()
        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            cadastrar_usuario()
            pausar()
        elif opcao == "2":
            listar_usuarios()
            pausar()
        elif opcao == "3":
            cadastrar_livro()
            pausar()
        elif opcao == "4":
            listar_livros()
            pausar()
        elif opcao == "5":
            buscar_livro()
            pausar()
        elif opcao == "6":
            emprestar_livro()
            pausar()
        elif opcao == "7":
            listar_emprestimos()
            pausar()
        elif opcao == "8":
            devolver_livro()
            pausar()
        elif opcao == "9":
            renovar_emprestimo()
            pausar()
        elif opcao == "10":
            consultar_multas()
            pausar()
        elif opcao == "11":
            pagar_multa()
            pausar()
        elif opcao == "12":
            remover_livro()
            pausar()
        elif opcao == "13":
            remover_usuario()
            pausar()
        elif opcao == "14":
            mostrar_relatorio()
            pausar()
        elif opcao == "15":
            salvar_relatorio_txt()
            pausar()
        elif opcao == "16":
            salvar_dados_json()
            pausar()
        elif opcao == "17":
            carregar_dados_json()
            pausar()
        elif opcao == "18":
            mostrar_estatisticas()
            pausar()
        elif opcao == "19":
            criar_dados_exemplo()
            pausar()
        elif opcao == "0":
            caminho = salvar_relatorio_automatico()
            print("\nEncerrando o sistema...")
            print(f"Relatório final salvo automaticamente em: {caminho}")
            print("Obrigado por utilizar o Sistema de Biblioteca. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
            pausar()


if __name__ == "__main__":
    executar_sistema()


