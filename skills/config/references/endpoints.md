# Endpoints

Use `TRADINGAGENTS_LLM_BACKEND_URL` when routing through a proxy, gateway, self-hosted OpenAI-compatible server, custom Azure endpoint, or OpenRouter.

For Ollama, prefer `OLLAMA_BASE_URL`. Default:

```
http://localhost:11434/v1
```

## Debugging

1. Check the selected provider.
2. Check `TRADINGAGENTS_LLM_BACKEND_URL`.
3. Check `OLLAMA_BASE_URL` for Ollama.
4. Confirm the model or deployment name is valid for that endpoint.
5. Do not modify source files to change provider defaults.
