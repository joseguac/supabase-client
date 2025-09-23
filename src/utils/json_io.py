import json
from pathlib import Path


def load_json_file(file_path: Path) -> list:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as a list
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
