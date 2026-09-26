FROM python:3.11-slim

WORKDIR /usr/src/app

COPY auditor_persistent.py .

CMD ["python", "auditor_persistent.py"]