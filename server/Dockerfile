FROM python:3.7
WORKDIR /work

RUN pip install pipenv
COPY . .
RUN pipenv install
CMD pipenv run python manage.py