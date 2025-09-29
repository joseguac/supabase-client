-- Fix RLS policies for bread_locations table
-- Run this SQL in your Supabase dashboard: SQL Editor → New Query

-- Drop existing policies for bread_locations
DROP POLICY IF EXISTS "Allow public read access to approved bread_locations" ON bread_locations;
DROP POLICY IF EXISTS "Allow public insert to bread_locations" ON bread_locations;

-- Create new policies that allow anonymous users to insert and read
CREATE POLICY "Allow public read access to approved bread_locations" ON bread_locations
    FOR SELECT USING (is_approved = true);

CREATE POLICY "Allow public insert to bread_locations" ON bread_locations
    FOR INSERT WITH CHECK (true);

-- Ensure anonymous role has proper permissions
GRANT INSERT ON bread_locations TO anon;
GRANT SELECT ON bread_locations TO anon;
GRANT USAGE, SELECT ON SEQUENCE bread_locations_id_seq TO anon;

-- Also ensure authenticated users can insert
GRANT INSERT ON bread_locations TO authenticated;
GRANT SELECT ON bread_locations TO authenticated;
GRANT USAGE, SELECT ON SEQUENCE bread_locations_id_seq TO authenticated;
