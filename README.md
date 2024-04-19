# private_gpt_code_review

Use local GPT to review you code. This project uses Ollama as the local LLM.

## Ollama

- Download Ollama, [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- Follow the instructions there for installation
- Start Ollama
  ```
  ollama serve
  ```
- Pull the model you use for exmple `ollama pull mistral`

## Run

```
pip3 install -r requirements.txt
```

```
python3 run.py local --repo_path=[PATH_TO_GIT_REPO]
```
