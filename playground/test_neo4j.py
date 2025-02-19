import os
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import gpt_4o_mini_complete, openai_embed


#########
# Uncomment the below two lines if running in a jupyter notebook to handle the async nature of rag.insert()
# import nest_asyncio
# nest_asyncio.apply()
#########

ROOT_DIR = "workspace/lightrag_openai_demo"
WORKING_DIR = os.path.join(ROOT_DIR, "data")
INPUT_DIR=os.path.join(ROOT_DIR, "input")

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=gpt_4o_mini_complete,  # Use gpt_4o_mini_complete LLM model
    embedding_func=openai_embed,
    graph_storage="Neo4JStorage",
    log_level="INFO",
    # llm_model_func=gpt_4o_complete  # Optionally, use a stronger model
)

# Read all files from docs directory
texts = []
for filename in os.listdir(INPUT_DIR):
    file_path = os.path.join(INPUT_DIR, filename)
    # Only process text-based files
    if os.path.isfile(file_path) and filename.endswith(('.txt', '.md', '.csv')):
        with open(file_path, "r", encoding="utf-8") as f:
            texts.append(f.read())

# Batch insert with split by character (corrected split parameters)
# rag.insert(texts, split_by_character=["\n", "#"], split_by_character_only=True)
rag.insert(texts)

# Perform naive search
print(
    rag.query("What are the top themes in this story?", param=QueryParam(mode="naive"))
)

# Perform local search
print(
    rag.query("What are the top themes in this story?", param=QueryParam(mode="local"))
)

# Perform global search
print(
    rag.query("What are the top themes in this story?", param=QueryParam(mode="global"))
)

# Perform hybrid search
print(
    rag.query("What are the top themes in this story?", param=QueryParam(mode="hybrid"))
)
