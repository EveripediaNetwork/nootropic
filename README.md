<div align="center">
  <img src="./misc/nootropic.svg" alt="Logo" height="70" />
  <p><strong>Instant IQ Boost for LLMs</strong></p>
</div>
<br/>

<p align="center">
    <a href="https://pypi.python.org/pypi/nootropic/"><img alt="PyPi" src="https://img.shields.io/pypi/v/nootropic.svg?style=flat-square"></a>
    <a href="https://github.com/EveripediaNetwork/nootropic/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/EveripediaNetwork/nootropic.svg?style=flat-square"></a>
</p>

# Installation

```bash
pip install nootropic
```

# Usage
```python
from nootropic import Nootropic
from openai import OpenAI
from os import environ as env

client = OpenAI(
    api_key=env.get('OPENAI_API_KEY')
)

# Wrap your client with Nootropic
client = Nootropic(
    client,
    # prefix='prompt prefix for every user message',
    # postfix='prompt postfix for every user message',
    system='system prompt for the model',
)

```

# Supported Python SDKs
- LLMDK: [llmdk](https://github.com/EveripediaNetwork/llmdk)
- OpenAI: [openai](https://github.com/openai/openai-python)
- Anthropic: [anthropic](https://github.com/anthropics/anthropic-sdk-python)
- Groq: [groq](https://github.com/groq/groq-python)
- Ollama: [ollama](https://github.com/ollama/ollama-python)
