from ...datamodels.models import Contract, NFT

def test_contract():
    '''
    Given the creation of a contract model
    When a contract comes from the chain
    Then check that the contractID, type, name and symbol are defined and set.
    '''

    cont = Contract()
    cont.contract_id = 'test'
    cont.contract_name = 'test2'
    cont.contract_symb = 'test3'
    cont.contract_type = 'test4'
    assert cont.contract_id == 'test'
    assert cont.contract_name == 'test2'
    assert cont.contract_symb == 'test3'
    assert cont.contract_type == 'test4'

def test_nft():
    '''
    Given the creation of a NFT model
    When a NFT comes from the contract
    Then check that the values are defined and set.
    '''

    nft = NFT()
    nft.contract_id = 'test'
    nft.chain = 'test2'
    nft.mint_date = 'test3'
    assert nft.contract_id == 'test'
    assert nft.chain == 'test2'
    assert nft.mint_date == 'test3'
