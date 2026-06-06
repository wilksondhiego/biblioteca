📚 Sistema de Biblioteca em Python

✨ Projeto Final da disciplina de Raciocínio Algorítmico, curso de Engenharia de Software da PUCPR, semestre 2026/1.

👩‍🏫 Professores: Lisiane Reips e Giulio Bordin

---

🏛️ Descrição

O sistema simula o funcionamento de uma biblioteca real, onde o usuário assume o papel de bibliotecário. É possível cadastrar livros e usuários, realizar empréstimos, registrar devoluções, calcular multas por atraso e gerar relatórios completos da situação da biblioteca.

O projeto foi desenvolvido em duas versões:

🖥️ A primeira é o arquivo **biblioteca.py**, que roda diretamente no terminal e usa input e print para toda a interação com o usuário.

🪟 A segunda é o arquivo **bibliotecaTK.py**, que possui uma interface gráfica construída com a biblioteca Tkinter, com janelas, botões e formulários.


▶️ Como executar

Para rodar o projeto é necessário ter o **Python 3.8 ou superior** instalado. O Tkinter já vem junto com o Python e não precisa ser instalado separadamente.

🟢 Para rodar a versão terminal, execute no prompt de comando:
```
python biblioteca.py
```

🟣 Para rodar a versão com interface gráfica, execute:
```
python bibliotecaTK.py
```

---

⚙️ Funcionalidades

👤 O sistema permite cadastrar usuários informando nome, CPF, e-mail, telefone, endereço e tipo (aluno, professor ou comunidade).

📖 Também é possível cadastrar livros com título, autor, ISBN, categoria, editora, quantidade de exemplares e localização na prateleira.

🔄 O controle de empréstimos verifica automaticamente se o usuário já atingiu o limite de 3 livros emprestados e se o livro está disponível. O prazo padrão de devolução é de 7 dias.

💸 Caso o livro seja devolvido com atraso, o sistema calcula automaticamente a multa de R$ 5,00 por dia de atraso.

📄 Ao encerrar o sistema, um relatório completo é salvo automaticamente em um arquivo .txt dentro da pasta relatorios, com data e hora no nome do arquivo.

💾 Também é possível salvar e carregar todos os dados em formato .json para não perder as informações entre sessões.


📦 Módulos utilizados

🔹 **os** — limpar a tela no terminal

🔹 **json** — salvar e carregar os dados em arquivo

🔹 **random** — gerar IDs únicos para livros e usuários

🔹 **statistics** — calcular a média das multas na tela de estatísticas

🔹 **textwrap** — formatar o texto dos relatórios

🔹 **datetime** — controlar as datas de empréstimo e calcular os dias de atraso

🔹 **pathlib** — criar pastas e montar os caminhos dos arquivos

🔹 **tkinter** — construir toda a interface gráfica da versão com janelas



 🗂️ Histórico de desenvolvimento

O projeto foi desenvolvido em etapas e cada etapa foi commitada separadamente no GitHub.

🔸 **Commit 1** — Criou a estrutura base do código com as constantes e variáveis globais.

🔸 **Commit 2** — Adicionou as funções de cadastro e listagem de usuários.

🔸 **Commit 3** — Incluiu o cadastro, listagem e busca de livros.

🔸 **Commit 4** — Implementou o empréstimo, devolução e renovação.

🔸 **Commit 5** — Adicionou o cálculo de multas e o registro de pagamentos.

🔸 **Commit 6** — Criou a geração e salvamento do relatório em arquivo .txt.

🔸 **Commit 7** — Adicionou a remoção de livros e usuários.

🔸 **Commit 8** — Finalizou o menu principal, a interface gráfica completa e o encerramento do sistema.

---

✅ Requisitos atendidos

✔️ **Requisito 1** — Fluxo com introdução, desenvolvimento e fim: atendido com a mensagem de boas-vindas na tela inicial, o menu de operações como desenvolvimento e o encerramento com geração de relatório.

✔️ **Requisito 2** — Entrada e saída de dados: atendido com mais de 30 campos de entrada espalhados pelos formulários da interface.

✔️ **Requisito 3** — Variáveis e constantes: atendido com as constantes LIMITE_EMPRESTIMOS, PRAZO_DIAS e MULTA_POR_DIA, além das variáveis globais livros, usuarios, emprestimos, historico e pagamentos.

✔️ **Requisito 4** — Operações aritméticas: atendido com o cálculo da multa por dia de atraso, atualização da quantidade disponível de livros e contagem de empréstimos ativos.

✔️ **Requisito 5** — Estruturas condicionais: atendido com condicionais que verificam disponibilidade do livro, limite de empréstimos do usuário e se a devolução está em atraso.

✔️ **Requisito 6** — Estruturas de repetição: atendido com loops que percorrem as listas de livros, usuários e empréstimos para buscar e exibir informações.

✔️ **Requisito 7** — Listas: atendido com as listas livros, usuarios, emprestimos, historico e pagamentos.

✔️ **Requisito 8** — Dicionários: atendido pois cada livro, usuário e empréstimo é armazenado como um dicionário com todos os seus campos.

✔️ **Requisito 9** — Funções e modularização: atendido com mais de 15 funções, uma para cada tela e operação do sistema.

✔️ **Requisito 10** — Imports: atendido com 6 módulos importados: json, random, statistics, tkinter, datetime e pathlib.

✔️ **Requisito 11** — Manipulação de arquivos: atendido com o salvamento automático do relatório em .txt ao encerrar o sistema.

✔️ **Requisito 12** — GitHub: atendido com o repositório contendo commits por etapa e este README explicativo.


