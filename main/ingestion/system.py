# Importando os pacotes
import os
import uvicorn
import logging
logging.basicConfig(level=logging.INFO)

import re
from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# Instânciando a classe FastAPI
app = FastAPI()

# Instânciando o word embedding pré-treinado
embedding_pre_trained = SentenceTransformer('neuralmind/bert-base-portuguese-cased')
# Inicializando o Qdrant
client = QdrantClient(
    host=os.getenv('VECTOR_DB_HOST', 'localhost'),
    port=int(os.getenv('VECTOR_DB_PORT', 6333))
    )
COLLECTION_NAME = 'documents'

def clean_text(text: str) -> str:
    """
    Um dos pré-processamentos. Limpa e normaliza o texto.
    
    Arguments:
        text -- Texto que será pré-processado.
    
    Return:
        text -- Text pré-processado.
    """
    # Substituindo qalquer caractere de espaço em branco
    text = re.sub(r'\s+', ' ', text).strip()
    # Substitui as tags HTML do texto
    text = re.sub(r'<[^>]+>', '', text)
    
    return text

@app.post('/pre_process_url/')
def pre_process_hotmart_url(url):
    """
    Pré-processa a URL da hotmart. Extrai o texto e o armazena em um banco de dados vetorial.
    
    Args:
        url -- URL da página da Hotmart.
    
    Returns:
        dict -- Dicionário python com os dados pré-processados.
    """
    try:
        # Acessando a página
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)

        # Dividindo o texto pré-processado em chunks
        chunks = split_text(clean_text(text))

        # Criando a collection, caso não exista
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                'size': embedding_pre_trained.get_sentence_embedding_dimension(), # Dimensão da matriz de word embedding
                'distance': 'Cosine' # Similaridade de cosseno como métrica de similaridade
                }
        )

        # Percorrendo cada chunk e os adicionando no Qdrant
        for i, chunk in enumerate(chunks):
            embedding = embedding_pre_trained.encode(chunk).tolist()
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[{
                    'id': i,
                    'vector': embedding,
                    'payload': {'text': chunk}
                }]
            )

        return {'status': 'success', 'chunks': len(chunks)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def split_text(text, chunk_size=500, overlap=50):
    """
    Divide o texto em chunks.
    
    Arguments:
        text -- Texto para ser dividido em chunks
        chunk_size -- Tamanho de cada chunk
        overlap -- Número de palavras a sobrepor entre os chunks
    
    Returns:
        chunks -- Lista de chunks de texto
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)