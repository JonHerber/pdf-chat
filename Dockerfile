# base image
FROM python:3.10.12-slim

WORKDIR /app-chat

RUN mkdir pdf-files

COPY requirements.txt requirements.txt
COPY pdf_rag.py pdf_rag.py

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "pdf_rag.py"]
