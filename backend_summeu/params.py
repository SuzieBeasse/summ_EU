import os
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model

##################  CONSTANTS  #####################
URL_EU_API_ALL = 'https://data.europarl.europa.eu/api/v2/plenary-session-documents?work-type=CRE_PLENARY&format=application%2Fld%2Bjson&offset=0&limit=-1'
LOCAL_DOCKER_PATH = os.path.join('backend_summeu', "data")
LOCAL_DATA_PATH =  os.path.join(os.path.expanduser('~'), "code", "SuzieBeasse", "summ_EU","backend_summeu", "data")
PERSIST_DIR = Path(LOCAL_DOCKER_PATH).joinpath("chroma_ep_follower")
COLLECTION_NAME = "EU_parliament"
EMBEDDINGS = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
MODEL = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
