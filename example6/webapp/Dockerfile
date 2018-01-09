FROM python:3.6

WORKDIR /web

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py ./
COPY wsgi.ini ./

# wsgi socket
RUN mkdir -p /var/run/wsgi

CMD ["python", "-m", "main"]
