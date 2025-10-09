import getpass
import os
from langchain import hub

if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

def answer_filtered(query, vector_store, llm, prompt_template=None, session_year = 2025, session_month = None):
    """Answer a query using the vector store and the language model."""
    # Retrieve similar documents from the vector store
    if session_month:
        filter = {"$and":[{"session_year": {"$eq": session_year}},
                  {"session_month": {"$eq": session_month}}]
                }
        retrieved_docs = vector_store.similarity_search(query, k=6, filter=filter)
    else:
        filter = {"session_year": session_year}
        retrieved_docs = vector_store.similarity_search(query, k=6, filter=filter)

    # Create the prompt
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # If no prompt template is provided, use the default one
    if not prompt_template:
        prompt_template = hub.pull("rlm/rag-prompt")

    prompt = prompt_template.invoke(
        {"context": docs_content, "question": query}
    )

    # Get the answer from the language model
    answer = llm.invoke(prompt)

    return answer.content
