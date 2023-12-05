# Dockerfile
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Run migrations during the Docker image build process
RUN python manage.py migrate

CMD ["python", "updater.py"]
