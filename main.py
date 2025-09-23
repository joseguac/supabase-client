#!/usr/bin/env python3
"""
Main entry point for the Supabase seeding application
This script orchestrates the database seeding process.
"""

import sys
from pathlib import Path
from src.supa.seed_database import run_seeding
from src.utils.json_io import load_json_file




def main():
    """Main function to run the database seeding process."""
    print("=" * 50)
    print("Supabase Database Seeding Application")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(__file__).parent / ".env"
    if not env_file.exists():
        print("[ERROR] .env file not found in the root directory")
        print("Please create a .env file with the following variables:")
        print("SUPABASE_URL=your_supabase_url")
        print("API_Key=your_service_key")
        sys.exit(1)
    
    try:
        # Define data directory and JSON files
        data_dir = Path(__file__).parent / "data"
        categories_file = data_dir / "categories.json"
        menu_items_file = data_dir / "menu_items.json"
        
        # Load JSON data
        print("\nLoading JSON data files...")
        categories_data = load_json_file(categories_file)
        menu_items_data = load_json_file(menu_items_file)
        
        print(f"[SUCCESS] Loaded {len(categories_data)} categories")
        print(f"[SUCCESS] Loaded {len(menu_items_data)} menu items")
        
        # Prepare data sets for seeding
        data_sets = [
            {
                'table_name': 'categories',
                'data': categories_data,
                'description': 'categories'
            },
            {
                'table_name': 'menu_items',
                'data': menu_items_data,
                'description': 'menu items'
            }
        ]
        
        # Run the seeding function with loaded data
        run_seeding(data_sets, verify_data=True, clear_existing=True)
        
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        sys.exit(1)
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        if "JSONDecodeError" in str(type(e)):
            print(f"[ERROR] Invalid JSON format: {e}")
        else:
            print(f"[ERROR] Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
