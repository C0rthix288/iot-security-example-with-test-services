# client/Dockerfile

FROM arm64v8/python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]

VOLUME ["/opt/gProVision/secrets"]
