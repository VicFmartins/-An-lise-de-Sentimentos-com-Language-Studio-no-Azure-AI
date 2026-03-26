# Analise de Sentimentos com Language Studio no Azure AI

Este repositorio deixou de ser apenas um resumo conceitual e virou um MVP executavel de analise de sentimentos. O projeto agora oferece uma API em FastAPI com modo local explicavel e integracao opcional com Azure AI Language, incluindo suporte a opinion mining.

## O que foi melhorado

- API REST para analise de sentimentos
- modo local para demonstracao sem credenciais
- integracao opcional com Azure AI Language
- retorno por sentenca
- extracao simples de opinioes por aspecto
- exemplos prontos de requisicao
- testes automatizados
- Dockerfile para execucao local

## Correcao importante

Analise de sentimentos nao pertence ao Azure AI Speech Studio. O servico correto e o Azure AI Language, e a experiencia no portal costuma ser feita pelo Language Studio. Ajustei o projeto para refletir isso de forma mais precisa.

## Endpoints

### `GET /health`

Retorna o status da API.

### `POST /api/sentiment/analyze`

Analisa o sentimento do texto e, quando possivel, retorna opinioes por aspecto.

Exemplo de payload:

```json
{
  "text": "O atendimento foi excelente, mas o preco continua caro e a plataforma ficou lenta no horario de pico.",
  "language": "pt",
  "include_opinion_mining": true
}
```

## Como executar localmente

### Com Python

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Com Docker

```bash
docker build -t language-studio-sentimentos .
docker run -p 8000:8000 language-studio-sentimentos
```

## Configuracao opcional do Azure

Defina:

- `AZURE_LANGUAGE_KEY`
- `AZURE_LANGUAGE_ENDPOINT`

Base pronta em [.env.example](.env.example).

Sem essas variaveis, a API roda no modo `local_heuristic`, ideal para portfolio e testes locais. Com elas, o projeto passa a chamar o endpoint oficial de analise de sentimento do Azure AI Language.

## Estrutura do projeto

- `app/main.py`: endpoints da API
- `app/analyzer.py`: analise local heuristica
- `app/azure_client.py`: integracao com Azure AI Language
- `app/lexicon.py`: vocabulario positivo, negativo e aspectos
- `tests/test_sentiment_api.py`: testes do fluxo principal
- `docs/how-it-works.md`: explicacao dos dois modos
- `examples/sample-request.json`: payload de exemplo

## Referencias oficiais

Usei como base documentacao oficial da Microsoft sobre Azure AI Language e sentiment analysis:

- [Azure AI Language documentation](https://learn.microsoft.com/en-us/azure/ai-services/language-service/)
- [Sentiment analysis and opinion mining](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview)
- [Analyze text REST API](https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/how-to/call-api)
- [Language Studio](https://learn.microsoft.com/en-us/azure/ai-services/language-service/language-studio)

## Validacao

```bash
pytest
```

Os testes cobrem:

- texto positivo
- texto negativo
- quebra por sentencas

## Proximos passos

- adicionar dashboard web simples
- salvar historico de analises
- incluir suporte a lotes de textos
- comparar local versus Azure no mesmo endpoint
- adicionar analise de entidades junto com sentimento
