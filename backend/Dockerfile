FROM python:3.13

WORKDIR /app

RUN apt-get update

RUN apt-get install -y curl

RUN curl -fsSL https://get.docker.com | sh

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]