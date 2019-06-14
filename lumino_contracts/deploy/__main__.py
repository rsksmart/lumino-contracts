import functools
import click
from logging import getLogger
from typing import Optional

from eth_utils import is_address, to_checksum_address
from raiden_contracts.constants import (
    CONTRACT_CUSTOM_TOKEN,
)


log = getLogger(__name__)


@click.group(chain=True)
def main():
    pass


def validate_address(ctx, param, value):
    if not value:
        return None
    try:
        is_address(value)
        return to_checksum_address(value)
    except ValueError:
        raise click.BadParameter('must be a valid ethereum address')

def error_removed_option(message: str):
    """ Takes a message and returns a callback that raises NoSuchOption

    if the value is not None. The message is used as an argument to NoSuchOption. """

    def f(_, param, value):
        if value is not None:
            raise click.NoSuchOption(
                f'--{param.name.replace("_", "-")} is no longer a valid option. ' + message
            )

    return f



def common_options(func):
    """A decorator that combines commonly appearing @click.option decorators."""

    @click.option("--private-key", required=True, help="Path to a private key store.")
    @click.option(
        "--rpc-provider",
        default="http://127.0.0.1:8545",
        help="Address of the Ethereum RPC provider",
    )
    @click.option("--wait", default=300, help="Max tx wait time in s.")
    @click.option("--gas-price", default=5, type=int, help="Gas price to use in gwei")
    @click.option("--gas-limit", default=5_500_000)
    @click.option(
        "--contracts-version",
        default=None,
        help="Contracts version to verify. Current version will be used by default.",
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper





@main.command()
@common_options
@click.option("--save-info/--no-save-info", default=True, help="Save deployment info to a file.")
@click.option(
    "--max-token-networks", help="The maximum number of tokens that can be registered.", type=int
)
@click.pass_context
def lumino(
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
   from raiden_contracts.deploy.__main__ import raiden
   raiden(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, save_info, contracts_version, max_token_networks)




@main.command()
@common_options
@click.option(
    "--token-supply",
    default=10000000,
    help="Token contract supply (number of total issued tokens).",
)
@click.option("--token-name", default=CONTRACT_CUSTOM_TOKEN, help="Token contract name.")
@click.option("--token-decimals", default=18, help="Token contract number of decimals.")
@click.option("--token-symbol", default="TKN", help="Token contract symbol.")
@click.pass_context
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
   from raiden_contracts.deploy.__main__ import token
   token(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, contracts_version, token_supply, token_name, token_decimals, token_symbol)

@main.command()
@common_options
@click.option(
    "--token-address",
    default=None,
    callback=validate_address,
    help="Already deployed token address.",
)
@click.option(
    "--registry-address",
    default=None,
    callback=error_removed_option("Use --token-network-registry-address"),
    hidden=True,
    help="Renamed into --token-network-registry-address",
)
@click.option(
    "--token-network-registry-address",
    default=None,
    callback=validate_address,
    help="Address of token network registry",
)
@click.option(
    "--channel-participant-deposit-limit",
    default=None,
    type=int,
    help="Address of token network registry",
)
@click.option(
    "--token-network-deposit-limit",
    default=None,
    type=int,
    help="Address of token network registry",
)
@click.pass_context
def register(
    ctx,
    private_key,
    rpc_provider,
    wait,
    gas_price,
    gas_limit,
    contracts_version,
    token_address,
    token_network_registry_address,
    channel_participant_deposit_limit,
    token_network_deposit_limit,
    registry_address,
):
   from raiden_contracts.deploy.__main__ import register
   register(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, contracts_version, token_address,
            token_network_registry_address, channel_participant_deposit_limit, token_network_deposit_limit, registry_address)


@main.command()
@common_options
@click.option(
    "--token-address",
    default=None,
    callback=validate_address,
    help="Address of token used to pay for the services (MS, PFS).",
)
@click.option(
    "--user-deposit-whole-limit",
    required=True,
    type=int,
    help="Maximum amount of tokens deposited in UserDeposit",
)
@click.option("--save-info/--no-save-info", default=True, help="Save deployment info to a file.")
@click.pass_context
@click.pass_context
def services(
    ctx,
    private_key,
    rpc_provider,
    wait,
    gas_price,
    gas_limit,
    token_address,
    save_info,
    contracts_version,
    user_deposit_whole_limit: int

):
   from raiden_contracts.deploy.__main__ import services
   services(ctx, private_key, rpc_provider, wait, gas_price, gas_limit, token_address, save_info, contracts_version,
            user_deposit_whole_limit)

@main.command()
@click.option(
    "--rpc-provider", default="http://127.0.0.1:8545", help="Address of the Ethereum RPC provider"
)
@click.option(
    "--contracts-version",
    help="Contracts version to verify. Current version will be used by default.",
)
@click.pass_context
def verify(ctx, rpc_provider, contracts_version):
   from raiden_contracts.deploy.__main__ import verify
   verify(ctx, rpc_provider, contracts_version)


if __name__ == '__main__':
    main()
