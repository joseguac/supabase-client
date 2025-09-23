# Supabase Database Seeding Tool

A modular and flexible Python application for seeding Supabase databases with JSON data. This tool provides a clean, maintainable way to populate your database tables with initial data.

## Features

- 🎯 **Generic & Modular**: Single function handles any table with any data structure
- 📁 **JSON-Based**: Load data from JSON files with automatic validation
- 🔄 **Flexible Configuration**: Easy to add new tables and data sources
- 🧹 **Smart Cleanup**: Optional table clearing before seeding
- ✅ **Data Verification**: Automatic verification of seeded data
- 🛡️ **Error Handling**: Comprehensive error handling with clear messages
- 🔌 **Environment-Based**: Secure configuration via environment variables

## Project Structure

```
supabase/
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (create this)
├── data/                     # JSON data files
│   ├── categories.json
│   └── menu_items.json
└── src/
    ├── supa/
    │   ├── __init__.py
    │   ├── supabase_client.py    # Supabase client wrapper
    │   └── seed_database.py      # Generic seeding logic
    └── utils/
        ├── __init__.py
        └── json_io.py            # JSON file utilities
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_project_url
API_Key=your_supabase_service_role_key
```

### 3. Prepare Your Data

Add your JSON data files to the `data/` directory. Example structure:

**data/categories.json:**
```json
[
  {
    "name": "Category 1",
    "description": "Description for category 1",
    "slug": "category-1"
  }
]
```

**data/menu_items.json:**
```json
[
  {
    "id": "item-1",
    "title": "Item 1",
    "description": "Description for item 1",
    "category": "Category 1",
    "price_range": "$5.00 - $10.00"
  }
]
```

### 4. Run the Seeder

```bash
python main.py
```

## Configuration

### Adding New Data Sources

To add a new JSON file and table:

1. **Create your JSON file** in the `data/` directory
2. **Update `main.py`** to include your new data source:

```python
# In main.py, add to the data_sets list:
data_sets = [
    # existing entries...
    {
        'table_name': 'your_table_name',
        'data': load_json_file(data_dir / "your_data.json"),
        'description': 'your description'
    }
]
```

### Customizing Behavior

The `run_seeding()` function accepts several parameters:

```python
run_seeding(
    data_sets,
    verify_data=True,      # Verify data after insertion
    clear_existing=True    # Clear tables before seeding
)
```

## API Reference

### Core Functions

#### `run_seeding(data_sets, verify_data=True, clear_existing=True)`

Main seeding function that processes multiple data sets.

**Parameters:**
- `data_sets` (List[Dict]): List of data set configurations
- `verify_data` (bool): Whether to verify data after insertion
- `clear_existing` (bool): Whether to clear existing data first

**Data Set Structure:**
```python
{
    'table_name': 'categories',     # Target table name
    'data': categories_data,        # List of records to insert
    'description': 'categories'     # Description for logging
}
```

#### `load_json_file(file_path)`

Utility function to load and parse JSON files.

**Parameters:**
- `file_path` (Path): Path to the JSON file

**Returns:**
- `list`: Parsed JSON data

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `json.JSONDecodeError`: If the file contains invalid JSON

### SupabaseClient Methods

#### `insert_data(table_name, data, description=None)`

Generic method to insert data into any table.

#### `clear_tables()`

Clears existing data from predefined tables (respects foreign key constraints).

#### `verify_data()`

Verifies and reports on seeded data.

#### `test_connection()`

Tests the connection to Supabase.

## Error Handling

The application includes comprehensive error handling:

- **File Not Found**: Clear messages when JSON files are missing
- **Invalid JSON**: Detailed parsing error information
- **Database Errors**: Supabase-specific error reporting
- **Connection Issues**: Network and authentication error handling
- **Import Errors**: Missing dependency notifications

## Example Output

```
==================================================
Supabase Database Seeding Application
==================================================

Loading JSON data files...
[SUCCESS] Loaded 4 categories
[SUCCESS] Loaded 12 menu items

==================================================
Starting Database Seeding Process
==================================================

Testing Supabase connection...
[SUCCESS] Connection test successful
Clearing existing data...
[SUCCESS] Cleared menu_items table
[SUCCESS] Cleared categories table

Seeding categories...
[SUCCESS] Inserted 4 categories

Seeding menu items...
[SUCCESS] Inserted 12 menu items

==================================================
Seeding Summary: 2/2 tables seeded successfully
Total records inserted: 16
==================================================

Verifying seeded data...
[SUCCESS] Found 4 categories in database
[SUCCESS] Found 12 menu items in database

Menu items by category:
  - Pan Dulce: 4 items
  - Pasteles: 3 items
  - Tres Leches: 3 items
  - Seasonal: 2 items

[SUCCESS] Database seeding completed successfully!
```

## Requirements

- Python 3.7+
- Supabase account and project
- Required Python packages (see `requirements.txt`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the error messages - they're designed to be helpful
2. Verify your `.env` configuration
3. Ensure your JSON files are valid
4. Check that your Supabase tables exist and have the correct schema

## Changelog

### v1.0.0
- Initial release
- Modular seeding architecture
- JSON-based data loading
- Comprehensive error handling
- Data verification system
