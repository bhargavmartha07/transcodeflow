FROM python:3.11-alpine

RUN apk add --no-cache bash curl

WORKDIR /app

COPY . .

RUN chmod +x scripts/transcode.sh

RUN pip install flask

EXPOSE 8080

CMD ["python", "source_code/app.py"]
