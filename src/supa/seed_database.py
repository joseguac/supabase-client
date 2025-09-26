#!/usr/bin/env python3
"""
Database seeding functionality
This module provides a generic seeding function that accepts JSON data and table information.
"""

from typing import Dict, List, Any, Optional
from .supabase_client import SupabaseClient
from ..config.constants import MESSAGES, DEFAULTS
from ..config.loader import ConfigLoader


def run_seeding(data_sets: List[Dict[str, Any]], verify_data: bool = True, clear_existing: bool = True, config_loader: Optional[ConfigLoader] = None) -> None:
    """
    Generic seeding function that accepts loaded JSON data and uploads to database.
    
    Args:
        data_sets: List of dictionaries containing:
            - 'table_name': Name of the table to insert into
            - 'data': List of records to insert
            - 'description': Optional description for logging
        verify_data: Whether to verify the data after insertion
        clear_existing: Whether to clear existing data before seeding
        config_loader: Optional configuration loader instance
    
    Example:
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
        run_seeding(data_sets)
    """
    separator = MESSAGES['SEPARATOR']
    print(f"\n{separator}")
    print(MESSAGES['SEEDING_TITLE'])
    print(separator)
    
    # Initialize Supabase client with optional config loader
    supabase_client = SupabaseClient(config_loader=config_loader)
    
    # Test connection first
    print(f"\n{MESSAGES['CONNECTION_TEST']}")
    if not supabase_client.test_connection():
        print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ERROR_CONNECTION']}")
        return
    
    # Clear existing data if requested
    if clear_existing:
        # Extract table names from data sets
        table_names = [data_set['table_name'] for data_set in data_sets]
        supabase_client.clear_tables(table_names=table_names)
    
    # Process each data set
    success_count = 0
    total_records = 0
    
    for data_set in data_sets:
        table_name = data_set['table_name']
        data = data_set['data']
        description = data_set.get('description', table_name)
        
        print(f"\nSeeding {description}...")
        result = supabase_client.insert_data(table_name, data, description)
        
        if result is not None:
            success_count += 1
            total_records += len(data)
        else:
            print(f"{MESSAGES['ERROR_PREFIX']} Failed to seed {description}")
    
    # Summary
    separator = MESSAGES['SEPARATOR']
    print(f"\n{separator}")
    print(MESSAGES['SEEDING_SUMMARY'].format(success=success_count, total=len(data_sets)))
    print(MESSAGES['TOTAL_RECORDS'].format(count=total_records))
    print(separator)
    
    # Verify data if requested
    if verify_data and success_count > 0:
        # Extract table names from successfully seeded data sets
        verified_table_names = [data_set['table_name'] for data_set in data_sets]
        supabase_client.verify_data(table_names=verified_table_names)
    
    if success_count == len(data_sets):
        print(f"\n{MESSAGES['SUCCESS_PREFIX']} {MESSAGES['SEEDING_COMPLETED']}")
    else:
        failed_count = len(data_sets) - success_count
        print(f"\n{MESSAGES['WARNING_PREFIX']} {MESSAGES['SEEDING_FAILED'].format(count=failed_count)}")
