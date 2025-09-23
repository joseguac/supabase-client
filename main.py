#!/usr/bin/env python3
"""
Main entry point for the Supabase seeding application
This script orchestrates the database seeding process.
"""

import os
import sys
from pathlib import Path
from src.supa.seed_database import run_seeding

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))


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
        # Run the seeding function
        run_seeding()
        
    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
