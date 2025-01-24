#!/usr/bin/env python3
"""
Test Suite for Simple I/O Program
Version 1.4
Enhanced test coverage for internationalization features
Added comprehensive testing for internationalization features
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from datetime import datetime
from pathlib import Path
from simple_io_v1_3 import ConfigManager, NameValidator, GreetingGenerator, LocaleManager

class TestLocaleManager(unittest.TestCase):
    """Test cases for LocaleManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_locales = {
            "en": {
                "greeting_templates": {
                    "default": "Hello {name}",
                    "formal": "Dear {name},"
                },
                "errors": {
                    "empty_name": "Name cannot be empty"
                }
            },
            "es": {
                "greeting_templates": {
                    "default": "Hola {name}",
                    "formal": "Estimado/a {name}:"
                },
                "errors": {
                    "empty_name": "El nombre no puede estar vacío"
                }
            }
        }
        
        self.config = {
            "default_locale": "en",
            "fallback_locale": "en",
            "available_locales": ["en", "es"]
        }
        
        # Mock file system for locale files
        self.mock_file_system = {
            "locales/en.json": json.dumps(self.test_locales["en"]),
            "locales/es.json": json.dumps(self.test_locales["es"])
        }
    
    @patch('builtins.open', new_callable=mock_open)
    def test_load_translations(self, mock_file):
        """Test loading of translation files."""
        def mock_open_file(filename, *args, **kwargs):
            mock = mock_open(read_data=self.mock_file_system.get(str(filename), ""))()
            mock.name = str(filename)
            return mock
            
        mock_file.side_effect = mock_open_file
        
        locale_manager = LocaleManager("locales", self.config)
        self.assertEqual(
            locale_manager.translations["en"]["greeting_templates"]["default"],
            "Hello {name}"
        )
        self.assertEqual(
            locale_manager.translations["es"]["greeting_templates"]["default"],
            "Hola {name}"
        )
    
    @patch('builtins.open', new_callable=mock_open)
    def test_missing_default_locale(self, mock_file):
        """Test handling of missing default locale file."""
        config = self.config.copy()
        config["default_locale"] = "fr"
        
        with self.assertRaises(ValueError):
            LocaleManager("locales", config)
    
    @patch('builtins.open', new_callable=mock_open)
    def test_get_text_with_params(self, mock_file):
        """Test text retrieval with parameters."""
        mock_file.side_effect = lambda f, *a, **k: mock_open(
            read_data=self.mock_file_system.get(str(f), ""))()
        
        locale_manager = LocaleManager("locales", self.config)
        text = locale_manager.get_text(
            "greeting_templates.default",
            locale="en",
            name="John"
        )
        self.assertEqual(text, "Hello John")
    
    @patch('builtins.open', new_callable=mock_open)
    def test_fallback_behavior(self, mock_file):
        """Test fallback to default locale."""
        mock_file.side_effect = lambda f, *a, **k: mock_open(
            read_data=self.mock_file_system.get(str(f), ""))()
        
        locale_manager = LocaleManager("locales", self.config)
        
        # Test fallback for missing key
        text = locale_manager.get_text("nonexistent.key", locale="es")
        self.assertTrue(text.startswith("Missing translation"))
        
        # Test fallback for missing locale
        text = locale_manager.get_text(
            "greeting_templates.default",
            locale="fr",
            name="John"
        )
        self.assertEqual(text, "Hello John")

class TestNameValidatorWithI18n(unittest.TestCase):
    """Test cases for NameValidator with internationalization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "name_validation": {
                "min_length": 2,
                "max_length": 50,
                "allowed_chars": r"^[A-Za-z\s\-']+$"
            }
        }
        
        # Mock LocaleManager
        self.locale_manager = MagicMock()
        self.locale_manager.get_text.return_value = "Error message"
        
        self.validator = NameValidator(self.config, self.locale_manager)
    
    def test_validation_error_messages(self):
        """Test localized error messages."""
        # Test empty name
        with self.assertRaises(ValueError):
            self.validator.validate("", locale="es")
        self.locale_manager.get_text.assert_called_with(
            "errors.empty_name",
            locale="es"
        )
        
        # Test name too short
        with self.assertRaises(ValueError):
            self.validator.validate("A", locale="es")
        self.locale_manager.get_text.assert_called_with(
            "errors.name_too_short",
            locale="es",
            min_length=2
        )

class TestGreetingGeneratorWithI18n(unittest.TestCase):
    """Test cases for GreetingGenerator with internationalization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = {"greeting_style": "default"}
        self.locale_manager = MagicMock()
        self.generator = GreetingGenerator(self.config, self.locale_manager)
    
    def test_localized_greetings(self):
        """Test generation of localized greetings."""
        self.locale_manager.get_text.return_value = "Hola {name}"
        greeting = self.generator.create_greeting("Juan", locale="es")
        self.assertEqual(greeting, "Hola Juan")
        self.locale_manager.get_text.assert_called_with(
            "greeting_templates.default",
            locale="es"
        )
    
    @patch('datetime.datetime')
    def test_localized_time_greetings(self, mock_datetime):
        """Test generation of time-based localized greetings."""
        mock_datetime.now.return_value = datetime(2025, 1, 10, 9, 0)
        
        self.locale_manager.get_text.side_effect = [
            "{time_greeting} {name}",  # Template
            "Buenos días"              # Time greeting
        ]
        
        greeting = self.generator.create_greeting(
            "Juan",
            style="time",
            locale="es"
        )
        self.assertEqual(greeting, "Buenos días Juan")

def main():
    """Run the test suite."""
    unittest.main()

if __name__ == "__main__":
    main()