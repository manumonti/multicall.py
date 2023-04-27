import pytest
from web3 import Web3

# TODO: use .env file instead of environment variable
# environment variable: WEB3_PROVIDER_URI=https://mainnet.infura.io/v3/d5d2cxxxxxxxxx13cab
w3 = Web3()
# if not w3.is_connected():
#     w3.connect(os.environ['PYTEST_NETWORK'])

@pytest.fixture
def w3():
    return Web3()
