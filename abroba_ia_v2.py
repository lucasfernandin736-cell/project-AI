from datetime import datetime
import re
import unicodedata

NOME = "Abroba IA"

DIAS = ["segunda-feira", "terça-feira", "quarta-feira",
        "quinta-feira", "sexta-feira", "sábado", "domingo"]

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

# ---------------------------------------------------------------
# BASE DE CONHECIMENTO SOBRE APIs
# Cada item: (palavras-chave, explicação)
# A ordem importa: os temas específicos vêm antes do tema geral.
# Para ensinar algo novo à Abroba IA, é só adicionar um item aqui.
# ---------------------------------------------------------------
TOPICOS = [
    (("rest", "restful"),
     "REST é um estilo de criar APIs que usa o protocolo HTTP, o mesmo da web. "
     "Cada coisa (usuário, produto, pedido) é um \"recurso\" com seu próprio endereço (URL), "
     "e você age sobre ele com métodos HTTP como GET, POST, PUT e DELETE. "
     "As respostas geralmente vêm em JSON. É o estilo de API mais comum hoje."),

    (("endpoint", "endpoints", "rota", "rotas", "url"),
     "Endpoint é o endereço (URL) específico de uma API onde você faz um pedido. "
     "Exemplo: https://api.exemplo.com/usuarios devolve a lista de usuários, "
     "e https://api.exemplo.com/usuarios/7 devolve só o usuário de número 7. "
     "Cada endpoint representa uma coisa que a API sabe fazer."),

    (("http", "metodo", "metodos", "get", "post", "put", "delete", "patch"),
     "HTTP é o protocolo de comunicação da web, e os métodos dizem o que você quer fazer:\n"
     "  GET    -> buscar dados\n"
     "  POST   -> criar algo novo\n"
     "  PUT    -> atualizar algo existente\n"
     "  DELETE -> apagar\n"
     "Numa API de usuários: GET /usuarios lista todos, POST /usuarios cria um novo, "
     "PUT /usuarios/7 atualiza o 7 e DELETE /usuarios/7 apaga o 7. "
     "(Existe também o PATCH, que atualiza só uma parte.)"),

    (("json",),
     "JSON é o formato de texto que as APIs mais usam para trocar dados. "
     "Ele parece com um dicionário do Python:\n"
     "  {\"nome\": \"Ana\", \"idade\": 20}\n"
     "Em Python, a biblioteca requests converte isso em dicionário com resposta.json()."),

    (("status", "200", "201", "400", "401", "403", "404", "500"),
     "O status code é o número que a API devolve para dizer como foi o seu pedido:\n"
     "  200 -> deu certo\n"
     "  201 -> criado com sucesso\n"
     "  400 -> pedido inválido\n"
     "  401 -> não autenticado (faltou login ou chave)\n"
     "  403 -> sem permissão\n"
     "  404 -> não encontrado\n"
     "  500 -> erro no servidor\n"
     "Regra rápida: 2xx é sucesso, 4xx é erro do cliente (seu), 5xx é erro do servidor."),

    (("key", "chave", "token", "autenticacao", "autenticar", "autorizacao"),
     "Muitas APIs pedem uma chave (API key) ou um token para saber quem está fazendo o pedido "
     "e controlar o uso. Normalmente você envia isso no cabeçalho (header) da requisição. "
     "Dica importante: nunca coloque sua chave direto no código nem suba ela para o GitHub. "
     "Guarde em variáveis de ambiente."),

    (("requisicao", "requisicoes", "request", "response", "resposta"),
     "Requisição (request) é o pedido que seu programa envia para a API, "
     "e resposta (response) é o que ela devolve. "
     "A requisição leva: o método (GET, POST...), o endereço (endpoint), "
     "cabeçalhos (headers) e, às vezes, um corpo (body) com dados. "
     "A resposta traz o status code e, normalmente, os dados em JSON."),

    (("requests", "python", "exemplo", "exemplos"),
     "Exemplo em Python com a biblioteca requests (instale com: pip install requests):\n\n"
     "  import requests\n\n"
     "  resposta = requests.get(\"https://api.github.com\")\n"
     "  print(resposta.status_code)  # 200 se deu certo\n"
     "  print(resposta.json())       # dados em formato de dicionário"),

    # Tema geral (fica por último)
    (("api", "apis"),
     "API (Application Programming Interface) é uma forma de dois programas conversarem entre si. "
     "Pense num restaurante: você (o cliente) faz o pedido ao garçom (a API), "
     "que leva até a cozinha (o servidor) e traz a resposta de volta. "
     "Você não precisa saber como a cozinha funciona, só como fazer o pedido. "
     "Exemplo do dia a dia: o app de clima do celular usa uma API para buscar a previsão do tempo.\n"
     "Quer ir mais fundo? Pergunte sobre: REST, endpoint, métodos HTTP, JSON, "
     "status code, API key, requisição ou exemplo em Python."),
]

