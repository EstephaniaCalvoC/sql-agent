FROM python:3.11-slim

WORKDIR /back

COPY runtime_requirements.txt .
COPY app/ ./app
COPY run_api.py .

RUN pip install -r runtime_requirements.txt

CMD ["python", "run_api.py"]
