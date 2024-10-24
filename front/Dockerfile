FROM python:3.11-slim

WORKDIR /front

COPY src/ .

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]
