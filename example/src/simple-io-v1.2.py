#!/usr/bin/env python3
"""
Simple I/O Program v1.2
Enhanced version with configurable greeting formats, extended input validation,
and unit test coverage.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

class ConfigManager:
    """Handles program configuration settings."""
    
    DEFAULT_CONFIG = {
        "greeting_style": "default",
        "name_validation": {
            "min_length": 2,
            "max_length": 50,
            "allowed_chars": r"^[A-Za-z\s\-']+$"
        },
        "greeting_templates": {
            "default": "Hello {name}",
            "formal": "Dear {name},",
            "casual": "Hey {name}!",
            "time": "{time_greeting} {name}"
        }
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
    
    def __init__(self, config: Dict):
        """
        Initialize validator with configuration.
        
        Args:
            config: Configuration dictionary containing validation rules
        """
        self.config = config["name_validation"]
    
    def validate(self, name: str) -> str:
        """
        Validate and clean input name.
        
        Args:
            name: Input name string
            
        Returns:
            str: Cleaned name string
            
        Raises:
            ValueError: If name is invalid
        """
        name = name.strip()
        
        if not name:
            raise ValueError("Name cannot be empty")
            
        if len(name) < self.config["min_length"]:
            raise ValueError(f"Name must be at least {self.config['min_length']} characters long")
            
        if len(name) > self.config["max_length"]:
            raise ValueError(f"Name cannot exceed {self.config['max_length']} characters")
            
        if not re.match(self.config["allowed_chars"], name):
            raise ValueError("Name contains invalid characters")
            
        return name

class GreetingGenerator:
    """Generates formatted greetings."""
    
    def __init__(self, config: Dict):
        """
        Initialize generator with configuration.
        
        Args:
            config: Configuration dictionary containing greeting templates
        """
        self.config = config
        self.templates = config["greeting_templates"]
    
    def _get_time_greeting(self) -> str:
        """
        Get time-appropriate greeting.
        
        Returns:
            str: Time-based greeting prefix
        """
        hour = datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"
    
    def create_greeting(self, name: str, style: Optional[str] = None) -> str:
        """
        Create formatted greeting.
        
        Args:
            name: Validated name string
            style: Optional greeting style
            
        Returns:
            str: Formatted greeting string
        """
        style = style or self.config["greeting_style"]
        template = self.templates.get(style, self.templates["default"])
        
        if style == "time":
            return template.format(time_greeting=self._get_time_greeting(), name=name)
        return template.format(name=name)

def get_user_name(validator: NameValidator) -> str:
    """
    Get and validate user name from input.
    
    Args:
        validator: NameValidator instance
        
    Returns:
        str: Validated name string
    """
    while True:
        try:
            name = input("Please enter your name: ")
            return validator.validate(name)
        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again.")

def main(config_path: Optional[str] = None):
    """
    Main program flow.
    
    Args:
        config_path: Optional path to configuration file
    """
    try:
        # Initialize components
        config_manager = ConfigManager(config_path)
        validator = NameValidator(config_manager.config)
        generator = GreetingGenerator(config_manager.config)
        
        # Get and validate input
        name = get_user_name(validator)
        
        # Generate and display greeting
        greeting = generator.create_greeting(name)
        print(greeting)
        
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()