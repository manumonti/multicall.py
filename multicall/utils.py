from typing import Any, Dict

from web3 import Web3

from multicall.constants import NO_STATE_OVERRIDE

chainids: Dict[Web3, int] = {}


def chain_id(w3: Web3) -> int:
    """
    Returns chain id for an instance of Web3. Helps save repeat calls to node.
    """
    try:
        return chainids[w3]
    except KeyError:
        chainids[w3] = w3.eth.chain_id
        return chainids[w3]


def get_endpoint(w3: Web3) -> str:
    provider = w3.provider
    if isinstance(provider, str):
        return provider
    if hasattr(provider, "_active_provider"):
        provider = provider._get_active_provider(False)
    return provider.endpoint_uri


def state_override_supported(w3: Web3) -> bool:
    if chain_id(w3) in NO_STATE_OVERRIDE:
        return False
    return True
