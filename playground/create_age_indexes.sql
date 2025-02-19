load 'age';
SET search_path = ag_catalog, "$user", public;

-- Create schema
CREATE SCHEMA IF NOT EXISTS dickens;

-- Create indexes
CREATE INDEX CONCURRENTLY entity_p_idx ON dickens."Entity" (id);
CREATE INDEX CONCURRENTLY vertex_p_idx ON dickens."_ag_label_vertex" (id);
CREATE INDEX CONCURRENTLY directed_p_idx ON dickens."DIRECTED" (id);
CREATE INDEX CONCURRENTLY directed_eid_idx ON dickens."DIRECTED" (end_id);
CREATE INDEX CONCURRENTLY directed_sid_idx ON dickens."DIRECTED" (start_id);
CREATE INDEX CONCURRENTLY directed_seid_idx ON dickens."DIRECTED" (start_id,end_id);
CREATE INDEX CONCURRENTLY edge_p_idx ON dickens."_ag_label_edge" (id);
CREATE INDEX CONCURRENTLY edge_sid_idx ON dickens."_ag_label_edge" (start_id);
CREATE INDEX CONCURRENTLY edge_eid_idx ON dickens."_ag_label_edge" (end_id);
CREATE INDEX CONCURRENTLY edge_seid_idx ON dickens."_ag_label_edge" (start_id,end_id);
create INDEX CONCURRENTLY vertex_idx_node_id ON dickens."_ag_label_vertex" (ag_catalog.agtype_access_operator(properties, '"node_id"'::agtype));
create INDEX CONCURRENTLY entity_idx_node_id ON dickens."Entity" (ag_catalog.agtype_access_operator(properties, '"node_id"'::agtype));
CREATE INDEX CONCURRENTLY entity_node_id_gin_idx ON dickens."Entity" using gin(properties);
ALTER TABLE dickens."DIRECTED" CLUSTER ON directed_sid_idx;
