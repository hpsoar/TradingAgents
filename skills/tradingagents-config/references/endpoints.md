# Endpoints

## Standard endpoints

Each provider has a default endpoint. Override with `TRADINGAGENTS_LLM_BACKEND_URL`.

## Ollama

Default: `http://localhost:11434/v1`

Override with `OLLAMA_BASE_URL`:

```
OLLAMA_BASE_URL=http://ollama-server:11434/v1
```

## Debugging

1. Check `TRADINGAGENTS_LLM_PROVIDER` — is it the expected provider?
2. Check `TRADINGAGENTS_LLM_BACKEND_URL` — is it set when it should be (or unset when it shouldn't)?
3. Check `OLLAMA_BASE_URL` — correct for Ollama?
4. Confirm the model/deployment name exists at that endpoint
5. Do NOT edit source files to change provider defaults
