FROM python:3.7-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./project /app/project

WORKDIR /app

CMD ["python", "-u", "./project/scraper.py"]