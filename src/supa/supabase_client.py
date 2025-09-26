#!/usr/bin/env python3
"""
Supabase Client Class
Encapsulates Supabase client creation and configuration to avoid module-level initialization issues.
"""

import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from gotrue import SyncMemoryStorage

from ..config.constants import (
    TABLE_NAMES, DB_OPERATIONS, MESSAGES, DEFAULTS,
    get_table_deletion_order
)
from ..config.loader import ConfigLoader


class SupabaseClient:
    """Supabase client wrapper class to handle initialization and configuration."""
    
    def __init__(self, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None, config_loader: Optional[ConfigLoader] = None):
        """
        Initialize the Supabase client.
        
        Args:
            supabase_url: Supabase project URL (if None, will load from environment or config)
            supabase_key: Supabase service key (if None, will load from environment or config)
            config_loader: Optional configuration loader instance
        """
        # Load environment variables if not provided
        if not supabase_url or not supabase_key:
            if config_loader:
                try:
                    config = config_loader.get_supabase_config()
                    supabase_url = supabase_url or config['url']
                    supabase_key = supabase_key or config['key']
                except Exception:
                    # Fallback to direct environment loading
                    load_dotenv()
                    supabase_url = supabase_url or os.getenv('SUPABASE_URL')
                    supabase_key = supabase_key or os.getenv('API_Key')
            else:
                load_dotenv()
                supabase_url = supabase_url or os.getenv('SUPABASE_URL')
                supabase_key = supabase_key or os.getenv('API_Key')
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and API_Key must be provided or available in environment variables")
        
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self._client: Optional[Client] = None
    
    def get_client(self) -> Client:
        """
        Get or create the Supabase client.
        
        Returns:
            Configured Supabase client instance
        """
        if self._client is None:
            try:
                # Create client options with explicit configuration
                options = ClientOptions(storage=SyncMemoryStorage())
                
                # Create the client
                self._client = create_client(
                    supabase_url=self.supabase_url,
                    supabase_key=self.supabase_key,
                    options=options
                )
            except Exception as e:
                if "proxy" in str(e).lower():
                    print(f"{MESSAGES['WARNING_PREFIX']} {MESSAGES['PROXY_ERROR']}")
                    # Try creating client without options first
                    try:
                        self._client = create_client(
                            supabase_url=self.supabase_url,
                            supabase_key=self.supabase_key
                        )
                        print(f"{MESSAGES['SUCCESS_PREFIX']} {MESSAGES['CLIENT_CREATED']}")
                    except Exception as e2:
                        print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['ALTERNATIVE_FAILED']}: {e2}")
                        raise e2
                else:
                    raise e
        
        return self._client
    
    def clear_tables(self, table_names: Optional[List[str]] = None, deletion_order: Optional[List[str]] = None) -> None:
        """
        Clear existing data from specified tables.
        
        Args:
            table_names: List of table names to clear. If None, uses default tables.
            deletion_order: Order in which to delete tables (respects foreign key constraints).
                          If None, uses default deletion order.
        """
        print(MESSAGES['CLEARING_DATA'])
        try:
            client = self.get_client()
            
            # Use provided table names or default ones
            if table_names is None:
                deletion_order = deletion_order or get_table_deletion_order()
            else:
                deletion_order = deletion_order or table_names
            
            for table_name in deletion_order:
                # Skip if table_names is specified and current table is not in the list
                if table_names is not None and table_name not in table_names:
                    continue
                    
                # Get delete condition based on table name
                delete_condition = self._get_delete_condition(table_name)
                if delete_condition:
                    client.table(table_name).delete().neq(
                        delete_condition['column'], delete_condition['value']
                    ).execute()
                else:
                    # Fallback: delete all records (use with caution)
                    client.table(table_name).delete().neq('id', 'nonexistent').execute()
                
                print(f"{MESSAGES['SUCCESS_PREFIX']} {MESSAGES['CLEARED_TABLE'].format(table=table_name)}")
            
        except Exception as e:
            print(f"{MESSAGES['WARNING_PREFIX']}: {MESSAGES['ERROR_CLEARING']}: {e}")
    
    def _get_delete_condition(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        Get the appropriate delete condition for a table based on its name.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with delete condition or None if no specific condition
        """
        # Map table names to their delete conditions
        table_conditions = {
            TABLE_NAMES['MENU_ITEMS']: DB_OPERATIONS['DELETE_CONDITIONS']['MENU_ITEMS'],
            TABLE_NAMES['CATEGORIES']: DB_OPERATIONS['DELETE_CONDITIONS']['CATEGORIES']
        }
        
        return table_conditions.get(table_name)
    
    def insert_data(self, table_name: str, data: list, description: Optional[str] = None) -> Optional[list]:
        """
        Generic function to insert data into any table.
        
        Args:
            table_name: Name of the table to insert into
            data: List of dictionaries to insert
            description: Optional description for logging (defaults to table_name)
            
        Returns:
            List of inserted data or None if failed
        """
        description = description or table_name
        print(f"\n{MESSAGES['SEEDING_TITLE'].replace('Starting Database Seeding Process', f'Seeding {description}')}...")
        try:
            client = self.get_client()
            result = client.table(table_name).insert(data).execute()
            print(f"{MESSAGES['SUCCESS_PREFIX']} {MESSAGES['INSERTED_RECORDS'].format(count=len(data), description=description)}")
            return result.data
        except Exception as e:
            print(f"{MESSAGES['ERROR_SEEDING'].format(description=description)}: {e}")
            return None
    
    def verify_data(self, table_names: Optional[List[str]] = None, show_category_breakdown: bool = True) -> Dict[str, int]:
        """
        Verify the seeded data in specified tables.
        
        Args:
            table_names: List of table names to verify. If None, uses default tables.
            show_category_breakdown: Whether to show category breakdown for menu items.
            
        Returns:
            Dictionary with table names as keys and record counts as values
        """
        print(f"\n{MESSAGES['VERIFYING_DATA']}")
        try:
            client = self.get_client()
            
            # Use provided table names or default ones
            if table_names is None:
                table_names = [TABLE_NAMES['CATEGORIES'], TABLE_NAMES['MENU_ITEMS']]
            
            record_counts = {}
            
            # Verify each table
            for table_name in table_names:
                result = client.table(table_name).select('*').execute()
                record_count = len(result.data)
                record_counts[table_name] = record_count
                
                # Determine description based on table name
                description = self._get_table_description(table_name)
                print(f"{MESSAGES['SUCCESS_PREFIX']} {MESSAGES['FOUND_RECORDS'].format(count=record_count, description=description)}")
                
                # Show category breakdown if requested and this is the menu items table
                if show_category_breakdown and table_name == TABLE_NAMES['MENU_ITEMS']:
                    self._show_category_breakdown(result.data)
                    
            return record_counts
                
        except Exception as e:
            print(f"{MESSAGES['ERROR_VERIFYING']}: {e}")
            return {}
    
    def _get_table_description(self, table_name: str) -> str:
        """
        Get a human-readable description for a table name.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Human-readable description
        """
        descriptions = {
            TABLE_NAMES['CATEGORIES']: 'categories',
            TABLE_NAMES['MENU_ITEMS']: 'menu items'
        }
        return descriptions.get(table_name, table_name)
    
    def _show_category_breakdown(self, menu_items_data: List[Dict[str, Any]]) -> None:
        """
        Show category breakdown for menu items.
        
        Args:
            menu_items_data: List of menu item records
        """
        category_counts = {}
        for item in menu_items_data:
            category = item.get('category', DEFAULTS['UNKNOWN_CATEGORY'])
            category_counts[category] = category_counts.get(category, 0) + 1
        
        print(f"\n{MESSAGES['MENU_ITEMS_BY_CATEGORY']}")
        for category, count in category_counts.items():
            print(f"  - {category}: {count} items")
    
    def test_connection(self, test_table: Optional[str] = None) -> bool:
        """
        Test the connection to Supabase.
        
        Args:
            test_table: Table name to use for testing connection. If None, uses default.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            client = self.get_client()
            # Try a simple query to test connection
            test_table = test_table or DB_OPERATIONS['TEST_QUERY_TABLE']
            limit = DB_OPERATIONS['VERIFY_LIMIT']
            result = client.table(test_table).select('*').limit(limit).execute()
            print(f"{MESSAGES['SUCCESS_PREFIX']} {MESSAGES['CONNECTION_SUCCESS']}")
            return True
        except Exception as e:
            print(f"{MESSAGES['ERROR_PREFIX']} {MESSAGES['CONNECTION_FAILED']}: {e}")
            return False
