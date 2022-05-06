import pytest
from dbaccess.crud import start_session,insert_contract,insert_nft

def test_start_session():
    session = db_session
    assert session != None

def test_insert_contract():
    rows_contract = []
    insert(0,[contract_address,results['contract']['name'],results['contract']['symbol'],results['contract']['type']])
    session = db_session

def test_insert_contract():
    rows_nft = []
    session = db_session

@pytest.fixture
def db_session():
    session = start_session()
    return session

    