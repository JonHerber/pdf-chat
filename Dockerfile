FROM python:3.10.12-slim

WORKDIR /app-chat

# Ensure the pdf-files directory exists
RUN mkdir -p /app-chat/pdf-files

# Copy necessary files
COPY requirements.txt .
COPY pdf_rag.py .

# Expose Streamlit's default port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Install dependencies
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the Streamlit app
CMD ["streamlit", "run", "pdf_rag.py", "--server.port=8501", "--server.address=0.0.0.0"]
