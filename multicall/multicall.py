from time import time
from typing import Any, Dict, List, Optional, Tuple, Union

from web3 import Web3

from multicall import Call
from multicall.constants import (
    GAS_LIMIT,
    MULTICALL2_ADDRESSES,
    MULTICALL3_BYTECODE,
    MULTICALL3_ADDRESSES,
)
from multicall.loggers import setup_logger
from multicall.utils import chain_id, state_override_supported

logger = setup_logger(__name__)

CallResponse = Tuple[Union[None, bool], bytes]


def get_args(
    calls: List[Call], require_success: bool = True
) -> List[Union[bool, List[List[Any]]]]:
    if require_success is True:
        return [[[call.target, call.data] for call in calls]]
    return [require_success, [[call.target, call.data] for call in calls]]


def unpack_aggregate_outputs(outputs: Any) -> Tuple[CallResponse, ...]:
    return tuple((None, output) for output in outputs)


def unpack_batch_results(batch_results: List[List[CallResponse]]) -> List[CallResponse]:
    return [result for batch in batch_results for result in batch]


class Multicall:
    def __init__(
        self,
        _w3: Web3,
        calls: List[Call],
        block_id: Optional[int] = None,
        require_success: bool = True,
        gas_limit: int = GAS_LIMIT,
    ) -> None:
        self.w3 = _w3
        self.calls = calls
        self.block_id = block_id
        self.require_success = require_success
        self.gas_limit = gas_limit
        self.chainid = chain_id(self.w3)
        if require_success is True:
            multicall_map = (
                MULTICALL3_ADDRESSES
                if self.chainid in MULTICALL3_ADDRESSES
                else MULTICALL2_ADDRESSES
            )
            self.multicall_sig = "aggregate((address,bytes)[])(uint256,bytes[])"
        else:
            multicall_map = (
                MULTICALL3_ADDRESSES
                if self.chainid in MULTICALL3_ADDRESSES
                else MULTICALL2_ADDRESSES
            )
            self.multicall_sig = "tryBlockAndAggregate(bool,(address,bytes)[])(uint256,uint256,(bool,bytes)[])"
        self.multicall_address = multicall_map[self.chainid]

    def __call__(self) -> Dict[str, Any]:
        start = time()

        outputs = self.fetch_outputs(self.calls)
        response = {
            name: result for output in outputs for name, result in output.items()
        }

        logger.debug(f"Multicall took {time() - start}s")
        return response

    def fetch_outputs(self, calls: List[Call]) -> List[CallResponse]:
        if calls is None:
            calls = self.calls

        try:
            args = get_args(calls, self.require_success)
            if self.require_success is True:
                _, outputs = self.aggregate(args)
                outputs = unpack_aggregate_outputs(outputs)
            else:
                _, _, outputs = self.aggregate(args)
            outputs = [
                Call.decode_output(output, call.signature, call.returns, success)
                for call, (success, output) in zip(calls, outputs)
            ]
            return outputs
        except Exception as e:
            logger.error(e)

    @property
    def aggregate(self) -> Call:
        if state_override_supported(self.w3):
            return Call(
                self.multicall_address,
                self.multicall_sig,
                returns=None,
                _w3=self.w3,
                block_id=self.block_id,
                gas_limit=self.gas_limit,
                state_override_code=MULTICALL3_BYTECODE,
            )

        # If state override is not supported, we simply skip it.
        # This will mean you're unable to access full historical data on chains without state override support.
        return Call(
            self.multicall_address,
            self.multicall_sig,
            returns=None,
            _w3=self.w3,
            block_id=self.block_id,
            gas_limit=self.gas_limit,
        )
