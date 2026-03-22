# Como o projeto funciona

O projeto tem dois modos:

## 1. Modo local

Usado quando as credenciais do Azure nao estao configuradas.

- faz tokenizacao simples
- calcula polaridade por lexicon
- separa sentencas
- tenta identificar aspectos como preco, atendimento e desempenho

## 2. Modo Azure

Usado quando `AZURE_LANGUAGE_KEY` e `AZURE_LANGUAGE_ENDPOINT` estao definidos.

- envia o texto para o endpoint de analise de sentimento do Azure AI Language
- habilita `opinionMining`
- retorna resultado consolidado e por sentenca

## Observacao importante

O projeto original citava Speech Studio, mas analise de sentimentos pertence ao Azure AI Language e pode ser explorada pelo Language Studio.
