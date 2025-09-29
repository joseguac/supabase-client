-- Create tables for Mexican bakery application
-- Run this SQL in your Supabase dashboard: SQL Editor → New Query

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    slug VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create menu_items table
CREATE TABLE IF NOT EXISTS menu_items (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price_range VARCHAR(50),
    image VARCHAR(500),
    category VARCHAR(100) NOT NULL,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_gluten_free BOOLEAN DEFAULT FALSE,
    allergens TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add some indexes for better performance
CREATE INDEX IF NOT EXISTS idx_menu_items_category ON menu_items(category);
CREATE INDEX IF NOT EXISTS idx_menu_items_vegetarian ON menu_items(is_vegetarian);
CREATE INDEX IF NOT EXISTS idx_menu_items_gluten_free ON menu_items(is_gluten_free);

-- Enable Row Level Security (optional, but recommended)
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE menu_items ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access (adjust as needed)
CREATE POLICY "Allow public read access to categories" ON categories
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to menu_items" ON menu_items
    FOR SELECT USING (true);

-- Create bread_locations table for the "Where Has Our Bread Been?" feature
CREATE TABLE IF NOT EXISTS bread_locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255) NOT NULL,
    state_province VARCHAR(255),
    country VARCHAR(255) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    customer_story TEXT,
    customer_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_approved BOOLEAN DEFAULT TRUE
);

-- Add indexes for better performance on bread_locations
CREATE INDEX IF NOT EXISTS idx_bread_locations_country ON bread_locations(country);
CREATE INDEX IF NOT EXISTS idx_bread_locations_approved ON bread_locations(is_approved);
CREATE INDEX IF NOT EXISTS idx_bread_locations_created_at ON bread_locations(created_at);

-- Enable Row Level Security for bread_locations
ALTER TABLE bread_locations ENABLE ROW LEVEL SECURITY;

-- Create policy for public read access to approved bread locations
CREATE POLICY "Allow public read access to approved bread_locations" ON bread_locations
    FOR SELECT USING (is_approved = true);

-- Create policy for public insert access (new submissions will need approval)
CREATE POLICY "Allow public insert to bread_locations" ON bread_locations
    FOR INSERT WITH CHECK (true);

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON categories TO anon, authenticated;
GRANT ALL ON menu_items TO anon, authenticated;
GRANT ALL ON bread_locations TO anon, authenticated;
GRANT USAGE, SELECT ON SEQUENCE categories_id_seq TO anon, authenticated;
GRANT USAGE, SELECT ON SEQUENCE bread_locations_id_seq TO anon, authenticated;
