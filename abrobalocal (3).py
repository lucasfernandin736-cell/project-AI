from datetime import datetime, timedelta, timezone
import re
import unicodedata

# Horário de Brasília (UTC-3), para a hora sair certa também no servidor
FUSO = timezone(timedelta(hours=-3))

NOME = "Abroba IA"
CRIADOR = "FERNANDO"   # troque pelo seu nome

SOBRE_QUEM = f"Eu sou a {NOME}, uma assistente de IA feita em Python."
SOBRE_CRIADOR = f"Fui criada por {CRIADOR}, como projeto de estudo de programação em Python."
SOBRE_FUNCOES = (
    "O que eu faço:\n"
    "  - Converso com cumprimentos (bom dia, boa tarde, boa noite)\n"
    "  - Digo a data e as horas\n"
    "  - Explico APIs: API, REST, endpoint, métodos HTTP, JSON, status code, API key e requisição\n"
    "  - Mostro um exemplo de código em Python com a biblioteca requests\n"
    "  - Explico tributos: ISS, IRRF, PIS, Cofins, CSLL, INSS, retenção e parametrização\n"
    "Digite 'ajuda' para ver exemplos de perguntas."
)

DIAS = ["segunda-feira", "terça-feira", "quarta-feira",
        "quinta-feira", "sexta-feira", "sábado", "domingo"]

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

# ---------------------------------------------------------------
# BASE DE CONHECIMENTO SOBRE APIs
# Cada item: (palavras-chave, explicação)
# A ordem importa: os temas específicos vêm antes do tema geral.
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

# ---------------------------------------------------------------
# BASE DE CONHECIMENTO SOBRE TRIBUTOS (atualizada em 26/11/2026)
# Material de estudo com regras gerais: confirme com o setor fiscal.
# Cada item: (pergunta, palavras-chave, explicação)
# ---------------------------------------------------------------
TRIBUTOS = [
    ("O que é parametrizar?",
     ("parametrizar", "parametrizacao",),
     "É configurar o sistema com regras. Exemplo: se for tal serviço, de tal prestador, em tal município, então aplicar tais tributos e alíquotas. Uma regra errada repete o erro em várias notas."),

    ("O que conferir antes de parametrizar uma nota?",
     ("conferir", "checklist",),
     "Tipo de serviço, regime tributário do prestador, quem é o tomador, município onde o ISS é devido, base de cálculo, alíquotas, dispensas e data de vigência da regra."),

    ("O que é ISS?",
     ("iss", "issqn",),
     "Imposto sobre Serviços, municipal. Regra geral na Lei Complementar 116/2003, com alíquota de 2% a 5%. Cada município tem sua lei, e a retenção e o local de pagamento dependem do serviço."),

    ("O que é IRRF?",
     ("irrf", "imposto de renda",),
     "Imposto de Renda Retido na Fonte, federal. Entre empresas, é comum 1,5% em serviços profissionais (como consultoria, contabilidade e advocacia) e 1% em limpeza, conservação, segurança, vigilância e locação de mão de obra. Há outras hipóteses. Retenção de até R$ 10,00 é dispensada."),

    ("O que é PIS?",
     ("pis",),
     "Contribuição federal. Na retenção sobre serviços sujeitos à regra, a alíquota é 0,65% em 2026. A partir de 2027 o PIS é substituído pela CBS."),

    ("O que é Cofins?",
     ("cofins",),
     "Contribuição federal para a seguridade social. Na retenção sobre serviços sujeitos à regra, a alíquota é 3% em 2026. A partir de 2027 a Cofins é substituída pela CBS."),

    ("O que é CSLL?",
     ("csll",),
     "Contribuição Social sobre o Lucro Líquido, federal. A alíquota de retenção é 1%. A retenção da CSLL continua a partir de 2027."),

    ("O que é CSRF ou PCC?",
     ("csrf", "pcc", "4 65",),
     "Retenção conjunta de PIS 0,65% + Cofins 3% + CSLL 1% = 4,65% (Lei 10.833/2003), em serviços como limpeza, manutenção, segurança, vigilância, locação de mão de obra e serviços profissionais. Prestador do Simples Nacional em regra não sofre essa retenção. A partir de 2027 fica só a CSLL de 1%."),

    ("Quando há retenção de INSS?",
     ("inss",),
     "Não vale para qualquer serviço. Em casos como cessão de mão de obra, a retenção geral é de 11%, respeitando regras de base de cálculo, deduções e exceções."),

    ("O que muda com prestador do Simples Nacional?",
     ("simples nacional",),
     "Em regra não há retenção de IRRF, PIS, Cofins e CSLL. ISS e INSS podem ter tratamento próprio, então precisam ser analisados."),

    ("O que muda com a reforma tributária?",
     ("reforma", "ibs", "cbs",),
     "2026: teste da CBS (0,9%) e do IBS (0,1%). 2027: CBS passa a ser cobrada e PIS e Cofins são extintos. 2029 a 2032: ISS e ICMS diminuem aos poucos e o IBS aumenta. 2033: ISS e ICMS deixam de existir."),

    ("Me dê um exemplo de cálculo de retenções",
     ("exemplo de retencao", "exemplo de retencoes", "calculo de retencao", "calculo de retencoes",),
     "Exemplo didático para 2026: serviço profissional de R$ 2.000, supondo IRRF 1,5% e CSRF 4,65% aplicáveis e sem ISS ou INSS retidos. IRRF = R$ 30,00. PIS = R$ 13,00. Cofins = R$ 60,00. CSLL = R$ 20,00. Total retido = R$ 123,00. Líquido = R$ 1.877,00."),
]

