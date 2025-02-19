import asyncio
import logging
import os
import time
from dotenv import load_dotenv

from lightrag import LightRAG, QueryParam
#from lightrag.llm.zhipu import zhipu_complete
from lightrag.llm.ollama import ollama_embedding, ollama_model_complete
from lightrag.utils import EmbeddingFunc
from lightrag.kg.postgres_impl import PostgreSQLDB

load_dotenv()
ROOT_DIR = os.environ.get("ROOT_DIR")
WORKING_DIR = f"{ROOT_DIR}/dickens-pg"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# PostgreSQL configuration
postgres_db = PostgreSQLDB(
    config={
        "host": os.environ.get("POSTGRES_HOST", "localhost"),
        "port": int(os.environ.get("POSTGRES_PORT", "15432")),
        "user": os.environ.get("POSTGRES_USER", "rag"),
        "password": os.environ.get("POSTGRES_PASSWORD", "rag"),
        "database": os.environ.get("POSTGRES_DATABASE", "rag"),
    }
)

# AGE
os.environ["AGE_GRAPH_NAME"] = "dickens"

os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "15432"
os.environ["POSTGRES_USER"] = "rag"
os.environ["POSTGRES_PASSWORD"] = "rag"
os.environ["POSTGRES_DATABASE"] = "rag"

async def init_database():
    """Initialize the database with required extensions and tables"""
    await postgres_db.initdb()
    
    # Create vector extension if it doesn't exist
    try:
        await postgres_db.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    except Exception as e:
        logging.error(f"Failed to create vector extension: {e}")
        raise
    
    # Initialize tables
    await postgres_db.check_tables()

async def create_rag():
    """Create and initialize RAG instance"""
    # Initialize PostgreSQL database
    await init_database()
    
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="mistral",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        enable_llm_cache_for_entity_extract=True,
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embedding(
                texts, embed_model="nomic-embed-text", host="http://localhost:11434"
            ),
        ),
        kv_storage="PGKVStorage",
        doc_status_storage="PGDocStatusStorage",
        graph_storage="PGGraphStorage",
        vector_storage="PGVectorStorage",
        auto_manage_storages_states=False
    )
    
    # Set the database connection for all storages
    rag.doc_status.db = postgres_db
    rag.full_docs.db = postgres_db
    rag.text_chunks.db = postgres_db
    rag.llm_response_cache.db = postgres_db
    rag.chunks_vdb.db = postgres_db
    rag.relationships_vdb.db = postgres_db
    rag.entities_vdb.db = postgres_db
    rag.chunk_entity_relation_graph.db = postgres_db
    
    # Initialize storages
    await rag.initialize_storages()
    
    # Add embedding_func for graph database
    rag.chunk_entity_relation_graph.embedding_func = rag.embedding_func
    
    return rag

async def main():
    # Create and initialize RAG
    rag = await create_rag()

    # Read and insert content
    with open(f"{ROOT_DIR}/book.txt", "r", encoding="utf-8") as f:
        await rag.ainsert(f.read())

    print("==== Trying to test the rag queries ====")
    
    # Test different query modes
    for mode in ["naive", "local", "global", "hybrid"]:
        print(f"**** Start {mode.capitalize()} Query ****")
        start_time = time.time()
        result = await rag.aquery(
            "What are the top themes in this story?", 
            param=QueryParam(mode=mode)
        )
        print(result)
        print(f"{mode.capitalize()} Query Time: {time.time() - start_time} seconds")

if __name__ == "__main__":
    asyncio.run(main())
