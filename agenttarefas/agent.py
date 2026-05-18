from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from trello import TrelloClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

# credenciais
API_KEY = os.getenv('TRELLO_API_KEY')
API_SECRET = os.getenv('TRELLO_API_SECRET')
TOKEN = os.getenv('TRELLO_TOKEN')
BOARD_ID = os.getenv("TRELLO_BOARD_ID")

def get_temporal_context():
    now = datetime.now()
    return now.strftime('%Y/%m/%d %H:%M:%S')

def adiciona_tarefa(nome_da_task: str, descricao_da_task: str, due_date: str = None):
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )

    # Obter o board pelo ID
    meu_board = client.get_board(BOARD_ID)

    #obter lisa onde adicionar o card
    listas = meu_board.list_lists()

    minhas_lista = [l for l in listas if l.name.upper()== 'TO DO' or l.name.upper()== 'A FAZER'][0]

    if due_date == "" or due_date == "None" or due_date == "none":
        due_date = None

    if due_date is not None:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
            due_date = f"{due_date}T12:00:00-03:00"
        except ValueError:
            due_date = None

    #add card
    card = minhas_lista.add_card(
        name=nome_da_task,
        desc=descricao_da_task,
        due=due_date
    )

    return f"Tarefa criada com sucesso no Trello: {card.name}"

def listar_tarefas(status: str = "todas"):
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )
    meu_board = client.get_board(BOARD_ID)
    listas = meu_board.list_lists()

    if status.lower() in ["todas", "todos", "all"]:
        listas_filtradas = listas
    elif status.lower() in ["a fazer", "afazer", "to do", "todo", "pendente", "pendentes"]:
        listas_filtradas = [l for l in listas if l.name.upper() in ["A FAZER", "TO DO", "TODO", "PENDENTE", "PENDENTES"]]
    elif status.lower() in ["em andamento", "andamento", "doing", "em progresso", "progresso"]:
        listas_filtradas = [l for l in listas if l.name.upper() in ["EM ANDAMENTO", "DOING", "EM PROGRESSO", "PROGRESSO"]]
    elif status.lower() in ["concluído", "concluido", "concluída", "concluida", "concluídos", "concluidos", "concluídas", "concluidas", "done"]:
        listas_filtradas = [l for l in listas if l.name.upper() in ["CONCLUÍDO", "CONCLUIDO", "CONCLUÍDA", "CONCLUIDA", "DONE"]]
    else:
        listas_filtradas = listas
    
    tarefas = []

    for lista in listas_filtradas:
        cards = lista.list_cards()
        for card in cards:
            tarefas.append({
                "nome": card.name,
                "descricao": card.desc,
                "vencimento": card.due,
                "status": lista.name,
                "id": card.id
            })

    return tarefas
def listar_tarefas_concluidas():
    return listar_tarefas("concluido")

def mudar_status_tarefa(nome_da_task: str, novo_status: str) -> str:
    client = TrelloClient(
        api_key=API_KEY,
        api_secret=API_SECRET,
        token=TOKEN
    )
    meu_board = client.get_board(BOARD_ID)
    listas = meu_board.list_lists()

    status_map = {
        "a fazer": "A FAZER",
        "em andamento": "EM ANDAMENTO",
        "concluido": "CONCLUIDO",
        "concluído": "CONCLUIDO"
    }

    nome_lista_destino = status_map.get(novo_status.lower())

    if not nome_lista_destino:
        return f"status invalido. use: ' a fazer', 'em andamento' ou 'concluido'"
    lista_destino = next(
        (l for l in listas if l.name.upper() in [nome_lista_destino, "CONCLUÍDO"]),
        None
    )

    if not lista_destino:
        return f"lista '{nome_lista_destino}' nao encontrada no board"
    card_encontrado = None
    lista_origem = None

    for lista in listas:
        cards = lista.list_cards()
        card_encontrado = next(
        (c for c in cards if c.name.lower() == nome_da_task.lower()),
        None
        )
        if card_encontrado:
            lista_origem = lista
            break

    if not card_encontrado:
        return f"Card '{nome_da_task}' não encontrado."

    card_encontrado.change_list(lista_destino.id)
    return f"Card '{nome_da_task}' movido de '{lista_origem.name}' para '{lista_destino.name}'."

root_agent = Agent(
    model=LiteLlm(model="groq/llama-3.3-70b-versatile"),
    name="root_agent",
    description="Agente de Organização de Tarefas",
    instruction="""
Você é um agente de organização de tarefas.
Sua função é receber uma tarefa e criar um card no Trello com o nome e a descrição da tarefa.
Você deve perguntar as atividades que o usuário tem no dia e criar um card para cada uma delas.
Você inicia a conversa assim que for ativado, perguntando quais são as tarefas do dia.
Sempre inicie a conversa perguntando quais são as tarefas do dia, informando a data com pela tool get_temporal_context.
Depois vá perguntando se tem mais alguma tarefa, até que o usuário diga que não tem mais tarefas.

Suas funções:
1. Adicionar novas tarefas com nome e descrição.
2. Listar todas as tarefas.
3. Marcar tarefas como concluídas.
4. Remover tarefas da lista.
5. Mudar o status da tarefa, por exemplo: de "A Fazer" para "Em Andamento" e de "Em Andamento" para "Concluído".
6. Gerar contexto temporal, data e hora atual, para organizar as tarefas do dia.

Ao iniciar a conversa:
- Chame obrigatoriamente a tool get_temporal_context para obter a data e hora atual.
- Use o resultado retornado pela tool para informar a data ao usuário.
- Depois pergunte quais são as tarefas do dia.

Regras:
- Quando o usuário pedir para listar tarefas, use obrigatoriamente a tool listar_tarefas.
- Quando o usuário pedir para criar tarefa, use obrigatoriamente a tool adiciona_tarefa.
- Quando o usuário pedir para mudar status, use obrigatoriamente a tool mudar_status_tarefa.
- Nunca escreva chamadas de ferramenta em texto, como <Listar tarefas>. Use a tool real.
- Quando o usuário pedir para listar tarefas, chame diretamente a tool listar_tarefas com status="todas".
- Quando o usuário pedir para criar uma tarefa, chame diretamente a tool adiciona_tarefa.
- Quando o usuário pedir para mudar status de uma tarefa, chame diretamente a tool mudar_status_tarefa.
- Nunca escreva chamadas de ferramenta em texto. Não escreva tags como <Listar tarefas>. Use apenas as tools disponíveis.
- Quando o usuário pedir tarefas concluídas, use a tool listar_tarefas_concluidas.
- Quando precisar da data e hora atual, chame a tool get_temporal_context.
- Nunca escreva o nome da tool como texto.
- Nunca escreva tags como <function=get_temporal_context>.
- Use apenas o resultado retornado pela tool.
""",
    tools=[get_temporal_context, adiciona_tarefa, listar_tarefas, listar_tarefas_concluidas, mudar_status_tarefa],

)