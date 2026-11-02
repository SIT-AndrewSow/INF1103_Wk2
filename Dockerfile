FROM python:3.11-slim

WORKDIR /usr/src/app

COPY main.py inventory.py product.py

CMD ["python", "main.py"]