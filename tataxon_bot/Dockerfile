FROM python:3.12.5

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

WORKDIR /app

COPY requirements.txt .

# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "tataxon_bot.wsgi"]
