"""
A simple Python script to deploy compiled contracts.
"""
import functools
import json
import logging
from logging import getLogger
from pathlib import Path
from typing import Any, Optional, Union

import click
from click import BadParameter, Context, Option, Parameter
from eth_typing.evm import ChecksumAddress, HexAddress
from eth_utils import is_address, to_checksum_address
from web3 import HTTPProvider, Web3
from web3.middleware import geth_poa_middleware

from raiden_contracts.constants import CONTRACT_CUSTOM_TOKEN, CONTRACT_TOKEN_NETWORK_REGISTRY
from raiden_contracts.deploy.contract_deployer import ContractDeployer
from raiden_contracts.deploy.contract_verifier import ContractVerifier
from raiden_contracts.utils.private_key import get_private_key
from raiden_contracts.utils.signature import private_key_to_address
from raiden_contracts.utils.versions import contract_version_with_max_token_networks

LOG = getLogger(__name__)




# pylint: disable=R0913
def setup_ctx(
    ctx: click.Context,
    private_key: Optional[str],
    rpc_provider: str,
    wait: int,
    gas_price: int,
    gas_limit: int,
    contracts_version: Optional[str] = None,
):
    """Set up deployment context according to common options (shared among all
    subcommands).
    """

    if private_key is None:
        return
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("web3").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)

    web3 = Web3(HTTPProvider(rpc_provider, request_kwargs={"timeout": 60}))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    print("Web3 provider is", web3.providers[0])
    private_key_string = get_private_key(Path(private_key))
    if not private_key_string:
        raise RuntimeError("Could not access the private key.")
    owner = private_key_to_address(private_key_string)
    # pylint: disable=E1101
    if web3.eth.getBalance(owner) == 0:
        raise RuntimeError("Account with insufficient funds.")
    deployer = ContractDeployer(
        web3=web3,
        private_key=private_key_string,
        gas_limit=gas_limit,
        gas_price=gas_price,
        wait=wait,
        contracts_version=contracts_version,
    )
    ctx.obj = {}
    ctx.obj["deployer"] = deployer
    ctx.obj["deployed_contracts"] = {}
    ctx.obj["token_type"] = "CustomToken"
    ctx.obj["wait"] = wait


@click.group(chain=True)
def main() -> int:
    pass


def check_version_dependent_parameters(
    contracts_version: Optional[str], max_token_networks: Optional[int]
) -> None:
    required = contract_version_with_max_token_networks(contracts_version)
    got = max_token_networks is not None

    # For newer conracts --max-token-networks is necessary.
    if required and not got:
        raise BadParameter(
            f"For contract_version {contracts_version},"
            " --max-token-networks option is necessary.  See --help."
        )
    # For older contracts --max_token_networks is forbidden.
    if not required and got:
        raise BadParameter(
            f"For contract_version {contracts_version},"
            " --max-token-networks option is forbidden"
            " because TokenNetworkRegistry this version is not configurable this way."
        )



def raiden(
    ctx,
    private_key,
    rpc_provider,
    wait,
    gas_price,
    gas_limit,
    save_info,
    contracts_version,
    max_token_networks: Optional[int],
):
    check_version_dependent_parameters(contracts_version, max_token_networks)

    setup_ctx(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, contracts_version)
    deployer = ctx.obj["deployer"]
    deployed_contracts_info = deployer.deploy_raiden_contracts(
        max_num_of_token_networks=max_token_networks
    )
    deployed_contracts = {
        contract_name: info["address"]
        for contract_name, info in deployed_contracts_info["contracts"].items()
    }

    if save_info:
        deployer.store_and_verify_deployment_info_raiden(
            deployed_contracts_info=deployed_contracts_info
        )
    else:
        deployer.verify_deployment_data(deployed_contracts_info=deployed_contracts_info)

    print(json.dumps(deployed_contracts, indent=4))
    ctx.obj["deployed_contracts"].update(deployed_contracts)


