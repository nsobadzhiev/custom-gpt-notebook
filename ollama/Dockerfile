FROM ollama/ollama:0.9.5 as ollama

ARG models

RUN ollama serve & sleep 4 && for model in $models; do ollama pull $model ; done;

EXPOSE 11434

CMD ["serve"]
