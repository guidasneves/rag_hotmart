# Importando os pacotes
import os
import uvicorn
import logging
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()

# Instânciando a classe FastAPI
app = FastAPI()

# Instânciando o word embedding e o modelo pré-treinado
embedding_pre_trained = SentenceTransformer('neuralmind/bert-base-portuguese-cased')
llm = pipeline('text-generation',
               model='pierreguilloux/zeroshot-xlm-roberta-base-multi-query-pt')

# Inicializando o Qdrant
client = QdrantClient(
    host=os.getenv('VECTOR_DB_HOST', 'localhost'),
    port=int(os.getenv('VECTOR_DB_PORT', 6333))
    )
COLLECTION_NAME = 'documents'

@app.post('/ask/')
def rag(query):
    """
    Gera a pergunta com base no contexto.
    
    Arguments:
        query -- Pergunta para o modelo.
    
    Returns:
        dict -- Dicionário python com a pergunta, o contexto e a resposta.
    """
    try:
        # Gerando o word embedding da query
        query_embedding = embedding_pre_trained.encode(query).tolist()

        # Buscando chunks relevantes do documento
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3 # Os 3 chunks com a maior similaridade
        )

        # Juntando o contexto
        context = ' '.join([hit.payload['text'] for hit in search_results])

        # Gerando a respota
        prompt = f'Context: {context}\nQuestion: {query}\nAnswer:'
        answer = llm(prompt,
                     max_length=200,
                     num_return_sequences=1)[0]['generated_text']

        return {
            'answer': answer.split('Answer:')[-1].strip(),
            'context': context
        }

    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)