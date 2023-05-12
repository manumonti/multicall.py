import pytest
from web3 import Web3

@pytest.fixture(scope="session")
def w3():
    return Web3()
