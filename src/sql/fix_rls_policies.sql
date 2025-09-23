-- Fix RLS policies to allow service key operations
-- Run this SQL in your Supabase dashboard: SQL Editor → New Query

-- Drop existing policies
DROP POLICY IF EXISTS "Allow public read access to categories" ON categories;
DROP POLICY IF EXISTS "Allow public read access to menu_items" ON menu_items;

-- Create new policies that allow service key to insert/update/delete
CREATE POLICY "Allow service key full access to categories" ON categories
    FOR ALL USING (true);

CREATE POLICY "Allow service key full access to menu_items" ON menu_items
    FOR ALL USING (true);

-- Also create policies for public read access
CREATE POLICY "Allow public read access to categories" ON categories
    FOR SELECT USING (true);

CREATE POLICY "Allow public read access to menu_items" ON menu_items
    FOR SELECT USING (true);

-- Ensure service role has proper permissions
GRANT ALL ON categories TO service_role;
GRANT ALL ON menu_items TO service_role;
GRANT USAGE, SELECT ON SEQUENCE categories_id_seq TO service_role;
