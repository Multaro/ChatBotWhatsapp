import requests 
from requests.structures import CaseInsensitiveDict


headers = CaseInsensitiveDict()
headers['Authorization'] = 'Bearer test_04e21f43ea74c2a6c14433986b0551'

url_champs = 'https://api.api-futebol.com.br/v1/campeonatos/'
url_live = 'https://api.api-futebol.com.br/v1/ao-vivo'
url_table = 'https://api.api-futebol.com.br/v1/campeonatos/'

def championships(key: str) -> str:
    resp = requests.get(url_champs + key, headers=headers)
    return resp.json()


def live()-> str:
    resp = requests.get(url_live, headers=headers)
    return resp.json()

def table(champsKey: str) -> str:
    resp = requests.get(url_table + champsKey + '/tabela', headers=headers)
    return resp.json()

print(live())


