import asyncio
import logging
import os
import time
from dotenv import load_dotenv

from lightrag import LightRAG, QueryParam
from lightrag.kg.postgres_impl import PostgreSQLDB
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed

ROOT_DIR = "workspace/lightrag_openai_demo"
WORKING_DIR = os.path.join(ROOT_DIR, "data")
INPUT_DIR=os.path.join(ROOT_DIR, "input")

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# AGE
# os.environ["AGE_GRAPH_NAME"] = "dickens"

postgres_db = PostgreSQLDB(
    config={
        "host": "localhost",
        "port": 55432,
        "user": "rag",
        "password": "rag",
        "database": "rag",
    }
)


async def main():
    await postgres_db.initdb()
    # Check if PostgreSQL DB tables exist, if not, tables will be created
    await postgres_db.check_tables()

    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=gpt_4o_mini_complete,
        embedding_func=openai_embed,
        kv_storage="PGKVStorage",
        doc_status_storage="PGDocStatusStorage",
        graph_storage="PGGraphStorage",
        vector_storage="PGVectorStorage",
    )
    # Set the KV/vector/graph storage's `db` property, so all operation will use same connection pool
    rag.doc_status.db = postgres_db
    rag.full_docs.db = postgres_db
    rag.text_chunks.db = postgres_db
    rag.llm_response_cache.db = postgres_db
    rag.key_string_value_json_storage_cls.db = postgres_db
    rag.chunks_vdb.db = postgres_db
    rag.relationships_vdb.db = postgres_db
    rag.entities_vdb.db = postgres_db
    rag.graph_storage_cls.db = postgres_db
    rag.chunk_entity_relation_graph.db = postgres_db
    # add embedding_func for graph database, it's deleted in commit 5661d76860436f7bf5aef2e50d9ee4a59660146c
    rag.chunk_entity_relation_graph.embedding_func = rag.embedding_func

    # with open(f"{INPUT_DIR}/book.txt", "r", encoding="utf-8") as f:
    #     await rag.ainsert(f.read())

    # Read all files from docs directory
    texts = []
    for filename in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                texts.append(f.read())
                
    await rag.ainsert(texts)

    print("==== Trying to test the rag queries ====")
    print("**** Start Naive Query ****")
    start_time = time.time()
    # Perform naive search
    print(
        await rag.aquery(
            "What are the top themes in this story?", param=QueryParam(mode="naive")
        )
    )
    print(f"Naive Query Time: {time.time() - start_time} seconds")
    # Perform local search
    print("**** Start Local Query ****")
    start_time = time.time()
    print(
        await rag.aquery(
            "What are the top themes in this story?", param=QueryParam(mode="local")
        )
    )
    print(f"Local Query Time: {time.time() - start_time} seconds")
    # Perform global search
    print("**** Start Global Query ****")
    start_time = time.time()
    print(
        await rag.aquery(
            "What are the top themes in this story?", param=QueryParam(mode="global")
        )
    )
    print(f"Global Query Time: {time.time() - start_time}")
    # Perform hybrid search
    print("**** Start Hybrid Query ****")
    print(
        await rag.aquery(
            "What are the top themes in this story?", param=QueryParam(mode="hybrid")
        )
    )
    print(f"Hybrid Query Time: {time.time() - start_time} seconds")


if __name__ == "__main__":
    asyncio.run(main())
