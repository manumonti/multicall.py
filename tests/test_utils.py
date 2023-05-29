from multicall.utils import *


def test_chain_id(w3):
    assert chain_id(w3) == 1
