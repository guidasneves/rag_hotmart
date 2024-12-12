<a name="1"></a>
# Hotmart Case Técnico Cientista de Dados
<a name="2"></a>
## About
Criação de dois microserviços:
1. O primeiro microserviço, [`ingestão e pré-processamento`](main/ingestion/system.py) é responsável por receber um documento de texto extraído da página da [`Hotmart`](https://hotmart.com/pt-br/blog/como-funciona-hotmart), realizar o pré-processamento desse texto que foi extraído e o carregar em um Vector DB.
2. O segundo microserviço, [`RAG`](main/rag/system.py), é uma API que, dado um texto de entrada no formato de pergunta, busca nessa base de conhecimento (knowledge base) quais sequências correspondem a esse contexto que foi dado como entrada, e usa isso como entrada para uma LLM pré-treinada retornar uma resposta.

<a name="3"></a>
## Table of Contents
* [Hotmart Case Técnico Cientista de Dados](#1)
  * [About](#2)
  * [Table of Contents](#3)
  * [Tecnologias](#4)
  * [Pacotes](#5)
  * [Instalação](#6)
    * [Variáveis de Ambiente](#6.1)
    * [Execução](#6.2)
  * [Endpoints](#7)
  * [Testes](#8)
    * [Pré-processamento](#8.1)
    * [RAG](#8.2)
  * [Outros Exemplos de Testes](#9)

<a name="4"></a>
## Tecnologias
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Qdrant Vector Database](https://qdrant.tech/)
* [Transformers](https://huggingface.co/docs/transformers/index)
* [Sentence Transformers](https://sbert.net/)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

<a name="5"></a>
## Pacotes
* [fastapi](https://fastapi.tiangolo.com/): framework web moderno, rápido (de alto desempenho) para criar APIs com Python com base em dicas de tipo padrão do Python.
* [uvicorn](https://www.uvicorn.org/): implementação de servidor web ASGI para Python.
* [sentence-transformers](https://sbert.net/): também conhecido como SBERT, word embedding pré-treinado.
* [qdrant_client](https://qdrant.tech/): banco de dados vetorial open-source.
* [transformers](https://huggingface.co/docs/transformers/index): fornece APIs e ferramentas para baixar e treinar facilmente modelos estado da arte pré-treinados.
* [accelerate](https://huggingface.co/docs/accelerate/index): permite que o mesmo código PyTorch seja executado em qualquer configuração distribuída.
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/): facilita a extração de informações de páginas da web.
* [requests](https://pypi.org/project/requests/): biblioteca HTTP simples, para fazer solicitações HTTP.
* [os](https://docs.python.org/3/library/os.html): fornece uma maneira portátil de usar a funcionalidade dependente do sistema operacional.
* [logging](https://docs.python.org/3/library/logging.html): define funções e classes que implementam um sistema de registro de eventos flexível para aplicativos e bibliotecas.
* [re](https://docs.python.org/3/library/re.html): especifica um conjunto de strings que correspondem a ele.
* [dotenv](https://pypi.org/project/python-dotenv/): lê pares de chave-valor de um arquivo `.env` e pode defini-los como variáveis de ambiente.

<a name="6"></a>
## Instalação
Clonando o repositório e baixando os pacotes que foram utilizados no sistema.
```console
git clone https://github.com/guidasneves/rag_hotmart.git
```

<a name="6.1"></a>
### Variáveis de Ambiente
Definição das variáveis de ambiente, no arquivo `.env`, que são utilizadas para executar o sistema.
```text
VECTOR_DB_HOST="localhost"
VECTOR_DB_PORT=6333
```

<a name="6.2"></a>
### Execução
Execução do sistema.
```console
docker-compose up --build
```

<a name="7"></a>
## Endpoints
Endpoints da API:
* `POST /pre_process_url`: sistema da ingestão e pré-processamento do documento. Endpoint para carregar o URL ou o texto do documento, para que os dados sejam extraídos e pré-processados.
* `POST /ask`: sistema do RAG. Endpoint para enviar uma pergunta para recuperar respostas similares ao contexto.

<a name="8"></a>
## Testes
Exemplo de teste do pré-processamento do URL em cURL.

<a name="8.1"></a>
### Pré-processamento
```bash
curl -X POST http://localhost:8000/pre_process_url/ \
     -H "Content-Type: application/json" \
     -d '{"url": "https://hotmart.com/pt-br/blog/como-funciona-hotmart"}'
```

<a name="8.2"></a>
### RAG
```bash
curl -X POST http://localhost:8001/ask/ \
     -H "Content-Type: application/json" \
     -d '{"query": "Como funciona a Hotmart?"}'
```

<a name="9"></a>
## Outros Exemplos de Testes
Outros exemplos de testes em `shellscripts` e `Postman` incluídos no diretório [`./tests`](tests).
