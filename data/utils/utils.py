import asyncio
import json
from typing import Any, Awaitable

from web3 import Web3
from web3.types import BlockIdentifier

from settings import web3_provider


def get_block_info(block_identifier: BlockIdentifier = "latest") -> (int, int):
    block = json.loads(Web3.to_json(Web3(web3_provider).eth.get_block(block_identifier)))
    return block["number"], block["timestamp"]


def await_awaitable(awaitable: Awaitable) -> Any:
    return asyncio.run(awaitable)
