# English to Kannada Translator

A powerful translator application that converts English text to Kannada using Google Translate API. Supports both command-line and web interfaces.

## Features

- 🌐 **Web Interface**: User-friendly Flask web application
- 💻 **CLI Support**: Command-line interface for quick translations
- 📄 **File Support**: Translate entire text files
- 🔄 **Caching**: Built-in translation caching for better performance
- 🛡️ **Error Handling**: Comprehensive error messages and logging
- 🔌 **API Endpoint**: REST API for programmatic access

## Installation

1. **Clone or navigate to the project directory**:
```bash
cd english-to-kannada-translator
```

2. **Create and activate virtual environment** (optional but recommended):
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On Linux/Mac:
source env/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- Flask 2.0+
- deep-translator 1.8.1+

## Usage

### Web Interface

Start the Flask web server:
```bash
python translator.py --serve
```

Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

With options:
```bash
python translator.py --serve --host 0.0.0.0 --port 8000 --debug
```

### Command Line

**Translate a single text**:
```bash
python translator.py -t "Hello, how are you?"
```

**Translate from a file**:
```bash
python translator.py -f input.txt
```

**Translate from stdin** (interactive mode):
```bash
python translator.py
# Then type or paste your text (Ctrl+Z then Enter on Windows, Ctrl+D on Linux/Mac)
```

**Pipe text**:
```bash
echo "Hello World" | python translator.py
```

### API Endpoint

Send a POST request to `/api/translate`:

```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, World!"}'
```

Response:
```json
{
  "text": "Hello, World!",
  "translated": "ನಮಸ್ಕಾರ, ಪ್ರಪಂಚ!"
}
```

## Code Structure

### Main Components

- **`TranslationManager`**: Core translation class with caching
- **`translate_text()`**: Legacy function for simple translations
- **Web Routes**: Flask routes for web interface and API
- **CLI Interface**: Command-line argument handling

### Example Usage in Python

```python
from translator import TranslationManager

# Initialize translator
manager = TranslationManager()

# Translate single text
result = manager.translate("Hello")
print(result)  # ನಮಸ್ಕಾರ

# Translate with paragraph preservation
text = "Hello\nWorld"
result = manager.translate_paragraph(text)
print(result)
```

## File Structure

```
english-to-kannada-translator/
├── translator.py          # Main application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface template
└── static/
    └── style.css         # Styling
```

## Error Handling

- Empty text detection
- File not found handling
- Network error management
- Request size limit (10MB)
- JSON parsing errors

## Performance

- **Caching**: Frequently translated texts are cached in memory
- **Paragraph Mode**: Preserves formatting for multi-line text
- **Rate Limiting**: Uses Google Translate's rate limits

## Limitations

- Dependent on Google Translate API availability
- Network connection required
- Translation accuracy depends on Google Translate's quality
- Maximum file size: 10MB

## Troubleshooting

**Import Error - `ModuleNotFoundError: No module named 'flask'`**:
```bash
pip install -r requirements.txt
```

**Connection Error**:
- Check your internet connection
- Google Translate API may be rate limited; try again later

**Port Already in Use**:
```bash
python translator.py --serve --port 8000
```

## Future Enhancements

- [ ] Batch translation support
- [ ] Multiple language support
- [ ] Translation history
- [ ] Offline mode with local models
- [ ] Docker support
- [ ] Database for persistent caching

## License

Open source - feel free to use and modify

## Author

Created as an educational project for English-Kannada translation