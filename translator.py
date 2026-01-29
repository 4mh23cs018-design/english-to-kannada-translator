#!/usr/bin/env python3
c"""
English to Kannada Translator
Supports both CLI and Flask web interface
"""

from deep_translator import GoogleTranslator
from flask import Flask, render_template, request, jsonify
import argparse
import sys
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit


class TranslationManager:
    """Handles translation operations with caching and error management"""
    
    def __init__(self, src_lang='en', target_lang='kn'):
        self.src_lang = src_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source=src_lang, target=target_lang)
        self.cache = {}
    
    def translate(self, text):
        """Translate text with caching"""
        if not text or not text.strip():
            raise ValueError("Empty text provided")
        
        # Check cache
        if text in self.cache:
            return self.cache[text]
        
        # Translate
        translated = self.translator.translate(text)
        self.cache[text] = translated
        return translated
    
    def translate_paragraph(self, text):
        """Translate preserving paragraph structure"""
        paragraphs = text.split('\n')
        translated_paragraphs = [self.translate(p) if p.strip() else '' for p in paragraphs]
        return '\n'.join(translated_paragraphs)


# Initialize translation manager
translation_manager = TranslationManager()


def translate_text(text, src='en', target='kn'):
    """Legacy function for compatibility"""
    translator = GoogleTranslator(source=src, target=target)
    return translator.translate(text)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Main web interface"""
    translated = None
    error = None
    source_text = ''
    
    if request.method == 'POST':
        source_text = request.form.get('text', '').strip()
        
        if not source_text:
            error = 'Please enter text to translate.'
        else:
            try:
                # Check if multiline
                if '\n' in source_text:
                    translated = translation_manager.translate_paragraph(source_text)
                else:
                    translated = translation_manager.translate(source_text)
            except Exception as e:
                error = f'Translation error: {str(e)}'
    
    return render_template('index.html', translated=translated, error=error, source_text=source_text)


@app.route('/api/translate', methods=['POST'])
def api_translate():
    """API endpoint for translations"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Empty text'}), 400
        
        translated = translation_manager.translate(text)
        return jsonify({'text': text, 'translated': translated}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle large file uploads"""
    return jsonify({'error': 'Text too large. Maximum size is 10MB.'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


def cli_main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description='English → Kannada Translator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python translator.py --serve                    # Start web server
  python translator.py -t "Hello"                # Translate text
  python translator.py -f input.txt              # Translate from file
  echo "Hello" | python translator.py            # Pipe text
        '''
    )
    parser.add_argument('--serve', action='store_true', help='Start Flask web server')
    parser.add_argument('--host', default='127.0.0.1', help='Server host (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Server port (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--text', help='Text to translate (English)')
    group.add_argument('-f', '--file', help='Path to text file to translate')
    
    args = parser.parse_args()

    if args.serve:
        print(f'Starting server on {args.host}:{args.port}...')
        app.run(host=args.host, port=args.port, debug=args.debug)
        return

    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as fh:
                text = fh.read()
        except FileNotFoundError:
            print(f'Error: File "{args.file}" not found.', file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f'Error reading file: {e}', file=sys.stderr)
            sys.exit(1)
    else:
        print('Enter text to translate (Ctrl+Z then Enter on Windows, Ctrl+D on Linux/Mac):')
        text = sys.stdin.read().strip()

    if not text:
        print('No text provided.', file=sys.stderr)
        sys.exit(1)

    try:
        if '\n' in text:
            out = translation_manager.translate_paragraph(text)
        else:
            out = translation_manager.translate(text)
        print(out)
    except Exception as e:
        print('Translation error:', str(e), file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    cli_main()
