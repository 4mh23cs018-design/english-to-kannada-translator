#!/usr/bin/env python3
"""
Translation utility functions and helpers
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Tuple


class TranslationHistory:
    """Manages translation history with JSON storage"""
    
    def __init__(self, history_file='translation_history.json'):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Save history to file"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add(self, source_text: str, translated_text: str):
        """Add entry to history"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source_text[:100],  # Store first 100 chars
            'translated': translated_text[:100],
            'full_source_length': len(source_text),
            'full_translated_length': len(translated_text)
        }
        self.history.append(entry)
        self.save_history()
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent translations"""
        return self.history[-limit:]
    
    def clear(self):
        """Clear history"""
        self.history = []
        self.save_history()


class TextValidator:
    """Validates and cleans text for translation"""
    
    @staticmethod
    def validate_text(text: str) -> Tuple[bool, str]:
        """Validate text input"""
        if not text:
            return False, "Text is empty"
        
        if len(text) > 10 * 1024 * 1024:  # 10MB
            return False, "Text exceeds maximum size (10MB)"
        
        if text.isspace():
            return False, "Text contains only whitespace"
        
        return True, "Valid"
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text for translation"""
        # Remove extra whitespace but preserve paragraphs
        lines = text.split('\n')
        cleaned_lines = [line.strip() for line in lines]
        return '\n'.join(cleaned_lines)
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Simple language detection (English vs other)"""
        # Count ASCII characters
        ascii_count = sum(1 for c in text if ord(c) < 128)
        if ascii_count / len(text) > 0.7:
            return 'en'
        return 'unknown'


class BatchTranslator:
    """Handles batch translation of multiple texts"""
    
    def __init__(self, translator_manager):
        self.translator = translator_manager
        self.results = []
    
    def translate_list(self, texts: List[str]) -> List[Dict]:
        """Translate a list of texts"""
        self.results = []
        for i, text in enumerate(texts):
            try:
                translated = self.translator.translate(text)
                self.results.append({
                    'index': i,
                    'source': text,
                    'translated': translated,
                    'status': 'success'
                })
            except Exception as e:
                self.results.append({
                    'index': i,
                    'source': text,
                    'error': str(e),
                    'status': 'error'
                })
        return self.results
    
    def translate_file(self, filepath: str, line_by_line: bool = False) -> List[Dict]:
        """Translate content from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if line_by_line:
                lines = content.split('\n')
                return self.translate_list(lines)
            else:
                result = self.translator.translate(content)
                return [{'source': content, 'translated': result, 'status': 'success'}]
        
        except FileNotFoundError:
            return [{'error': f'File not found: {filepath}', 'status': 'error'}]
        except Exception as e:
            return [{'error': str(e), 'status': 'error'}]
    
    def export_results(self, output_file: str, format: str = 'txt'):
        """Export translation results"""
        if format == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                for result in self.results:
                    if result['status'] == 'success':
                        f.write(f"Source: {result['source']}\n")
                        f.write(f"Translated: {result['translated']}\n")
                        f.write("-" * 50 + "\n")
        
        elif format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)


class LanguagePair:
    """Represents a language pair for translation"""
    
    def __init__(self, source: str = 'en', target: str = 'kn'):
        self.source = source
        self.target = target
    
    def swap(self):
        """Swap source and target languages"""
        self.source, self.target = self.target, self.source
    
    def __str__(self):
        return f"{self.source} -> {self.target}"
    
    def __repr__(self):
        return f"LanguagePair('{self.source}', '{self.target}')"


# Common language codes
LANGUAGE_CODES = {
    'en': 'English',
    'kn': 'Kannada',
    'hi': 'Hindi',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'ta': 'Tamil',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'ur': 'Urdu'
}


def get_language_name(code: str) -> str:
    """Get language name from code"""
    return LANGUAGE_CODES.get(code, 'Unknown')


def is_valid_language_code(code: str) -> bool:
    """Check if language code is valid"""
    return code in LANGUAGE_CODES
