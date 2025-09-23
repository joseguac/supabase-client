#!/usr/bin/env python3
"""
Supabase Client Class
Encapsulates Supabase client creation and configuration to avoid module-level initialization issues.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from gotrue import SyncMemoryStorage


class SupabaseClient:
    """Supabase client wrapper class to handle initialization and configuration."""
    
    def __init__(self, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None):
        """
        Initialize the Supabase client.
        
        Args:
            supabase_url: Supabase project URL (if None, will load from environment)
            supabase_key: Supabase service key (if None, will load from environment)
        """
        # Load environment variables if not provided
        if not supabase_url or not supabase_key:
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
                    print("[WARNING] Proxy error detected, trying alternative client creation...")
                    # Try creating client without options first
                    try:
                        self._client = create_client(
                            supabase_url=self.supabase_url,
                            supabase_key=self.supabase_key
                        )
                        print("[SUCCESS] Client created successfully without explicit options")
                    except Exception as e2:
                        print(f"[ERROR] Alternative client creation also failed: {e2}")
                        raise e2
                else:
                    raise e
        
        return self._client
    
    def clear_tables(self) -> None:
        """Clear existing data from tables."""
        print("Clearing existing data...")
        try:
            client = self.get_client()
            
            # Delete menu items first (due to foreign key constraints)
            # Use a condition that works for string IDs
            client.table('menu_items').delete().neq('id', 'nonexistent').execute()
            print("[SUCCESS] Cleared menu_items table")
            
            # Delete categories - use a condition that works for integer IDs
            client.table('categories').delete().gte('id', 0).execute()
            print("[SUCCESS] Cleared categories table")
            
        except Exception as e:
            print(f"Warning: Error clearing tables: {e}")
    
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
        print(f"\nSeeding {description}...")
        try:
            client = self.get_client()
            result = client.table(table_name).insert(data).execute()
            print(f"[SUCCESS] Inserted {len(data)} {description}")
            return result.data
        except Exception as e:
            print(f"Error seeding {description}: {e}")
            return None
    
    def verify_data(self) -> None:
        """Verify the seeded data."""
        print("\nVerifying seeded data...")
        try:
            client = self.get_client()
            
            # Check categories
            categories_result = client.table('categories').select('*').execute()
            print(f"[SUCCESS] Found {len(categories_result.data)} categories in database")
            
            # Check menu items
            menu_items_result = client.table('menu_items').select('*').execute()
            print(f"[SUCCESS] Found {len(menu_items_result.data)} menu items in database")
            
            # Show category breakdown
            category_counts = {}
            for item in menu_items_result.data:
                category = item.get('category', 'Unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            print("\nMenu items by category:")
            for category, count in category_counts.items():
                print(f"  - {category}: {count} items")
                
        except Exception as e:
            print(f"Error verifying data: {e}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to Supabase.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            client = self.get_client()
            # Try a simple query to test connection
            result = client.table('categories').select('*').limit(1).execute()
            print("[SUCCESS] Connection test successful")
            return True
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
            return False
