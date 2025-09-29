#!/usr/bin/env python3
"""
Seed script for bread_locations table
Contains initial data for the "Where Has Our Bread Been?" feature
"""

from typing import List, Dict, Any

def get_initial_bread_locations() -> List[Dict[str, Any]]:
    """
    Get initial bread location data for seeding the database.
    
    Returns:
        List of bread location dictionaries
    """
    return [
        {
            "city": "Dallas",
            "state_province": "Texas",
            "country": "United States",
            "latitude": 32.7767,
            "longitude": -96.7970,
            "customer_story": "My daughter moved to Dallas for work and I bring her fresh conchas every time I visit. She says it reminds her of home.",
            "customer_name": "Maria G.",
            "is_approved": True
        },
        {
            "city": "Toronto",
            "state_province": "Ontario",
            "country": "Canada",
            "latitude": 43.6532,
            "longitude": -79.3832,
            "customer_story": "I moved to Toronto for university and my mom ships me pan dulce every month. My roommates are now addicted too!",
            "customer_name": "Carlos M.",
            "is_approved": True
        },
        {
            "city": "Honolulu",
            "state_province": "Hawaii",
            "country": "United States",
            "latitude": 21.3099,
            "longitude": -157.8581,
            "customer_story": "We took your tres leches cake to our family reunion in Hawaii. Everyone wanted to know where we got it!",
            "customer_name": "Rosa L.",
            "is_approved": True
        },
        {
            "city": "Phoenix",
            "state_province": "Arizona",
            "country": "United States",
            "latitude": 33.4484,
            "longitude": -112.0740,
            "customer_story": "My son lives in Phoenix and I always pack a box of your pastries when I visit. His neighbors love them!",
            "customer_name": "Elena S.",
            "is_approved": True
        },
        {
            "city": "Los Angeles",
            "state_province": "California",
            "country": "United States",
            "latitude": 34.0522,
            "longitude": -118.2437,
            "customer_story": "I brought your churros to my cousin's wedding in LA. The whole family was asking for your bakery's information!",
            "customer_name": "Miguel R.",
            "is_approved": True
        },
        {
            "city": "Chicago",
            "state_province": "Illinois",
            "country": "United States",
            "latitude": 41.8781,
            "longitude": -87.6298,
            "customer_story": "My daughter goes to school in Chicago. Every care package includes your pan de muerto - it's her favorite!",
            "customer_name": "Carmen D.",
            "is_approved": True
        },
        {
            "city": "Mexico City",
            "state_province": "Mexico City",
            "country": "Mexico",
            "latitude": 19.4326,
            "longitude": -99.1332,
            "customer_story": "I took your rosca de reyes to my family in Mexico City. They said it tastes just like abuela's!",
            "customer_name": "Ana P.",
            "is_approved": True
        },
        {
            "city": "Denver",
            "state_province": "Colorado",
            "country": "United States",
            "latitude": 39.7392,
            "longitude": -104.9903,
            "customer_story": "My brother moved to Denver and I always bring him empanadas when I visit. He shares them with his coworkers!",
            "customer_name": "Luis G.",
            "is_approved": True
        }
    ]

def get_table_name() -> str:
    """Get the table name for bread locations."""
    return "bread_locations"
