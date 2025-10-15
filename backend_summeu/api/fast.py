from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from backend_summeu.params import LOCAL_DATA_PATH, PERSIST_DIR, EMBEDDINGS, MODEL
from langchain.chat_models import init_chat_model
from langchain import hub
import chromadb

from backend_summeu.data_scrapping.fetch_cre import scrap_all_id_list, pdf_download
from backend_summeu.data_scrapping.embedding import create_vector_store, embed_and_store_fancy
from backend_summeu.data_scrapping.answer_query import load_vector_store, answer_filtered
app = FastAPI()

# State parameters
app.state.vector_store = load_vector_store()



# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def root():
    return {'greeting': 'Hellu'}


def fetch_and_embed_CRE():

    # Get the list of CRE id for the last year
    id_list = scrap_all_id_list()

    # Download the matching PDF files and store them locally
    pdf_download(id_list)


    # Embed the downloaded PDF into the vector store:
    for i, id in enumerate(id_list):
        data_path = Path(LOCAL_DATA_PATH).joinpath(f'EP/{id}_EN.pdf')
        session_date = id[-10:]
        embed_and_store_fancy(data_path, app.state.vector_store, session_date)

@app.get('/query_vs')
def query_vector_store(query: str):
    """Answer a query using the vector store and the language model."""
   # Retrieve similar documents from the vector store
    embedded_query = EMBEDDINGS.embed_query(query)

    retrieved_docs = app.state.vector_store.query(
        query_embeddings=[embedded_query],
        n_results=6
    )

    # Create the prompt
    docs_content = "\n\n".join(retrieved_docs['documents'][0])

    # If no prompt template is provided, use the default one
    prompt_template = hub.pull("rlm/rag-prompt")

    prompt = prompt_template.invoke(
        {"context": docs_content, "question": query}
    )

    # Get the answer from the language model
    answer = MODEL.invoke(prompt)
    if answer.content:
        return {"answer": answer.content}
    else:
        return {"error": "Something went wrong"}
