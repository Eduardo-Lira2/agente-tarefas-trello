# Agente de Tarefas com Trello e Groq

## Descrição

Este projeto é um agente de organização de tarefas desenvolvido em Python, utilizando Google ADK, Trello API e Groq como modelo de linguagem.

O agente permite conversar com o usuário, entender tarefas do dia e interagir com um quadro do Trello para criar, listar e mudar o status das tarefas.

## Objetivo

O objetivo do projeto é praticar automação com Python, integração com APIs e uso de agentes inteligentes para organizar tarefas de forma automatizada.

## Tecnologias Utilizadas

- Python
- Google ADK
- Groq
- LiteLLM
- Trello API
- py-trello
- python-dotenv
- Git e GitHub

## Funcionalidades

- Criar cards no Trello;
- Listar tarefas;
- Filtrar tarefas por status;
- Mudar tarefas entre listas, como:
  - A Fazer;
  - Em Andamento;
  - Concluído;
- Usar variáveis de ambiente para proteger credenciais;
- Utilizar Groq como modelo de linguagem no agente.

## Estrutura do Projeto

```text
agent04/
├── agenttarefas/
│   ├── agent.py
│   └── .env
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuração do Ambiente

Antes de executar o projeto, é necessário criar um arquivo `.env` dentro da pasta `agenttarefas`.

Exemplo:

```env
TRELLO_API_KEY=sua_api_key
TRELLO_API_SECRET=seu_api_secret
TRELLO_TOKEN=seu_token
TRELLO_BOARD_ID=id_do_board
GROQ_API_KEY=sua_chave_groq
```

Importante: o arquivo `.env` não deve ser enviado para o GitHub, pois contém dados sensíveis.

## Instalação das Dependências

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Executar

Na pasta principal do projeto, execute:

```bash
adk web
```

Depois acesse no navegador:

```text
http://127.0.0.1:8000
```

## Aprendizados

Durante o desenvolvimento deste projeto, pratiquei conceitos importantes como:

- Integração com API externa;
- Manipulação de dados com Python;
- Uso de variáveis de ambiente;
- Criação de agentes com Google ADK;
- Uso de modelos de linguagem com Groq via LiteLLM;
- Organização de tarefas usando Trello.

## Autor

Carlos Eduardo