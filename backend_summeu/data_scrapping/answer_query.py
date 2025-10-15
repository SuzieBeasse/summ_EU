import getpass
import os
from langchain import hub
import chromadb
from backend_summeu.params import PERSIST_DIR, EMBEDDINGS, MODEL, COLLECTION_NAME
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

def load_vector_store():
    client = chromadb.PersistentClient(path = str(PERSIST_DIR))
    collection = client.get_collection(COLLECTION_NAME)
    print(f"✅ Loaded collection: {COLLECTION_NAME}")
    return collection

def answer_filtered(query, vector_store, llm, prompt_template=None, session_year = 2025, session_month = None):
    """Answer a query using the vector store and the language model."""
    # Retrieve similar documents from the vector store
    embedded_query = EMBEDDINGS.embed_query(query)

    retrieved_docs = vector_store.query(
        query_embeddings=[embedded_query],
        n_results=6
    )


    # Create the prompt
    docs_content = "\n\n".join(retrieved_docs['documents'][0])

    # If no prompt template is provided, use the default one
    if not prompt_template:
        prompt_template = hub.pull("rlm/rag-prompt")

    prompt = prompt_template.invoke(
        {"context": docs_content, "question": query}
    )

    # Get the answer from the language model
    answer = llm.invoke(prompt)

    return answer.content

# Test the function
if __name__ == "__main__":
    vector_store =load_vector_store()
    query = "Summarize the discussion on water quality"
    print(answer_filtered(query, vector_store, MODEL))
