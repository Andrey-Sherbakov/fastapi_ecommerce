FROM python:3.13-slim
LABEL authors="Andrey"
RUN groupadd -r fast_group && useradd -r -g fast_group fast_user

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /home/fast
COPY requirements.txt .
Run pip install -r requirements.txt

COPY app app
ADD alembic.ini .

RUN chown -R fast_user:fast_group .

USER fast_user
