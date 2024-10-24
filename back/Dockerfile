FROM python:3.11-slim

WORKDIR /back

COPY ./src .
RUN pip install -r requirements.txt

CMD ["python", "run_api.py"]
