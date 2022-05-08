import pytest
import datetime
from dbaccess.crud import start_session, insert_contract, insert_nft


''' Testing DB both positive and negative handling successful insert and wrong data'''

''' Test the DB can create a sesson'''


def test_start_session():
    session = start_session()
    assert session is not None


''' Test we can insert a contract and that an insert fails if the contract is defined incorrectly'''


def test_insert_contract():
    rows_contract = []
    rows_contract.insert(0, ['1', "TEST", "TST", "TST"])
    session = start_session()
    insert_contract(session, rows_contract)

    with pytest.raises(Exception) as e_info:
        rows_contract.insert(0, [1, "TEST", "TST", "TST"])
        # INDEX COLUMN IS int instead of text
        insert_contract(session, rows_contract)


''' Test we can insert a NFT and that an insert fails if the contract is defined incorrectly'''


def test_insert_nft():
    rows_nft = []
    rows_nft.insert(0, [1, '1', "TEST", "{}", "TST", "TEST",
                        "TEST", str(datetime.datetime.now()), "TEST"])
    session = start_session()
    insert_nft(session, rows_nft)
    rows_nft = []

    with pytest.raises(Exception) as e_info:
        rows_nft.insert(0, ["TED", '1', "TEST", "{}", "TST", "TEST", "TEST", str(
            datetime.datetime.now()), "TEST"])  # Index column is text instead of int
        insert_nft(session, rows_nft)
