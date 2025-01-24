#!/usr/bin/env python3
"""
Simple I/O Program v1.3
Enhanced version with internationalization support, configurable greeting formats,
extended input validation, and unit test coverage.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, Union

class LocaleManager:
    """Handles program localization."""
    
    def __init__(self, locale_dir: str, config: Dict):
        """
        Initialize locale manager.
        
        Args:
            locale_dir: Directory containing locale files
            config: Configuration dictionary with locale settings
        """
        self.locale_dir = Path(locale_dir)
        self.config = config
        self.default_locale = config.get("default_locale", "en")
        self.fallback_locale = config.get("fallback_locale", "en")
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict:
        """
        Load all available translations.
        
        Returns:
            Dict: Loaded translations
        """
        translations = {}
        available_locales = self.config.get("available_locales", ["en"])
        
        for locale in available_locales:
            locale_file = self.locale_dir / f"{locale}.json"
            if locale_file.exists():
                try:
                    with open(locale_file, 'r', encoding='utf-8') as f:
                        translations[locale] = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Invalid locale file {locale_file}. Skipping.")
                    if locale == self.default_locale:
                        raise ValueError(f"Default locale {locale} file is invalid")
        
        if not translations:
            raise ValueError("No valid translations found")
        return translations
    
    def get_text(self, key: str, locale: Optional[str] = None, **kwargs) -> str:
        """
        Get translated text for a given key.
        
        Args:
            key: Translation key (dot notation for nested keys)
            locale: Optional locale override
            **kwargs: Format string parameters
            
        Returns:
            str: Translated text
        """
        locale = locale or self.default_locale
        
        # Navigate nested dictionary using key parts
        text = self.translations.get(locale, {})
        for part in key.split('.'):
            if not isinstance(text, dict):
                text = self._fallback_text(key, **kwargs)
                break
            text = text.get(part, None)
            if text is None:
                text = self._fallback_text(key, **kwargs)
                break
        
        if not isinstance(text, str):
            text = self._fallback_text(key, **kwargs)
        
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    
    def _fallback_text(self, key: str, **kwargs) -> str:
        """
        Get fallback text when translation is missing.
        
        Args:
            key: Translation key
            **kwargs: Format string parameters
            
        Returns:
            str: Fallback text
        """
        if self.fallback_locale in self.translations:
            text = self.translations[self.fallback_locale]
            for part in key.split('.'):
                if not isinstance(text, dict):
                    return f"Missing translation: {key}"
                text = text.get(part, f"Missing translation: {key}")
            
            if isinstance(text, str):
                try:
                    return text.format(**kwargs)
                except (KeyError, ValueError):
                    return text
        
        return f"Missing translation: {key}"

class ConfigManager:
    """Handles program configuration settings."""
    
    DEFAULT_CONFIG = {
        "greeting_style": "default",
        "name_validation": {
            "min_length": 2,
            "max_length": 50,
            "allowed_chars": r"^[A-Za-z\s\-']+$"
        },
        "default_locale": "en",
        "fallback_locale": "en",
        "available_locales": ["en", "es", "fr"]
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """
        Load configuration from file or use defaults.
        
        Returns:
            Dict: Configuration dictionary
        """
        if self.config_path and Path(self.config_path).exists():
            try:
                with open(self.config_path, 'r') as f:
                    return {**self.DEFAULT_CONFIG, **json.load(f)}
            except json.JSONDecodeError:
                print(f"Warning: Invalid config file. Using defaults.")
        return self.DEFAULT_CONFIG.copy()

class NameValidator:
    """Handles input name validation."""
    
    def __init__(self, config: Dict, locale_manager: LocaleManager):
        """
        Initialize validator with configuration.
        
        Args:
            config: Configuration dictionary containing validation rules
            locale_manager: LocaleManager instance for error messages
        """
        self.config = config["name_validation"]
        self.locale_manager = locale_manager
    
    def validate(self, name: str, locale: Optional[str] = None) -> str:
        """
        Validate and clean input name.
        
        Args:
            name: Input name string
            locale: Optional locale for error messages
            
        Returns:
            str: Cleaned name string
            
        Raises:
            ValueError: If name is invalid
        """
        name = name.strip()
        
        if not name:
            raise ValueError(
                self.locale_manager.get_text("errors.empty_name", locale=locale)
            )
            
        if len(name) < self.config["min_length"]:
            raise ValueError(
                self.locale_manager.get_text(
                    "errors.name_too_short",
                    locale=locale,
                    min_length=self.config["min_length"]
                )
            )
            
        if len(name) > self.config["max_length"]:
            raise ValueError(
                self.locale_manager.get_text(
                    "errors.name_too_long",
                    locale=locale,
                    max_length=self.config["max_length"]
                )
            )
            
        if not re.match(self.config["allowed_chars"], name):
            raise ValueError(
                self.locale_manager.get_text("errors.invalid_chars", locale=locale)
            )
            
        return name

class GreetingGenerator:
    """Generates formatted greetings."""
    
    def __init__(self, config: Dict, locale_manager: LocaleManager):
        """
        Initialize generator with configuration.
        
        Args:
            config: Configuration dictionary containing greeting settings
            locale_manager: LocaleManager instance for translations
        """
        self.config = config
        self.locale_manager = locale_manager
    
    def _get_time_greeting(self, locale: Optional[str] = None) -> str:
        """
        Get time-appropriate greeting.
        
        Args:
            locale: Optional locale for greeting
            
        Returns:
            str: Time-based greeting prefix
        """
        hour = datetime.now().hour
        if hour < 12:
            key = "time_greetings.morning"
        elif hour < 17:
            key = "time_greetings.afternoon"
        else:
            key = "time_greetings.evening"
        
        return self.locale_manager.get_text(key, locale=locale)
    
    def create_greeting(self, name: str, style: Optional[str] = None,
                       locale: Optional[str] = None) -> str:
        """
        Create formatted greeting.
        
        Args:
            name: Validated name string
            style: Optional greeting style
            locale: Optional locale for greeting
            
        Returns:
            str: Formatted greeting string
        """
        style = style or self.config["greeting_style"]
        template = self.locale_manager.get_text(
            f"greeting_templates.{style}",
            locale=locale
        )
        
        if style == "time":
            return template.format(
                time_greeting=self._get_time_greeting(locale),
                name=name
            )
        return template.format(name=name)

def get_user_name(validator: NameValidator, locale_manager: LocaleManager,
                  locale: Optional[str] = None) -> str:
    """
    Get and validate user name from input.
    
    Args:
        validator: NameValidator instance
        locale_manager: LocaleManager instance
        locale: Optional locale for prompts and errors
        
    Returns:
        str: Validated name string
    """
    while True:
        try:
            prompt = locale_manager.get_text("prompts.enter_name", locale=locale)
            name = input(f"{prompt}: ")
            return validator.validate(name, locale=locale)
        except ValueError as e:
            print(e)