FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV PORT=5000

EXPOSE 5000

CMD ["python", "app.py"]
