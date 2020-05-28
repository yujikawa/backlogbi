FROM python:3.7.4-slim
LABEL maintainer="yujikawa"

RUN apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        less \
        vim \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && pip install awscli --upgrade

COPY poetry.lock tmp/poetry.lock
COPY pyproject.toml tmp/pyproject.toml
RUN cd /tmp && poetry install --no-dev

WORKDIR /opt/backlogbi
COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]