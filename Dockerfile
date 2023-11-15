# Usar a imagem base oficial do Python
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY main.py /app

# Instala as dependências do Flask
RUN pip install Flask

# Expõe a porta 5000 do contêiner para o host
EXPOSE 5000

# Define o comando para iniciar o Flask quando o contêiner for executado
CMD ["python", "main.py"]
