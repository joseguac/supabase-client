"""
Configuration constants
All hardcoded values are centralized here for easy maintenance and configuration.
"""

from typing import Dict, List, Any
from pathlib import Path


# Table names used in the database
TABLE_NAMES = {
    'CATEGORIES': 'categories',
    'MENU_ITEMS': 'menu_items'
}

# Environment variable names are hardcoded directly in the code as they are standard

# Data file paths and names
DATA_FILES = {
    'CATEGORIES_FILE': 'categories.json',
    'MENU_ITEMS_FILE': 'menu_items.json',
    'DATA_DIR': 'data'
}

# Database operation constants
DB_OPERATIONS = {
    'DELETE_CONDITIONS': {
        'MENU_ITEMS': {
            'condition': 'neq',
            'value': 'nonexistent',
            'column': 'id'
        },
        'CATEGORIES': {
            'condition': 'gte', 
            'value': 0,
            'column': 'id'
        }
    },
    'VERIFY_LIMIT': 1,
    'TEST_QUERY_TABLE': 'categories'
}

# Application messages
MESSAGES = {
    'APP_TITLE': 'Supabase Database Seeding Application',
    'SEEDING_TITLE': 'Starting Database Seeding Process',
    'SUCCESS_PREFIX': '[SUCCESS]',
    'ERROR_PREFIX': '[ERROR]',
    'WARNING_PREFIX': '[WARNING]',
    'SEPARATOR': '=' * 50,
    'CONNECTION_TEST': 'Testing Supabase connection...',
    'CLEARING_DATA': 'Clearing existing data...',
    'VERIFYING_DATA': 'Verifying seeded data...',
    'SEEDING_SUMMARY': 'Seeding Summary: {success}/{total} tables seeded successfully',
    'TOTAL_RECORDS': 'Total records inserted: {count}',
    'MENU_ITEMS_BY_CATEGORY': 'Menu items by category:',
    'SEEDING_COMPLETED': 'Database seeding completed successfully!',
    'SEEDING_FAILED': '{count} table(s) failed to seed',
    'CONNECTION_SUCCESS': 'Connection test successful',
    'CONNECTION_FAILED': 'Connection test failed',
    'CLIENT_CREATED': 'Client created successfully without explicit options',
    'PROXY_ERROR': 'Proxy error detected, trying alternative client creation...',
    'ALTERNATIVE_FAILED': 'Alternative client creation also failed',
    'CLEARED_TABLE': 'Cleared {table} table',
    'INSERTED_RECORDS': 'Inserted {count} {description}',
    'FOUND_RECORDS': 'Found {count} {description} in database',
    'ERROR_SEEDING': 'Error seeding {description}',
    'ERROR_CLEARING': 'Error clearing tables',
    'ERROR_VERIFYING': 'Error verifying data',
    'ERROR_FILE_NOT_FOUND': 'File not found',
    'ERROR_IMPORT': 'Import error',
    'ERROR_JSON': 'Invalid JSON format',
    'ERROR_UNEXPECTED': 'Unexpected error',
    'ERROR_ENV_FILE': '.env file not found in the root directory',
    'ERROR_CONNECTION': 'Failed to connect to Supabase. Aborting seeding process.',
    'ENV_INSTRUCTIONS': 'Please create a .env file with the following variables:',
    'INSTALL_INSTRUCTIONS': 'Make sure all required packages are installed:'
}

# Default values and settings
DEFAULTS = {
    'VERIFY_DATA': True,
    'CLEAR_EXISTING': True,
    'LIMIT_DEFAULT': 1,
    'UNKNOWN_CATEGORY': 'Unknown',
    'REQUIREMENTS_FILE': 'requirements.txt',
    'ENV_FILE': '.env',
    'ENCODING': 'utf-8'
}

# File path configurations
def get_data_file_paths(base_path: Path) -> Dict[str, Path]:
    """
    Generate file paths for data files based on base path.
    
    Args:
        base_path: Base directory path
        
    Returns:
        Dictionary mapping file types to their paths
    """
    data_dir = base_path / DATA_FILES['DATA_DIR']
    return {
        'data_dir': data_dir,
        'categories': data_dir / DATA_FILES['CATEGORIES_FILE'],
        'menu_items': data_dir / DATA_FILES['MENU_ITEMS_FILE'],
        'env_file': base_path / DEFAULTS['ENV_FILE']
    }

# Environment variable validation (hardcoded as they are standard)
def get_required_env_vars() -> List[str]:
    """Get list of required environment variables."""
    return ['SUPABASE_URL', 'API_Key']

# Table deletion order (for foreign key constraints)
def get_table_deletion_order() -> List[str]:
    """Get the order in which tables should be deleted to respect foreign key constraints."""
    return [TABLE_NAMES['MENU_ITEMS'], TABLE_NAMES['CATEGORIES']]

# Table insertion order (for foreign key constraints)
def get_table_insertion_order() -> List[str]:
    """Get the order in which tables should be inserted to respect foreign key constraints."""
    return [TABLE_NAMES['CATEGORIES'], TABLE_NAMES['MENU_ITEMS']]
