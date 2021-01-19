FROM python:3.8-alpine

WORKDIR /tmp

COPY requirements.txt /tmp
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /webapp
COPY src/ /webapp/

ENTRYPOINT ["python3", "app.py"]
