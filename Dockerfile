FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y curl pipx && \
    pipx ensurepath && rm -rf /var/lib/apt/lists/*

RUN pip install uv

RUN uv sync

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uv", "run", "streamlit", "run", "streamlit_app.py", "--server.port=8501"]
