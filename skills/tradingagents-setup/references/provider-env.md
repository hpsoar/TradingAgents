# Provider Environment

Use canonical provider keys: `openai`, `anthropic`, `google`, `azure`, `xai`, `deepseek`, `qwen`, `qwen-cn`, `glm`, `glm-cn`, `minimax`, `minimax-cn`, `openrouter`, or `ollama`.

Provider key mapping:

```text
openai      -> OPENAI_API_KEY
google      -> GOOGLE_API_KEY
anthropic   -> ANTHROPIC_API_KEY
azure       -> AZURE_OPENAI_API_KEY
xai         -> XAI_API_KEY
deepseek    -> DEEPSEEK_API_KEY
qwen        -> DASHSCOPE_API_KEY
qwen-cn     -> DASHSCOPE_CN_API_KEY
glm         -> ZHIPU_API_KEY
glm-cn      -> ZHIPU_CN_API_KEY
minimax     -> MINIMAX_API_KEY
minimax-cn  -> MINIMAX_CN_API_KEY
openrouter  -> OPENROUTER_API_KEY
ollama      -> no API key
```

Optional data key:

```bash
ALPHA_VANTAGE_API_KEY=
```

Unattended `.env` settings:

```bash
TRADINGAGENTS_LLM_PROVIDER=openai
TRADINGAGENTS_DEEP_THINK_LLM=gpt-5.5
TRADINGAGENTS_QUICK_THINK_LLM=gpt-5.4-mini
TRADINGAGENTS_LLM_BACKEND_URL=
TRADINGAGENTS_OUTPUT_LANGUAGE=English
TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
TRADINGAGENTS_MAX_RISK_ROUNDS=1
TRADINGAGENTS_CHECKPOINT_ENABLED=false
TRADINGAGENTS_TEMPERATURE=0.0
```

Use `TRADINGAGENTS_CACHE_DIR`, `TRADINGAGENTS_RESULTS_DIR`, and `TRADINGAGENTS_MEMORY_LOG_PATH` only when the default `~/.tradingagents` layout is not appropriate.

For Ollama, use `OLLAMA_BASE_URL` only when the endpoint is not the local default `http://localhost:11434/v1`.
