-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS age;

-- Set up AGE schema
SET search_path = ag_catalog, "$user", public;
CREATE SCHEMA IF NOT EXISTS dickens;