# Conceitos gerais: só valem se nenhum tema acima for encontrado
CONCEITOS = [
    ("O que é tributo?",
     ("tributo", "tributos",),
     "É o nome geral para valores obrigatórios pagos ao governo: impostos, taxas e contribuições, entre outros. ISS e IRRF envolvem impostos; PIS, Cofins, CSLL e INSS são contribuições."),

    ("Qual a diferença entre tributo municipal e federal?",
     ("municipal", "municipais", "federal", "federais",),
     "Municipal é cobrado pelo município, como o ISS. Federal é cobrado pela União, como IRRF, PIS, Cofins, CSLL e INSS."),

    ("O que é alíquota?",
     ("aliquota", "aliquotas",),
     "É o percentual aplicado sobre a base de cálculo. Exemplo: 5% sobre R$ 1.000 dá R$ 50."),

    ("O que é base de cálculo?",
     ("base de calculo",),
     "É o valor sobre o qual a alíquota é aplicada. Nem sempre é igual ao valor total da nota, pois há deduções previstas em alguns casos."),

    ("O que é retenção na fonte?",
     ("retencao", "retido", "reter",),
     "Quem contrata o serviço desconta o tributo do pagamento e recolhe ao governo. O prestador recebe o valor líquido."),

    ("Quem é o prestador e quem é o tomador?",
     ("tomador", "prestador",),
     "Prestador é quem faz o serviço e emite a nota. Tomador é quem contrata e paga."),
]

TEXTO_AJUDA = (
    "Posso te ajudar com:\n"
    "  - Cumprimentos: bom dia, boa tarde, boa noite\n"
    "  - Data e hora: \"que dia é hoje?\" e \"que horas são?\"\n"
    "  - Sobre mim: \"quem é você?\", \"o que você faz?\", \"quem te criou?\", \"se apresente\"\n"
    "  - Explicar APIs: \"o que é uma API?\", \"o que é REST?\", \"o que é endpoint?\",\n"
    "    \"métodos HTTP\", \"o que é JSON?\", \"status code\", \"API key\",\n"
    "    \"o que é requisição?\" e \"exemplo em Python\"\n"
    "  - Tributos: \"o que é tributo?\", \"o que é alíquota?\", \"o que é ISS?\",\n"
    "    \"o que é parametrizar?\" e \"o que muda com a reforma tributária?\"\n"
    "Para encerrar, digite: sair"
)


