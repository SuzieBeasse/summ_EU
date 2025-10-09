# Import the necessary libraries
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain import hub
import getpass
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from backend_summeu.params import EMBEDDINGS, LOCAL_DATA_PATH

def create_vector_store():
    vector_store_c = Chroma(
        collection_name="EU_parliament",
    embedding_function=EMBEDDINGS,
    persist_directory=Path(LOCAL_DATA_PATH).joinpath("chroma_ep_follower"),
    )
    return vector_store_c

def embed_and_store_fancy(file_path, vector_store, session_date):
    """Load a PDF file, split it into chunks, and store the chunks in a vector store.
    Session_date is added to the metadata of each chunk."""


    # Load the PDF file as a single document
    loader = PyPDFLoader(file_path, mode='single')
    pdf_text = loader.load()

    # Create a text splitter instance
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2_000,  # chunk size (characters)
        chunk_overlap=400,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )

    # Split the document into smaller chunks
    all_splits = text_splitter.transform_documents(pdf_text)

    session_year = int(session_date[:4])
    session_month = int(session_date[5:7])
    session_day = int(session_date[-2:])

    # Add the session_date to the metadata
    for split in all_splits:
        split.metadata['session_day'] = session_day
        split.metadata['session_month'] = session_month
        split.metadata['session_year'] = session_year

    # Add the chunks to the vector store
    document_ids = vector_store.add_documents(documents=all_splits)

    return document_ids
