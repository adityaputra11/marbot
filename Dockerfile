FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential \
  && pip install -r requirements.txt \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]