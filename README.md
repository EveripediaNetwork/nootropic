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
    api_key=env.get('OPENAI_API_KEY'),
)

# Wrap your client with Nootropic
client = Nootropic(
    client,
    # prefix='Prefix for every user message.',
    # postfix='Postfix for every user message.',
    # system='System prompt.',
    # disable_cache=False,
)
```

# Extractors

Nootropic provides built-in extractors to help parse structured data from LLM responses. Here's how to use them:

## XML Extractor

The `XMLExtractor` can parse XML-like structures from the text, returning a list of dictionaries. You can optionally filter by a specific tag.

```python
from nootropic.extractors import XMLExtractor

# Example LLM response with XML
llm_response = '''
Some text...
<person>
    <name>John Doe</name>
    <age>30</age>
</person>
More text...
<person>
    <name>Jane Smith</name>
    <age>25</age>
</person>
Even more text...
'''

# Extract all XML structures
xml_data = XMLExtractor.extract(llm_response)
print('All XML data:', xml_data)

# Extract XML structures with a specific tag
tagged_xml_data = XMLExtractor.extract(
    llm_response,
    tag='person',
)
print('Tagged XML data:', tagged_xml_data)
```

## JSON Extractor

The `JSONExtractor` finds and parses all valid JSON objects in the text, returning a list of parsed JSON objects.

```python
from nootropic.extractors import JSONExtractor

# Example LLM response with JSON
llm_response = '''
Some text...
{"name": "John Doe", "age": 30}
More text...
{"name": "Jane Smith", "age": 25, "city": "New York"}
Even more text...
'''

json_data = JSONExtractor.extract(llm_response)
print('JSON data:', json_data)
```

# Supported SDKs
- LLMDK: [llmdk](https://github.com/EveripediaNetwork/llmdk)
- Anthropic: [anthropic](https://github.com/anthropics/anthropic-sdk-python)
- Groq: [groq](https://github.com/groq/groq-python)
- HuggingFace: [huggingface](https://github.com/huggingface/huggingface_hub)
- Ollama: [ollama](https://github.com/ollama/ollama-python)
- OpenAI: [openai](https://github.com/openai/openai-python)
