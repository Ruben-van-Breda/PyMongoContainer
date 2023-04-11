FROM python:3.9-slim-buster
WORKDIR /code

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 3000
EXPOSE 5000

CMD ["python3", "app.py"]