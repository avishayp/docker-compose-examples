FROM python:alpine

RUN pip install requests pytest

WORKDIR /test
COPY test_app.py ./

CMD pytest -svx