import requests
from backend_summeu.params import URL_EU_API_ALL, LOCAL_DATA_PATH
from pathlib import Path
from colorama import Fore, Style


def scrap_all_id_list():
    url = URL_EU_API_ALL
    response = requests.get(url).json()

    id_list = []

    for i in range(len(response['data'])):
        id_list.append(response['data'][i]['identifier'])
    id_list.sort(key=lambda x: x[-10:])
    id_list_one_year = id_list[-54:]

    return id_list_one_year

def pdf_download(id_list:list):
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

    print("Download is over 🚀")
    return

# Test the function
# if __name__ == "__main__":
#     # id_list = scrap_all_id_list()
#     # print(id_list)
#     # pdf_download(id_list)
