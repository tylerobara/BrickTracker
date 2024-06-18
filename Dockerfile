FROM python:slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN bash lego.sh
#CMD ["python", "app.py"]
CMD ["gunicorn","--bind","0.0.0.0:3333","app:app","--worker-class","eventlet"]
