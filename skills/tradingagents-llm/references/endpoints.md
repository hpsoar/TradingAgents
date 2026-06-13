# Endpoints

Use `TRADINGAGENTS_LLM_BACKEND_URL` when routing through a proxy, gateway, self-hosted OpenAI-compatible server, custom Azure endpoint, or OpenRouter-style endpoint.

For Ollama, prefer `OLLAMA_BASE_URL`; the default is:

```text
http://localhost:11434/v1
```

When debugging endpoint issues:

- Check the selected provider.
- Check `TRADINGAGENTS_LLM_BACKEND_URL`.
- Check `OLLAMA_BASE_URL` for Ollama.
- Confirm the selected model or deployment name is valid for that endpoint.
- Do not modify source files to change provider defaults.
