#!/usr/bin/env python3
"""
Main entry point for the Supabase seeding application
This script orchestrates the database seeding process.
"""

import sys
from pathlib import Path
from src.supa.seed_database import run_seeding
from src.utils.json_io import load_json_file
from src.config import (
    TABLE_NAMES, MESSAGES, get_config_loader
)




def main():
    """Main function to run the database seeding process."""
    separator = MESSAGES['SEPARATOR']
    print(separator)
    print(MESSAGES['APP_TITLE'])
    print(separator)
    
    # Initialize configuration loader
    base_path = Path(__file__).parent
    config_loader = get_config_loader(base_path)
    
    # Validate configuration
    if not config_loader.validate_configuration():
        print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ERROR_ENV_FILE']}")
        print(MESSAGES['ENV_INSTRUCTIONS'])
        # Hardcoded environment variable names as they are standard
        required_vars = ['SUPABASE_URL', 'API_Key']
        for var in required_vars:
            print(f"{var}=your_value_here")
        sys.exit(1)
    
    try:
        # Get file paths from configuration
        file_paths = config_loader.get_file_paths()
        categories_file = file_paths['categories']
        menu_items_file = file_paths['menu_items']
        
        # Load JSON data
        print("\nLoading JSON data files...")
        categories_data = load_json_file(categories_file)
        menu_items_data = load_json_file(menu_items_file)
        
        print(f"{MESSAGES['SUCCESS_PREFIX']} Loaded {len(categories_data)} categories")
        print(f"{MESSAGES['SUCCESS_PREFIX']} Loaded {len(menu_items_data)} menu items")
        
        # Prepare data sets for seeding using configuration
        data_sets = [
            {
                'table_name': TABLE_NAMES['CATEGORIES'],
                'data': categories_data,
                'description': 'categories'
            },
            {
                'table_name': TABLE_NAMES['MENU_ITEMS'],
                'data': menu_items_data,
                'description': 'menu items'
            }
        ]
        
        # Get data configuration and run seeding
        data_config = config_loader.get_data_config()
        run_seeding(
            data_sets, 
            verify_data=data_config['verify_data'], 
            clear_existing=data_config['clear_existing'],
            config_loader=config_loader
        )
        
    except FileNotFoundError as e:
        print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ERROR_FILE_NOT_FOUND']}: {e}")
        sys.exit(1)
        
    except ImportError as e:
        print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ERROR_IMPORT']}: {e}")
        print(MESSAGES['INSTALL_INSTRUCTIONS'])
        from src.config.constants import DEFAULTS
        print(f"pip install -r {DEFAULTS['REQUIREMENTS_FILE']}")
        sys.exit(1)
        
    except Exception as e:
        if "JSONDecodeError" in str(type(e)):
            print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ERROR_JSON']}: {e}")
        else:
            print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ERROR_UNEXPECTED']}: {e}")
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
