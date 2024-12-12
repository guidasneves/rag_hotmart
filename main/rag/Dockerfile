FROM python:3.9

WORKDIR /app

# Instalando as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiando os requisitos e instalando os pacotes do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o código do sistema
COPY . .

# Porta onde o sistema é executado
EXPOSE 8001

# Comando para executar o sistema
CMD ["uvicorn", "system:app", "--host", "0.0.0.0", "--port", "8001"]