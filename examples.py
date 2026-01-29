#!/usr/bin/env python3
"""
Example usage of the English to Kannada Translator
"""

from translator import TranslationManager
from translation_utils import (
    TranslationHistory, TextValidator, BatchTranslator, 
    LanguagePair, LANGUAGE_CODES
)


def example_basic_translation():
    """Example 1: Basic translation"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Translation")
    print("=" * 60)
    
    manager = TranslationManager()
    
    texts = [
        "Hello",
        "Good morning",
        "How are you?",
        "I love programming"
    ]
    
    for text in texts:
        try:
            result = manager.translate(text)
            print(f"EN: {text}")
            print(f"KN: {result}")
            print()
        except Exception as e:
            print(f"Error: {e}\n")


def example_paragraph_translation():
    """Example 2: Paragraph translation"""
    print("=" * 60)
    print("EXAMPLE 2: Paragraph Translation")
    print("=" * 60)
    
    manager = TranslationManager()
    
    text = """Good morning everyone.
I am learning Python programming.
This is an amazing experience.
Thank you for your support."""
    
    try:
        result = manager.translate_paragraph(text)
        print("Original:")
        print(text)
        print("\nTranslated:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")


def example_batch_translation():
    """Example 3: Batch translation"""
    print("=" * 60)
    print("EXAMPLE 3: Batch Translation")
    print("=" * 60)
    
    manager = TranslationManager()
    batch = BatchTranslator(manager)
    
    texts = [
        "Welcome",
        "Thank you",
        "Please help me",
        "Good bye"
    ]
    
    results = batch.translate_list(texts)
    
    for result in results:
        if result['status'] == 'success':
            print(f"✓ {result['source']} → {result['translated']}")
        else:
            print(f"✗ {result['source']} (Error: {result['error']})")


def example_text_validation():
    """Example 4: Text validation"""
    print("=" * 60)
    print("EXAMPLE 4: Text Validation")
    print("=" * 60)
    
    validator = TextValidator()
    
    test_texts = [
        "Valid text",
        "",
        "   ",
        "Another valid sentence"
    ]
    
    for text in test_texts:
        valid, message = validator.validate_text(text)
        status = "✓ Valid" if valid else "✗ Invalid"
        print(f"{status}: '{text[:30]}...' - {message}")
    
    print("\nLanguage Detection:")
    english_text = "Hello World, this is English"
    detected = validator.detect_language(english_text)
    print(f"Text: '{english_text}'")
    print(f"Detected Language: {detected}")


def example_language_pairs():
    """Example 5: Language pairs"""
    print("=" * 60)
    print("EXAMPLE 5: Language Pairs and Codes")
    print("=" * 60)
    
    pair = LanguagePair('en', 'kn')
    print(f"Current pair: {pair}")
    
    print("\nAvailable languages:")
    for code, name in LANGUAGE_CODES.items():
        print(f"  {code}: {name}")


def example_translation_history():
    """Example 6: Translation history"""
    print("=" * 60)
    print("EXAMPLE 6: Translation History")
    print("=" * 60)
    
    manager = TranslationManager()
    history = TranslationHistory()
    
    # Translate some texts
    texts = ["Hello", "World", "Python"]
    
    for text in texts:
        try:
            translated = manager.translate(text)
            history.add(text, translated)
            print(f"✓ Translated: {text}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\nRecent translations:")
    recent = history.get_recent(5)
    for entry in recent:
        print(f"  {entry['source']} → {entry['translated']}")


def example_text_cleaning():
    """Example 7: Text cleaning"""
    print("=" * 60)
    print("EXAMPLE 7: Text Cleaning")
    print("=" * 60)
    
    validator = TextValidator()
    
    messy_text = """   Hello    world   
    
    This   has   extra    spaces   
    and weird formatting   """
    
    print("Original text:")
    print(repr(messy_text))
    
    cleaned = validator.clean_text(messy_text)
    print("\nCleaned text:")
    print(repr(cleaned))


def run_all_examples():
    """Run all examples"""
    examples = [
        example_basic_translation,
        example_paragraph_translation,
        example_batch_translation,
        example_text_validation,
        example_language_pairs,
        example_translation_history,
        example_text_cleaning
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"Error in {example_func.__name__}: {e}")
        print()


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("ENGLISH TO KANNADA TRANSLATOR - EXAMPLES")
    print("=" * 60 + "\n")
    
    # Uncomment the example you want to run:
    
    run_all_examples()
    
    # Or run individual examples:
    # example_basic_translation()
    # example_paragraph_translation()
    # example_batch_translation()
    # example_text_validation()
    # example_language_pairs()
    # example_translation_history()
    # example_text_cleaning()
