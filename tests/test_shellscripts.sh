# Configuração do ambiente
DOCUMENT_PROCESSOR_URL="http://localhost:8000/pre_process_url/"
QA_SERVICE_URL="http://localhost:8001/ask/"

# URL para teste
TEST_URLS=(
    "https://hotmart.com/pt-br/blog/como-funciona-hotmart"
)

# Função para pré-processar os documentos
pre_process_documents() {
    for url in "${TEST_URLS[@]}"; do
        echo "Pré-processando URL: $url"
        curl -X POST "$DOCUMENT_PROCESSOR_URL" \
             -H "Content-Type: application/json" \
             -d "{\"url\": \"$url\"}"
        echo -e "\n"
    done
}

# Função para testar o RAG
test_rag() {
    local questions=(
        "Como funciona a Hotmart?"
        "O que é a Hotmart?"
        "Quanto a Hotmart cobra por venda?"
    )

    for question in "${questions[@]}"; do
        echo "Perguntando: $question"
        curl -X POST "$QA_SERVICE_URL" \
             -H "Content-Type: application/json" \
             -d "{\"query\": \"$question\"}"
        echo -e "\n"
    done
}

# Função para executar todos os testes
main() {
    echo "Começando com os testes do sistema."
    
    # Pré-processando os documentos
    pre_process_documents
    
    # Esperando 5 segundos para indexar
    sleep 5
    
    # Executando o teste do RAG
    test_rag
}

# Executando os testes
main