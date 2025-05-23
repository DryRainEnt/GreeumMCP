FROM python:3.11-slim

# prevent bytecode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install build deps
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app
RUN pip install --no-cache-dir .

# create data dir
RUN mkdir -p /app/data

EXPOSE 8000

ENTRYPOINT ["greeum_mcp", "--transport", "http", "--port", "8000", "--data-dir", "/app/data"] 