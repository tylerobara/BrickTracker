FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt update && \
    apt install -y wget && \
    rm -rf /var/lib/apt/lists/*

RUN bash lego.sh

CMD ["gunicorn","--bind","0.0.0.0:3333","app:app","--worker-class","eventlet"]
