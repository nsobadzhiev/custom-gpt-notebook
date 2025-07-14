# Local Custom GPTs

This is a collection of a notebook and Streamlit application that can be used for running customGPTs outside OpenAI.

## Running

Option 1: Run the Notebook in VS Code, PyCharm, Jupyter Notebooks or whatever software that supports notebooks.

Option 2 (recommended): Run the chat UI via streamlit:

```shell
streamlit run streamlit_app.py
```

### Dependencies

The official way to run this project is via uv. Build the project via:

```shell
uv sync
```

or run it directly via:

```shell
uv run streamlit run streamlit_app.py
```

## Connect an LLM

The [LiteLLM](https://docs.litellm.ai/docs/) library is used in order to provide a common interface to many LLMs, both local and cloud-based ones.
Refer to their docs for more information how to provide the correct settings.

For instance, if you want to use Ollama, the default settings would be to specify a URL of `http://localhost:11434` and a model such as `ollama/llama3.1`.

For remote LLMs such as OpenAI's, just put a valid API key in the API key text field.

### Running on Ollama

A cheap way to run this app is to connect it to a locally running [Ollama](https://ollama.com). To do this, install it, pull a model (I recommend `llama3.1`) and run it via `ollama serve`.

### Running via Docker

There are three Docker files in this project:
* `Dockerfile` - builds the Streamlit application
* `./ollama/Dockerfile` - builds a Docker image with Ollama and Llama3.1 already pulled in and ready to be used
* `docker-compose.yaml` - a compose file that runs the previous two and sets them up to communicate via a network

It's recommended to run Ollama locally on the host machine as the docker container can be quite slow to respond (many times slower than a locally running Ollama from my tests).

**Note:** When you open the Streamlit app, don't expect `localhost` to work as a LLM URL. You need to specify the address of the Ollama container as seen by the Streamlit container. 
