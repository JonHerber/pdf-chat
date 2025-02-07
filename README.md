# Chat with PDF
A simple RAG (Retrieval-Augmented Generation) system using Deepseek, LangChain, and Streamlit to chat with PDFs and answer complex questions about your local documents.

Insprired by [YouTube](https://youtu.be/M6vZ6b75p9k).

# Pre-requisites
Install Ollama on your local machine from the [official website](https://ollama.com/). And then pull the Deepseek model:

```bash
ollama pull deepseek-r1:7b
```

Additionally Docker is required!

Build the docker container:

```bash
docker build -t chat .
```

# Run the container
Run the container and access it on localhost:

```bash
docker run --rm chat
```
