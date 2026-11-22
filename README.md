# Abroba IA

Assistente local em Python, feita para **explicar APIs de um jeito simples**. Ela roda no seu computador, sem internet e sem instalar bibliotecas extras.

> Status: em desenvolvimento.

## O que ela faz

- Se apresenta sozinha ao iniciar, com o cumprimento certo para o horário
- Responde cumprimentos: bom dia, boa tarde e boa noite
- Responde "tudo bem?" e conversa de forma básica
- Diz a data e a hora atuais
- Explica conceitos de API: API, REST, endpoint, métodos HTTP, JSON, status code, API key, requisição e resposta
- Mostra um exemplo de código em Python com a biblioteca `requests`

## Como rodar

Você só precisa ter o Python 3 instalado.

```
python abroba_ia_v2.py
```

Para ver tudo que ela sabe, digite `ajuda`. Para encerrar, digite `sair`.

## Exemplos de conversa

```
Você: bom dia, tudo bem?
Abroba IA: Bom dia! Estou ótima, obrigada por perguntar! E você, como está?

Você: que horas são?
Abroba IA: Agora são 14:30.

Você: o que é endpoint?
Abroba IA: Endpoint é o endereço (URL) específico de uma API onde você faz um pedido...
```

## Perguntas sobre API que ela entende

| Assunto | Exemplo de pergunta |
|---|---|
| O que é API | `o que é uma API?` |
| REST | `o que é REST?` |
| Endpoint | `o que é endpoint?` |
| Métodos HTTP | `métodos HTTP` |
| JSON | `o que é JSON?` |
| Status code | `status code` |
| Chave de acesso | `o que é API key?` |
| Requisição e resposta | `o que é requisição?` |
| Código de exemplo | `exemplo em python` |

## Como ensinar um assunto novo

No começo do arquivo existe a lista `TOPICOS`. Cada item tem as palavras-chave e a explicação. Para adicionar um tema, é só incluir um novo item ali.

## Como funciona

Ela é um chatbot baseado em regras: procura palavras-chave na sua mensagem (ignorando acentos, maiúsculas e pontuação) e responde com base nelas. Não usa modelo de linguagem.
