import os
from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings

##################  CONSTANTS  #####################
URL_EU_API_ALL = 'https://data.europarl.europa.eu/api/v2/plenary-session-documents?work-type=CRE_PLENARY&format=application%2Fld%2Bjson&offset=0&limit=-1'
LOCAL_DOCKER_PATH = Path("data")
LOCAL_DATA_PATH =  os.path.join(os.path.expanduser('~'), "code", "SuzieBeasse", "summ_EU", "data")

EMBEDDINGS = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
