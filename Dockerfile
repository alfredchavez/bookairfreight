FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
COPY . bookairfreight/
WORKDIR bookairfreight/
RUN pip install -r requirements.txt
