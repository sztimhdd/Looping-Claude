from typing import Dict, Optional, List, Any
import json
from pathlib import Path
import unicodedata
import re
from dataclasses import dataclass
from enum import Enum
import logging

class TextDirection(Enum):
    """Text direction enumeration."""
    LTR = "ltr"
    RTL = "rtl"
    MIXED = "mixed"

@dataclass
class LocaleMetadata:
    """Metadata for locale configuration."""
    code: str
    name: str
    native_name: str
    direction: TextDirection
    fallback_chain: List[str]
    number_format: Dict[str, str]
    date_format: Dict[str, str]
    plural_rules: Dict[str, str]

class LocaleManager:
    """Enhanced locale manager with support for RTL and Asian languages."""
    
    def __init__(self, locale_dir: str, config: Dict):
        """
        Initialize enhanced locale manager.
        
        Args:
            locale_dir: Directory containing locale files
            config: Configuration dictionary with locale settings
        """
        self.locale_dir = Path(locale_dir)
        self.config = config
        self.default_locale = config.get("default_locale", "en")
        self.fallback_locale = config.get("fallback_locale", "en")
        self.cached_translations: Dict[str, Dict] = {}
        self.metadata_cache: Dict[str, LocaleMetadata] = {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize locale data
        self._init_locale_metadata()
        self._load_required_translations()

    def _init_locale_metadata(self) -> None:
        """Initialize locale metadata for all available locales."""
        metadata_file = self.locale_dir / "metadata.json"
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata_data = json.load(f)
                
            for locale_code, meta in metadata_data.items():
                self.metadata_cache[locale_code] = LocaleMetadata(
                    code=locale_code,
                    name=meta["name"],
                    native_name=meta["native_name"],
                    direction=TextDirection(meta["direction"]),
                    fallback_chain=meta.get("fallback_chain", [self.fallback_locale]),
                    number_format=meta.get("number_format", {}),
                    date_format=meta.get("date_format", {}),
                    plural_rules=meta.get("plural_rules", {})
                )
        except Exception as e:
            self.logger.error(f"Error loading metadata: {e}")
            raise ValueError(f"Failed to initialize locale metadata: {e}")

    def _load_required_translations(self) -> None:
        """Load translations for default and fallback locales."""
        required_locales = {self.default_locale, self.fallback_locale}
        for locale in required_locales:
            self._load_locale_translations(locale)

    def _load_locale_translations(self, locale: str) -> Dict:
        """
        Load translations for a specific locale.
        
        Args:
            locale: Locale code to load
            
        Returns:
            Dict: Loaded translations
        """
        if locale in self.cached_translations:
            return self.cached_translations[locale]
            
        locale_file = self.locale_dir / f"{locale}.json"
        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                self.cached_translations[locale] = translations
                return translations
        except Exception as e:
            self.logger.error(f"Error loading translations for {locale}: {e}")
            raise ValueError(f"Failed to load translations for {locale}: {e}")

    def get_text(self, key: str, locale: Optional[str] = None,
                 fallback_chain: Optional[List[str]] = None,
                 **kwargs) -> str:
        """
        Get translated text with enhanced fallback support.
        
        Args:
            key: Translation key
            locale: Target locale
            fallback_chain: Optional custom fallback chain
            **kwargs: Format string parameters
            
        Returns:
            str: Translated text
        """
        locale = locale or self.default_locale
        if locale not in self.metadata_cache:
            self.logger.warning(f"Locale {locale} not found in metadata")
            locale = self.default_locale
            
        # Use custom fallback chain or get from metadata
        fallback_chain = fallback_chain or self.metadata_cache[locale].fallback_chain
        
        # Try each locale in the fallback chain
        for fallback_locale in [locale] + fallback_chain:
            try:
                translations = self._load_locale_translations(fallback_locale)
                text = self._get_nested_value(translations, key)
                if text:
                    return self._format_text(text, kwargs, locale)
            except Exception as e:
                self.logger.debug(f"Fallback to next locale due to: {e}")
                continue
                
        return f"Missing translation: {key}"

    def _get_nested_value(self, data: Dict, key: str) -> Optional[str]:
        """
        Get nested dictionary value using dot notation.
        
        Args:
            data: Dictionary to search
            key: Dot-notated key
            
        Returns:
            Optional[str]: Found value or None
        """
        current = data
        for part in key.split('.'):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
        return current if isinstance(current, str) else None

    def _format_text(self, text: str, params: Dict[str, Any],
                    locale: str) -> str:
        """
        Format text with parameters, handling RTL and special characters.
        
        Args:
            text: Text to format
            params: Format parameters
            locale: Current locale
            
        Returns:
            str: Formatted text
        """
        # Get text direction
        direction = self.metadata_cache[locale].direction
        
        # Handle RTL text if needed
        if direction == TextDirection.RTL:
            text = self._handle_rtl_text(text)
            
        # Format with parameters
        try:
            return text.format(**params)
        except KeyError as e:
            self.logger.warning(f"Missing format parameter: {e}")
            return text
        except ValueError as e:
            self.logger.warning(f"Invalid format string: {e}")
            return text

    def _handle_rtl_text(self, text: str) -> str:
        """
        Handle right-to-left text formatting.
        
        Args:
            text: Input text
            
        Returns:
            str: Formatted RTL text
        """
        # Add RTL marks and handle mixed content
        if self._has_mixed_content(text):
            return self._format_mixed_direction_text(text)
        return f"\u200F{text}\u200F"  # RLM marks

    def _has_mixed_content(self, text: str) -> bool:
        """
        Check if text contains mixed RTL and LTR content.
        
        Args:
            text: Text to check
            
        Returns:
            bool: True if mixed content
        """
        has_rtl = bool(re.search(r'[\u0591-\u07FF\uFB1D-\uFDFD\uFE70-\uFEFC]', text))
        has_ltr = bool(re.search(r'[A-Za-z]', text))
        return has_rtl and has_ltr

    def _format_mixed_direction_text(self, text: str) -> str:
        """
        Format text with mixed RTL and LTR content.
        
        Args:
            text: Mixed direction text
            
        Returns:
            str: Properly formatted text
        """
        # Split into RTL and LTR segments and format each appropriately
        segments = []
        current_segment = []
        current_direction = None
        
        for char in text:
            char_direction = unicodedata.bidirectional(char)
            if char_direction in ('R', 'AL'):
                if current_direction == 'LTR':
                    segments.append(('LTR', ''.join(current_segment)))
                    current_segment = []
                current_direction = 'RTL'
            elif char_direction == 'L':
                if current_direction == 'RTL':
                    segments.append(('RTL', ''.join(current_segment)))
                    current_segment = []
                current_direction = 'LTR'
            current_segment.append(char)
            
        if current_segment:
            segments.append((current_direction, ''.join(current_segment)))
            
        # Format each segment with appropriate directional marks
        formatted_segments = []
        for direction, segment in segments:
            if direction == 'RTL':
                formatted_segments.append(f"\u200F{segment}\u200F")
            else:
                formatted_segments.append(f"\u200E{segment}\u200E")
                
        return ''.join(formatted_segments)

    def get_locale_info(self, locale: str) -> LocaleMetadata:
        """
        Get locale metadata.
        
        Args:
            locale: Locale code
            
        Returns:
            LocaleMetadata: Locale metadata
            
        Raises:
            ValueError: If locale not found
        """
        if locale not in self.metadata_cache:
            raise ValueError(f"Locale {locale} not found")
        return self.metadata_cache[locale]

    def format_number(self, number: float, locale: str) -> str:
        """
        Format number according to locale conventions.
        
        Args:
            number: Number to format
            locale: Target locale
            
        Returns:
            str: Formatted number
        """
        locale_info = self.get_locale_info(locale)
        format_info = locale_info.number_format
        
        # Convert to string with proper decimal places
        str_num = f"{number:,.{format_info.get('decimal_places', 2)}f}"
        
        # Replace decimal and thousand separators
        str_num = str_num.replace(',', format_info.get('thousand_sep', ','))
        str_num = str_num.replace('.', format_info.get('decimal_sep', '.'))
        
        return str_num

    def format_date(self, date_obj: Any, locale: str,
                   format_key: str = 'default') -> str:
        """
        Format date according to locale conventions.
        
        Args:
            date_obj: Date object to format
            locale: Target locale
            format_key: Format style key
            
        Returns:
            str: Formatted date
        """
        locale_info = self.get_locale_info(locale)
        date_formats = locale_info.date_format
        date_format = date_formats.get(format_key, date_formats.get('default'))
        
        try:
            return date_obj.strftime(date_format)
        except Exception as e:
            self.logger.error(f"Date formatting error: {e}")
            return str(date_obj)