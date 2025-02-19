-- Note: Run this script only after the LightRAG application has been executed at least once
-- to ensure all necessary tables and relations are created

load 'age';
SET search_path = ag_catalog, "$user", public;

-- Create indexes (these will only succeed if the tables exist)
DO $$
BEGIN
    -- Entity indexes
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'dickens' AND table_name = 'Entity') THEN
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'Entity' AND indexname = 'entity_p_idx') THEN
            CREATE INDEX CONCURRENTLY entity_p_idx ON dickens."Entity" (id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'Entity' AND indexname = 'entity_idx_node_id') THEN
            CREATE INDEX CONCURRENTLY entity_idx_node_id ON dickens."Entity" (ag_catalog.agtype_access_operator(properties, '"node_id"'::agtype));
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'Entity' AND indexname = 'entity_node_id_gin_idx') THEN
            CREATE INDEX CONCURRENTLY entity_node_id_gin_idx ON dickens."Entity" using gin(properties);
        END IF;
    END IF;

    -- Vertex indexes
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'dickens' AND table_name = '_ag_label_vertex') THEN
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = '_ag_label_vertex' AND indexname = 'vertex_p_idx') THEN
            CREATE INDEX CONCURRENTLY vertex_p_idx ON dickens."_ag_label_vertex" (id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = '_ag_label_vertex' AND indexname = 'vertex_idx_node_id') THEN
            CREATE INDEX CONCURRENTLY vertex_idx_node_id ON dickens."_ag_label_vertex" (ag_catalog.agtype_access_operator(properties, '"node_id"'::agtype));
        END IF;
    END IF;

    -- Directed edge indexes
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'dickens' AND table_name = 'DIRECTED') THEN
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'DIRECTED' AND indexname = 'directed_p_idx') THEN
            CREATE INDEX CONCURRENTLY directed_p_idx ON dickens."DIRECTED" (id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'DIRECTED' AND indexname = 'directed_eid_idx') THEN
            CREATE INDEX CONCURRENTLY directed_eid_idx ON dickens."DIRECTED" (end_id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'DIRECTED' AND indexname = 'directed_sid_idx') THEN
            CREATE INDEX CONCURRENTLY directed_sid_idx ON dickens."DIRECTED" (start_id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = 'DIRECTED' AND indexname = 'directed_seid_idx') THEN
            CREATE INDEX CONCURRENTLY directed_seid_idx ON dickens."DIRECTED" (start_id,end_id);
        END IF;
        -- Cluster the DIRECTED table
        ALTER TABLE dickens."DIRECTED" CLUSTER ON directed_sid_idx;
    END IF;

    -- Edge indexes
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'dickens' AND table_name = '_ag_label_edge') THEN
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = '_ag_label_edge' AND indexname = 'edge_p_idx') THEN
            CREATE INDEX CONCURRENTLY edge_p_idx ON dickens."_ag_label_edge" (id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = '_ag_label_edge' AND indexname = 'edge_sid_idx') THEN
            CREATE INDEX CONCURRENTLY edge_sid_idx ON dickens."_ag_label_edge" (start_id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = '_ag_label_edge' AND indexname = 'edge_eid_idx') THEN
            CREATE INDEX CONCURRENTLY edge_eid_idx ON dickens."_ag_label_edge" (end_id);
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE schemaname = 'dickens' AND tablename = '_ag_label_edge' AND indexname = 'edge_seid_idx') THEN
            CREATE INDEX CONCURRENTLY edge_seid_idx ON dickens."_ag_label_edge" (start_id,end_id);
        END IF;
    END IF;
END $$;
