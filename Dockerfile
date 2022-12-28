FROM python:3.10-slim

RUN mkdir /app
WORKDIR /app
COPY . .
ARG POETRY_HOME
RUN apt-get update
RUN apt-get install -y libpq-dev build-essential curl
RUN curl -sSL https://install.python-poetry.org | python - --version 1.3.1
RUN /root/.local/bin/poetry config virtualenvs.create false
RUN /root/.local/bin/poetry install --no-dev --no-root
CMD ["python", "app.py"]