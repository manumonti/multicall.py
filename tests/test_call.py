from joblib import Parallel, delayed
from multicall import Call
from multicall.utils import await_awaitable

CHAI = '0x06AF07097C9Eeb7fD685c692751D5C66dB49c215'


def from_wei(value):
    return value / 1e18


def test_call(w3):
    call = Call(CHAI, 'name()(string)', [['name', None]], _w3=w3)
    assert call() == {'name': 'Chai'}


def test_call_with_args(w3):
    call = Call(CHAI, 'balanceOf(address)(uint256)', [['balance', from_wei]], _w3=w3)
    assert isinstance(call([CHAI])['balance'], float)


def test_call_with_predefined_args(w3):
    call = Call(CHAI, ['balanceOf(address)(uint256)', CHAI], [['balance', from_wei]], _w3=w3)
    assert isinstance(call()['balance'], float)


def test_call_async(w3):
    call = Call(CHAI, 'name()(string)', [['name', None]], _w3=w3)
    assert await_awaitable(call.coroutine()) == {'name': 'Chai'}


def test_call_with_args_async(w3):
    call = Call(CHAI, 'balanceOf(address)(uint256)', [['balance', from_wei]], _w3=w3)
    assert isinstance(await_awaitable(call.coroutine([CHAI]))['balance'], float)


def test_call_with_predefined_args_async(w3):
    call = Call(CHAI, ['balanceOf(address)(uint256)', CHAI], [['balance', from_wei]], _w3=w3)
    assert isinstance(await_awaitable(call.coroutine())['balance'], float)


def test_call_threading(w3):
    Parallel(4,'threading')(delayed(Call(CHAI, 'name()(string)', [['name', None]], _w3=w3))() for i in range(10))
