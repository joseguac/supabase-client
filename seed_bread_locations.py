#!/usr/bin/env python3
"""
Seed bread locations data into Supabase
Run this script to populate the bread_locations table with initial data.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.supa.seed_database import run_seeding
from src.supa.seed_bread_locations import get_initial_bread_locations, get_table_name
from src.config.loader import ConfigLoader


def main():
    """Main function to seed bread locations data."""
    try:
        # Initialize config loader
        config_loader = ConfigLoader()
        
        # Get initial bread locations data
        bread_locations_data = get_initial_bread_locations()
        table_name = get_table_name()
        
        # Prepare data set for seeding
        data_sets = [
            {
                'table_name': table_name,
                'data': bread_locations_data,
                'description': 'bread locations'
            }
        ]
        
        # Run the seeding process
        print("🍞 Seeding Bread Locations Data")
        print("=" * 50)
        run_seeding(
            data_sets=data_sets,
            verify_data=True,
            clear_existing=True,
            config_loader=config_loader
        )
        
    except Exception as e:
        print(f"❌ Error seeding bread locations: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
