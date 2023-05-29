from typing import Any, Tuple

from multicall import Call, Multicall

CHAI = "0x06AF07097C9Eeb7fD685c692751D5C66dB49c215"
DUMMY_CALL = Call(CHAI, "totalSupply()(uint)", [["totalSupply", None]])


def from_wei(val):
    return val / 1e18


def from_ray(val):
    return val / 1e18


def unpack_no_success(success: bool, output: Any) -> Tuple[bool, Any]:
    return (success, output)


def test_multicall(w3):
    multi = Multicall(
        w3,
        [
            Call(CHAI, "totalSupply()(uint256)", [["supply", from_wei]]),
            Call(CHAI, ["balanceOf(address)(uint256)", CHAI], [["balance", from_ray]]),
        ],
    )
    result = multi()
    print(result)
    assert isinstance(result["supply"], float)
    assert isinstance(result["balance"], float)


def test_multicall_no_success(w3):
    multi = Multicall(
        w3,
        [
            Call(
                CHAI,
                "transfer(address,uint256)(bool)",
                [["success", unpack_no_success]],
            ),  # lambda success, ret_flag: (success, ret_flag)
            Call(
                CHAI,
                ["balanceOf(address)(uint256)", CHAI],
                [["balance", unpack_no_success]],
            ),  # lambda success, value: (success, from_ray(value))
        ],
        require_success=False,
    )
    result = multi()
    print(result)
    assert isinstance(result["success"], tuple)
    assert isinstance(result["balance"], tuple)
