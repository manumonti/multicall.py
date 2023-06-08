from multicall import Call
from multicall.constants import Network, MULTICALL3_ADDRESSES

CHAI = "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215"
MULTICALL3 = MULTICALL3_ADDRESSES[Network.Mainnet]


def from_wei(value):
    return value / 1e18


def test_call(w3):
    call = Call(CHAI, "name()(string)", [["name", None]], w3=w3)
    assert call() == {"name": "Chai"}


def test_call_with_args(w3):
    call = Call(CHAI, "balanceOf(address)(uint256)", [["balance", from_wei]], w3=w3)
    assert isinstance(call([CHAI])["balance"], float)


def test_call_with_predefined_args(w3):
    call = Call(
        CHAI, ["balanceOf(address)(uint256)", CHAI], [["balance", from_wei]], w3=w3
    )
    assert isinstance(call()["balance"], float)


def test_call_get_block_number(w3):
    call = Call(
        MULTICALL3, "getBlockNumber()(uint256)", [["block_number", None]], w3=w3
    )
    assert isinstance(call()["block_number"], int)


def test_call_get_eth_balance(w3):
    call = Call(
        MULTICALL3,
        ["getEthBalance(address)(uint256)", CHAI],
        [["balance", from_wei]],
        w3=w3,
    )
    assert isinstance(call()["balance"], float)
