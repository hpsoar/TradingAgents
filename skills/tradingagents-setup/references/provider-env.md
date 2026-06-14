# Provider Environment

## Supported providers

```
openai, anthropic, google, azure, xai, deepseek,
qwen, qwen-cn, glm, glm-cn, minimax, minimax-cn,
openrouter, ollama
```

Aliases (also accepted):
```
dashscope   → qwen
dashscope_cn → qwen-cn
zhipu       → glm
zhipu_cn    → glm-cn
minimax_cn  → minimax-cn
```

## Credential mapping

| Provider | Env var |
|---|---|
| openai | `OPENAI_API_KEY` |
| google | `GOOGLE_API_KEY` |
| anthropic | `ANTHROPIC_API_KEY` |
| azure | `AZURE_OPENAI_API_KEY` |
| xai | `XAI_API_KEY` |
| deepseek | `DEEPSEEK_API_KEY` |
| qwen | `DASHSCOPE_API_KEY` |
| qwen-cn | `DASHSCOPE_CN_API_KEY` |
| glm | `ZHIPU_API_KEY` |
| glm-cn | `ZHIPU_CN_API_KEY` |
| minimax | `MINIMAX_API_KEY` |
| minimax-cn | `MINIMAX_CN_API_KEY` |
| openrouter | `OPENROUTER_API_KEY` |
| ollama | (none) |

Optional data key: `ALPHA_VANTAGE_API_KEY`
