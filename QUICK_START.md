# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install deep-translator>=1.8.1 Flask>=2.0.0 requests>=2.25.0
```

## Quick Usage

### 1. Web Interface
```bash
python translator.py --serve
# Open http://127.0.0.1:5000
```

### 2. Command Line
```bash
python translator.py -t "Hello, how are you?"
```

### 3. From File
```bash
python translator.py -f input.txt
```

### 4. Interactive Mode
```bash
python translator.py
# Type or paste text, then Ctrl+Z + Enter (Windows) or Ctrl+D (Linux/Mac)
```

## Examples

### Basic Translation
```python
from translator import TranslationManager

manager = TranslationManager()
result = manager.translate("Hello World")
print(result)  # ನಮಸ್ಕಾರ ಜಗತ್ತು
```

### Batch Translation
```python
from translator import TranslationManager
from translation_utils import BatchTranslator

manager = TranslationManager()
batch = BatchTranslator(manager)

texts = ["Hello", "World", "Python"]
results = batch.translate_list(texts)

for result in results:
    print(f"{result['source']} → {result['translated']}")
```

### Translation History
```python
from translator import TranslationManager
from translation_utils import TranslationHistory

manager = TranslationManager()
history = TranslationHistory()

# Translate and save to history
text = manager.translate("Hello")
history.add("Hello", text)

# View recent translations
recent = history.get_recent(5)
```

## API Usage

```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello"}'
```

## Running Examples

```bash
python examples.py
```

This will run all 7 example functions demonstrating:
1. Basic translation
2. Paragraph translation
3. Batch translation
4. Text validation
5. Language pairs
6. Translation history
7. Text cleaning
