#!/usr/bin/env python3
"""
Database seeding functionality
This module provides a generic seeding function that accepts JSON data and table information.
"""

from typing import Dict, List, Any, Optional
from .supabase_client import SupabaseClient


def run_seeding(data_sets: List[Dict[str, Any]], verify_data: bool = True, clear_existing: bool = True) -> None:
    """
    Generic seeding function that accepts loaded JSON data and uploads to database.
    
    Args:
        data_sets: List of dictionaries containing:
            - 'table_name': Name of the table to insert into
            - 'data': List of records to insert
            - 'description': Optional description for logging
        verify_data: Whether to verify the data after insertion
        clear_existing: Whether to clear existing data before seeding
    
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
    print("\n" + "=" * 50)
    print("Starting Database Seeding Process")
    print("=" * 50)
    
    # Initialize Supabase client
    supabase_client = SupabaseClient()
    
    # Test connection first
    print("\nTesting Supabase connection...")
    if not supabase_client.test_connection():
        print("[ERROR] Failed to connect to Supabase. Aborting seeding process.")
        return
    
    # Clear existing data if requested
    if clear_existing:
        supabase_client.clear_tables()
    
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
            print(f"[ERROR] Failed to seed {description}")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Seeding Summary: {success_count}/{len(data_sets)} tables seeded successfully")
    print(f"Total records inserted: {total_records}")
    print("=" * 50)
    
    # Verify data if requested
    if verify_data and success_count > 0:
        supabase_client.verify_data()
    
    if success_count == len(data_sets):
        print("\n[SUCCESS] Database seeding completed successfully!")
    else:
        print(f"\n[WARNING] {len(data_sets) - success_count} table(s) failed to seed")
