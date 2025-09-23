"""
Supabase utilities package
Contains all Supabase-related functionality for database operations.
"""

from .supabase_client import SupabaseClient
from .seed_database import run_seeding as seed_database

__all__ = ['SupabaseClient', 'seed_database']
