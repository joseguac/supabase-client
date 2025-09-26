"""
Configuration package
Contains all configuration constants and settings for the application.
"""

from .constants import (
    # Table names
    TABLE_NAMES,
    
    # File paths
    DATA_FILES,
    
    # Database operations
    DB_OPERATIONS,
    
    # Messages
    MESSAGES,
    
    # Default values
    DEFAULTS
)

from .loader import ConfigLoader, get_config_loader

__all__ = [
    'TABLE_NAMES',
    'DATA_FILES',
    'DB_OPERATIONS',
    'MESSAGES',
    'DEFAULTS',
    'ConfigLoader',
    'get_config_loader'
]
