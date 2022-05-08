''' Retrieve NFT data from NFTPort for given contract address'''
import json
import requests

API_KEY = 'c479da49-74f7-4fcc-86f0-51ff9af3f477'
NFT_PORT_API_URL = 'https://api.nftport.xyz/v0/nfts/{contract_address}?chain=ethereum&page_size=50&page_number={page_number}&include=all'
AUTH_HEADER = {"Authorization": API_KEY}


def get_contract_nft_by_page(
        contract_address: str,
        page_number: int = 1) -> dict:
    url = NFT_PORT_API_URL.format(
        contract_address=contract_address, page_number=page_number)
    response = requests.get(url, headers=AUTH_HEADER)
    return response.json()


def get_contract_nfts(contract_address: str):
    page_number = 1
    nfts = []
    while True:
        # The first API call will have the page number set to 1
        results = get_contract_nft_by_page(contract_address, page_number)
        if results["response"] != 'OK':
            # print validation error
            break
        # When we are done going through all pages
        if (len(results["nfts"]) == 0 or page_number > 5):
            # We got to end of page
            break
        nfts += results['nfts']
        # Continue
        page_number += 1
    return nfts


contract_nfts = get_contract_nfts('0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d')
print(json.dumps(contract_nfts))
