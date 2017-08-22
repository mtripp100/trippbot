FROM python:3

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "trippbot.web:app"]
