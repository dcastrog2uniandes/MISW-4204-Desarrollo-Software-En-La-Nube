FROM python:3.10-alpine

RUN mkdir -p /home/flask_app/conversorArchivosAudio
WORKDIR /home/flask_app/conversorArchivosAudio

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ConversorArchivosAudio ./start.sh ./
RUN chmod +x start.sh

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./start.sh"]
