FROM python:3.11-slim

WORKDIR /app

COPY auditor_persistent.py .

CMD ["python", "auditor_persistent.py"]