def normalizar(texto):
    """Minúsculo, sem acentos e sem pontuação, para facilitar a comparação."""
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9 ]", " ", texto)
    texto = " ".join(texto.split())
    # abreviações comuns de chat
    texto = re.sub(r"\bvc\b", "voce", texto)
    texto = re.sub(r"\bqm\b", "quem", texto)
    texto = re.sub(r"\boq\b", "o que", texto)
    texto = re.sub(r"\bq\b", "que", texto)
    return texto


def tem(msg, *termos):
    """True se algum termo aparece como palavra (ou frase) inteira na mensagem."""
    return any(f" {t} " in f" {msg} " for t in termos)


def responder_tributos(msg):
    """Recebe a mensagem já normalizada. Devolve a explicação ou None."""
    # Pergunta igual à cadastrada
    for pergunta, _, explicacao in TRIBUTOS + CONCEITOS:
        if msg == normalizar(pergunta):
            return explicacao
    # Senão, vence a palavra-chave mais longa; temas antes dos conceitos
    for lista in (TRIBUTOS, CONCEITOS):
        achados = [(len(p), explicacao) for _, palavras, explicacao in lista
                   for p in palavras if tem(msg, p)]
        if achados:
            return max(achados, key=lambda a: a[0])[1]
    return None


def saudacao_do_dia(agora):
    if agora.hour < 12:
        return "Bom dia"
    if agora.hour < 18:
        return "Boa tarde"
    return "Boa noite"


def apresentacao():
    saudacao = saudacao_do_dia(datetime.now(FUSO))
    return (
        f"{saudacao}! Eu sou a {NOME}, sua assistente local. "
        "Meu foco é explicar APIs e tributos de um jeito simples. "
        "Também posso te dizer a data e as horas.\n"
        "Digite 'ajuda' para ver o que posso responder ou 'sair' para encerrar."
    )


def responder(mensagem):
    msg = normalizar(mensagem)
    agora = datetime.now(FUSO)
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

    # Sobre a IA (quem é, o que faz, quem criou)
    if tem(msg, "se apresente", "apresente se"):
        curtas.append(f"{SOBRE_QUEM} {SOBRE_CRIADOR}")
        longas.append(SOBRE_FUNCOES)
    if tem(msg, "seu nome", "quem e voce", "quem eh voce", "quem voce e"):
        curtas.append(SOBRE_QUEM)
    if tem(msg, "quem criou voce", "quem te criou", "quem fez voce", "quem te fez",
           "seu criador", "quem programou voce"):
        curtas.append(SOBRE_CRIADOR)
    if tem(msg, "o que voce faz", "oq voce faz", "o que voce sabe fazer", "para que voce serve"):
        longas.append(SOBRE_FUNCOES)

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

    # Tributos
    sobre_tributos = responder_tributos(msg)
    if sobre_tributos:
        longas.append(sobre_tributos)
    else:
        # Explicações sobre APIs (responde só o primeiro tema encontrado)
        for palavras, explicacao in TOPICOS:
            if tem(msg, *palavras):
                longas.append(explicacao)
                break

    if not curtas and not longas:
        return ("Ainda não sei responder isso, meu foco é explicar APIs e tributos. "
                "Digite 'ajuda' para ver o que posso responder.")

    resposta = " ".join(curtas)
    if longas:
        resposta += ("\n\n" if curtas else "") + "\n\n".join(longas)
    return resposta


def main():
    print(f"=== {NOME} (versão 7) ===\n")
    print(f"{NOME}: {apresentacao()}\n")
    while True:
        mensagem = input("Você: ")
        if normalizar(mensagem) == "sair":
            print(f"{NOME}: Até mais!")
            break
        print(f"\n{NOME}: {responder(mensagem)}\n")


if __name__ == "__main__":
    main()
    