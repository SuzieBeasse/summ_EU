import requests
from backend_summeu.params import URL_EU_API, LOCAL_DATA_PATH
from pathlib import Path
from colorama import Fore, Style


def scrap_id_list(limit=25, offset=40):
    url = URL_EU_API
    params = {
        'work-type': 'CRE_PLENARY',
        'limit': limit,
        'offset': offset,
        'format':"application/ld+json"
    }
    response = requests.get(url, params=params).json()

    id_list = []

    for i in range(len(response['data'])):
        id_list.append(response['data'][i]['identifier'])

    return id_list

def pdf_download(id_list:list, data_path):
    for i, id in enumerate(id_list):
        url_ep = f'https://www.europarl.europa.eu/doceo/document/{id+"_EN"}.pdf'
        resp = requests.get(url_ep)
        data_path = Path(LOCAL_DATA_PATH).joinpath(f'EP/{id}_EN.pdf')
        with open(data_path, 'wb') as f:
            f.write(resp.content)
        if data_path.is_file():
            print(Fore.BLUE + f"\nSuccesfully downloaded CRE nr {i} / {len(id_list)}..." + Style.RESET_ALL)
        else:
            print(f"❌ Problem downloading file {i}/{len(id_list)} from session {id}")
