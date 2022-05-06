''' This is the entry from download of contracts and associated NFTS from the collections.json file'''
import json
import assetdownload
from math import fabs
import requests
import config as cfg
import dbaccess.crud as crud
from datamodels.models import Contract
from ratelimiter import RateLimiter
from concurrent.futures import ThreadPoolExecutor, as_completed


NFT_PORT_API_URL = 'https://api.nftport.xyz/v0/nfts/{contract_address}?chain=ethereum&page_size=50&page_number={page_number}&include=all'
AUTH_HEADER = {"Authorization": cfg.API_KEY}

@RateLimiter(max_calls=3, period=1)
def get_contract_nft_by_page(contract_address: str, page_number: int = 1) -> dict:
    url = NFT_PORT_API_URL.format(
        contract_address=contract_address, page_number=page_number)
    response = requests.get(url, headers=AUTH_HEADER)
    return response.json()


async def limited(until):
    duration = int(round(until - time.time()))
    print('Rate limited, sleeping for {:d} seconds'.format(duration))

def get_contract_nfts_and_ins(contract_address: str):
    
    print(contract_address)
    page_number = 1
    nfts = []
    
    session = crud.start_session()

    while True:
        try:
            results = get_contract_nft_by_page(contract_address, page_number)
            if results["response"] != 'OK':
                # print validation error
                break
            # When we are done going through all pages
            if (len(results["nfts"]) == 0):
                # We got to end of page
                break
            nfts += results['nfts']
        
            if page_number == 1:
                rows = []
                rows.insert(0,[contract_address,results['contract']['name'],results['contract']['symbol'],results['contract']['type']])
                crud.insert_contract(session,rows)
                # Continue
            page_number += 1
        except BaseException  as err:
            print(f"Unexpected {err=}, {type(err)=}")
    return nfts

def main():
    f = open("collections.json")
    data = json.load(f)

    for contract_id in data:
        results = get_contract_nfts_and_ins(contract_id)

    
        rows = [];
        for nft in results: 
            rows.insert(0,[nft['token_id'],nft['contract_address'],nft['chain'],nft['metadata'],nft['metadata_url'],nft['file_url'],nft['cached_file_url'],nft['mint_date'],nft['file_information'],nft['updated_date']])
            assetdownload.add_url(nft['cached_file_url'])
    
        assetdownload.runner()
        session = crud.start_session()
        crud.insert_nft(session,rows)
    print("Import complete")

if __name__ == "__main__":
    main()