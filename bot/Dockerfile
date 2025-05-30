FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Указываем PYTHONPATH, чтобы Python корректно находил src
ENV PYTHONPATH=/app

# Точка входа — main.py внутри src
CMD ["bash", "-c", "python src/init_db.py && python -m src.main"]