def services(
    ctx: Context,
    private_key: Optional[str],
    rpc_provider: str,
    wait: int,
    gas_price: int,
    gas_limit: int,
    token_address: HexAddress,
    save_info: bool,
    contracts_version: Optional[str],
    user_deposit_whole_limit: int,
):
    setup_ctx(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, contracts_version)
    deployer: ContractDeployer = ctx.obj["deployer"]

    deployed_contracts_info = deployer.deploy_service_contracts(
        token_address=token_address, user_deposit_whole_balance_limit=user_deposit_whole_limit
    )
    deployed_contracts = {
        contract_name: info["address"]
        for contract_name, info in deployed_contracts_info["contracts"].items()
    }

    if save_info:
        deployer.store_and_verify_deployment_info_services(
            deployed_contracts_info=deployed_contracts_info,
            token_address=token_address,
            user_deposit_whole_balance_limit=user_deposit_whole_limit,
        )
    else:
        deployer.verify_service_contracts_deployment_data(
            deployed_contracts_info=deployed_contracts_info,
            token_address=token_address,
            user_deposit_whole_balance_limit=user_deposit_whole_limit,
        )

    print(json.dumps(deployed_contracts, indent=4))
    ctx.obj["deployed_contracts"].update(deployed_contracts)



def token(
    ctx,
    private_key,
    rpc_provider,
    wait,
    gas_price,
    gas_limit,
    contracts_version,
    token_supply,
    token_name,
    token_decimals,
    token_symbol,
):
    setup_ctx(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, contracts_version)
    deployer = ctx.obj["deployer"]
    token_supply *= 10 ** token_decimals
    deployed_token = deployer.deploy_token_contract(
        token_supply, token_decimals, token_name, token_symbol, token_type=ctx.obj["token_type"]
    )
    print(json.dumps(deployed_token, indent=4))
    ctx.obj["deployed_contracts"].update(deployed_token)



def register(
    ctx: Context,
    private_key: str,
    rpc_provider: str,
    wait: int,
    gas_price: int,
    gas_limit: int,
    contracts_version: str,
    token_address: HexAddress,
    token_network_registry_address: HexAddress,
    channel_participant_deposit_limit: Optional[int],
    token_network_deposit_limit: Optional[int],
    registry_address: Optional[HexAddress],
) -> None:
    assert registry_address is None  # No longer used option
    setup_ctx(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, contracts_version)
    token_type = ctx.obj["token_type"]
    deployer = ctx.obj["deployer"]

    if token_address:
        ctx.obj["deployed_contracts"][token_type] = token_address
    if token_network_registry_address:
        ctx.obj["deployed_contracts"][
            CONTRACT_TOKEN_NETWORK_REGISTRY
        ] = token_network_registry_address

    if CONTRACT_TOKEN_NETWORK_REGISTRY not in ctx.obj["deployed_contracts"]:
        raise RuntimeError(
            "No TokenNetworkRegistry was specified. "
            "Add --token-network-registry-address <address>."
        )
    assert token_type in ctx.obj["deployed_contracts"]
    abi = deployer.contract_manager.get_contract_abi(CONTRACT_TOKEN_NETWORK_REGISTRY)
    deployer.register_token_network(
        token_registry_abi=abi,
        token_registry_address=ctx.obj["deployed_contracts"][CONTRACT_TOKEN_NETWORK_REGISTRY],
        token_address=ctx.obj["deployed_contracts"][token_type],
        channel_participant_deposit_limit=channel_participant_deposit_limit,
        token_network_deposit_limit=token_network_deposit_limit,
    )



def verify(_: Any, rpc_provider: str, contracts_version: Optional[str]) -> None:
    web3 = Web3(HTTPProvider(rpc_provider, request_kwargs={"timeout": 60}))
    web3.middleware_stack.inject(geth_poa_middleware, layer=0)
    print("Web3 provider is", web3.providers[0])

    verifier = ContractVerifier(web3=web3, contracts_version=contracts_version)
    verifier.verify_deployed_contracts_in_filesystem()


if __name__ == "__main__":
    main()
