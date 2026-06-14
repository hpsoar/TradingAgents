# Provider Environment

Supported provider keys:

```
openai, anthropic, google, azure, xai, deepseek,
qwen, qwen-cn, glm, glm-cn, minimax, minimax-cn,
openrouter, ollama
```

Credential mapping:

```
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

Common config variables:

```
TRADINGAGENTS_LLM_PROVIDER=openai
TRADINGAGENTS_QUICK_THINK_LLM=gpt-5.4-mini
TRADINGAGENTS_DEEP_THINK_LLM=gpt-5.5
TRADINGAGENTS_LLM_BACKEND_URL=
TRADINGAGENTS_TEMPERATURE=0
```

Regional providers use separate accounts; international and China keys are not interchangeable.
