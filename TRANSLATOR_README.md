# English → Kannada Translator (Python)

Simple command-line translator that uses Google Translate via `deep-translator`.

Requirements
- Python 3.7+
- Install dependencies:

```powershell
pip install -r requirements.txt
```

Usage
- Translate a literal string:

```powershell
python translator.py --text "Hello, how are you?"
```

- Translate a file:

```powershell
python translator.py --file sample.txt
```

- Or type/paste text and finish with Ctrl+Z then Enter on Windows:

```powershell
python translator.py
```

Notes
- This uses the `deep-translator` package which uses Google Translate under the hood.
- If you need batch translations or a GUI, I can extend this.
