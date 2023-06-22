import logging

from eth_abi.exceptions import DecodingError
from eth_typing import ChecksumAddress
from web3 import Web3
from web3._utils.abi import get_abi_output_types, map_abi_data
from web3._utils.normalizers import BASE_RETURN_NORMALIZERS
from web3.contract.contract import ContractFunction
from web3.exceptions import ContractLogicError
from web3.types import BlockIdentifier

from data.utils.multicall_abi import abi
from settings import web3_provider

logger = logging.getLogger()


class MaxRetriesExceeded(Exception):
    pass


class Multicall:
    def __init__(self, address: str, provider: Web3.HTTPProvider, batch: int = 100, max_retries: int = 3):
        self.web3 = Web3(provider)
        self.max_retries = max_retries
        self.batch = batch
        self.contract = self.web3.eth.contract(address=address, abi=abi)

    @staticmethod
    def _encode_data(calls: list[ContractFunction]):
        return [(call.address, call._encode_transaction_data()) for call in calls]

    @staticmethod
    def _encode_data_with_address(calls: list[ContractFunction], addresses: list[ChecksumAddress]):
        return [(address, call._encode_transaction_data()) for address, call in zip(addresses, calls)]

    @staticmethod
    def _get_return_types(calls: list[ContractFunction]):
        return [get_abi_output_types(call.abi) for call in calls]

    def _decode(self, return_data, return_type):
        try:
            decoded_data = self.web3.codec.decode(return_type, return_data)
            normalized_data = map_abi_data(BASE_RETURN_NORMALIZERS, return_type, decoded_data)
            if len(normalized_data) == 1:
                return normalized_data[0]
            else:
                return normalized_data
        except DecodingError as e:
            logger.error(f"Failed to decode {return_data} as {return_type}: {e}")
        return None

    def _parse_aggregate(self, calldata, return_types, block_identifier):
        output_data = []
        _, results = self.contract.functions.aggregate(calldata).call(block_identifier=block_identifier)
        for result, return_type in zip(results, return_types):
            output_data.append(self._decode(result, return_type))
        return output_data

    def _parse_try_aggregate(self, calldata, return_types, block_identifier):
        output_data = []
        returned_data = self.contract.functions.tryAggregate(False, calldata).call(block_identifier=block_identifier)
        successes, results = list(map(list, zip(*returned_data)))
        for success, result, return_type in zip(successes, results, return_types):
            if not success:
                output_data.append(None)
            else:
                output_data.append(self._decode(result, return_type))
        return output_data

    def _aggregate(
        self,
        call_list: list[ContractFunction],
        use_try: bool,
        block_identifier: BlockIdentifier,
        target_address_list: list[ChecksumAddress] | None = None,
    ):
        output_data = []
        batch = self.batch
        retries = 0
        while True:
            if retries > self.max_retries:
                raise MaxRetriesExceeded(f"Failed to call multicall after {retries} attempts.")
            try:
                for i in range(0, len(call_list), batch):
                    addresses = target_address_list[i : i + batch] if target_address_list else None
                    calls = call_list[i : i + batch]
                    calldata = (
                        self._encode_data_with_address(calls, addresses) if addresses else self._encode_data(calls)
                    )
                    return_types = self._get_return_types(calls)
                    if use_try:
                        output_data += self._parse_try_aggregate(calldata, return_types, block_identifier)
                    else:
                        output_data += self._parse_aggregate(calldata, return_types, block_identifier)
                return output_data
            except OverflowError as e:
                logger.error(f"Overflow error calling with {batch}-size batch, reducing by half: {e}")
                batch //= 2
                retries += 1
            except (ContractLogicError, ValueError) as e:
                logger.error(f"Error calling multicall, retrying: {e}")
                retries += 1

    def try_aggregate(self, calls: list[ContractFunction], block_identifier: BlockIdentifier = "latest"):
        """
        Calls tryAggregate on multicall v2, assuming that all
        functions in calls are calling the contract with which the
        ContractFunction were instantiated, and accepting reverts
        """
        return self._aggregate(calls, use_try=True, block_identifier=block_identifier)

    def aggregate(self, calls: list[ContractFunction], block_identifier: BlockIdentifier = "latest"):
        """
        Calls aggregate on multicall, assuming that all the
        functions in calls are calling the contract with which the
        ContractFunction were instantiated
        """
        return self._aggregate(calls, use_try=False, block_identifier=block_identifier)

    def aggregate_with_addresses(
        self,
        addresses: list[ChecksumAddress],
        calls: list[ContractFunction],
        block_identifier: BlockIdentifier = "latest",
    ):
        """
        Calls aggregate on multicall but lets user specify a list of
        target addresses corresponding to each ContractFunction. This
        is useful to optimize in cases where we might only want to load
        a few abis with function signatures but call the same functions
        on different contracts using the same ABI.
        (ContractFunction is heavy to instantiate)
        """
        return self._aggregate(calls, use_try=False, target_address_list=addresses, block_identifier=block_identifier)

    def try_aggregate_with_addresses(
        self,
        addresses: list[ChecksumAddress],
        calls: list[ContractFunction],
        block_identifier: BlockIdentifier = "latest",
    ):
        """
        Calls tryAggregate on multicall v2 but lets user specify a list of
        target addresses corresponding to each ContractFunction. This
        is useful to optimize in cases where we might only want to load
        a few abis with function signatures but call the same functions
        on different contracts using the same ABI.
        (ContractFunction is heavy to instantiate)
        """
        return self._aggregate(calls, use_try=True, target_address_list=addresses, block_identifier=block_identifier)


# this is the multicall v2 address which was deployed in Q2 2021
multicall = Multicall(address="0x5BA1e12693Dc8F9c48aAD8770482f4739bEeD696", provider=web3_provider, max_retries=0)
