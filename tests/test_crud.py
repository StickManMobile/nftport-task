from dbaccess.crud import start_session

def test_start_session():
    session = start_session()
    assert session != None