TEXTO_AJUDA = (
    "Posso te ajudar com:\n"
    "  - Cumprimentos: bom dia, boa tarde, boa noite\n"
    "  - Data e hora: \"que dia é hoje?\" e \"que horas são?\"\n"
    "  - Explicar APIs: \"o que é uma API?\", \"o que é REST?\", \"o que é endpoint?\",\n"
    "    \"métodos HTTP\", \"o que é JSON?\", \"status code\", \"API key\",\n"
    "    \"o que é requisição?\" e \"exemplo em Python\"\n"
    "Para encerrar, digite: sair"
)


def normalizar(texto):
    """Minúsculo, sem acentos e sem pontuação, para facilitar a comparação."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9 ]", " ", texto)
    return " ".join(texto.split())


def tem(msg, *termos):
    """True se algum termo aparece como palavra (ou frase) inteira na mensagem."""
    return any(f" {t} " in f" {msg} " for t in termos)


def saudacao_do_dia(agora):
    if agora.hour < 12:
        return "Bom dia"
    if agora.hour < 18:
        return "Boa tarde"
    return "Boa noite"


def apresentacao():
    saudacao = saudacao_do_dia(datetime.now())
    return (
        f"{saudacao}! Eu sou a {NOME}, sua assistente local. "
        "Meu foco é explicar APIs de um jeito simples. "
        "Também posso te dizer a data e as horas.\n"
        "Digite 'ajuda' para ver o que posso responder ou 'sair' para encerrar."
    )


def responder(mensagem):
    msg = normalizar(mensagem)
    agora = datetime.now()
    curtas = []   # respostas de uma linha
    longas = []   # explicações maiores

    # Cumprimentos
    if tem(msg, "bom dia"):
        curtas.append("Bom dia!")
    if tem(msg, "boa tarde"):
        curtas.append("Boa tarde!")
    if tem(msg, "boa noite"):
        curtas.append("Boa noite!")

    # Como ela está
    if tem(msg, "tudo bem", "tudo bom", "esta bem", "como vai", "como voce esta", "como esta voce"):
        curtas.append("Estou ótima, obrigada por perguntar! E você, como está?")
    if tem(msg, "estou bem", "to bem", "tudo otimo", "estou otimo", "estou otima"):
        curtas.append("Que bom saber! Quer aprender sobre APIs? Digite 'ajuda' para ver os temas.")

    # Nome
    if tem(msg, "seu nome", "quem e voce", "quem eh voce", "quem voce e"):
        curtas.append(f"Eu sou a {NOME}, uma IA local que roda no seu computador e explica APIs.")

    # Horas
    if tem(msg, "hora", "horas"):
        curtas.append(f"Agora são {agora:%H:%M}.")

    # Data
    if tem(msg, "que dia", "data", "hoje"):
        dia_semana = DIAS[agora.weekday()]
        mes = MESES[agora.month - 1]
        curtas.append(f"Hoje é {dia_semana}, {agora.day} de {mes} de {agora.year}.")

    # Ajuda
    if tem(msg, "ajuda", "menu", "temas", "topicos", "o que voce sabe"):
        longas.append(TEXTO_AJUDA)

    # Explicações sobre APIs (responde só o primeiro tema encontrado)
    for palavras, explicacao in TOPICOS:
        if tem(msg, *palavras):
            longas.append(explicacao)
            break

    if not curtas and not longas:
        return ("Ainda não sei responder isso, meu foco é explicar APIs. "
                "Digite 'ajuda' para ver o que posso responder.")

    resposta = " ".join(curtas)
    if longas:
        resposta += ("\n\n" if curtas else "") + "\n\n".join(longas)
    return resposta


def main():
    print(f"{NOME}: {apresentacao()}\n")
    while True:
        mensagem = input("Você: ")
        if normalizar(mensagem) == "sair":
            print(f"{NOME}: Até mais!")
            break
        print(f"\n{NOME}: {responder(mensagem)}\n")


if __name__ == "__main__":
    main()
