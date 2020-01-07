# RIF Lumino Contracts
![Lumino Network](Lumino.png?raw=true "RIF Lumino Network")

## Overview

Lumino has a set of Smart Contracts, that must be deployed into the RSK network, that are in charge of handling all the on-chain operations.


## Pre requisites

1. RSK account with RBTC balance
2. Python 3.7
3. Pip
4. Virtualenv



## Build RIF Lumino contract 

1. Git clone
2. Go to the path you downloaded or cloned Lumino's code (lets call this path `$RIF_LUMINO_CONTRACTS_PATH`)
3. Create python virtual env for RIF Lumino (this has to be made one time)

```virtualenv -p <PATH_TO_PYTHON3.7> contractsVenv```

**Note 1:**
Replace `<PATH_TO_PYTHON3.7>` for the path where Python3.7 is installed in your system, in the case of Ubuntu this usually is on path `/usr/bin/python3.7`

**Note 2:**
If you receive an error please check ***Additional Help*** section.

4. Activate python virtual env

```$ source contractsVenv/bin/activate```

5. Check Python version is correct inside the virtual environment

Run:

```$ python --version```

This command should output version 3.7.x

6. Install RIF Lumino contracts requirements

Inside the virtual environment run the following command to install the Lumino deployment scripts dependencies:

```$ pip install -r requirements-dev.txt```


## Creating a Lumino custom network

Lumino network is defined by a set of Smart Contracts deployed into RSK. This is a step by step guide for those who wants to create a private custom Lumino network. The guide is based on a regtest node or local cluster of RegTest nodes, but the same steps applies for MainNet or TestNet.

#### Deploy the set of Lumino contracts into RSK

As a first step, define the following variables, they will be used at the Lumino Scripts. The following are examples

```
export PRIV_KEY=./keystores/UTC--2019-05-15T17-24-00.312006960Z--3278deed4ee3de26bb53ffb82f4be82a6bb66d19
export VERSION="0.12.0"
export MAX_TOKENS=10
export PROVIDER="http://127.0.0.1:4444"

```
To deploy the TokenNetworkRegistry, SecretRegistry and EndpointRegistry, we encourage you to use the `lumino_contracts.deploy lumino` script specifying:

-   `--private-key`: Path to the RSK account private key, typically a keystore file.
-   `--gas-price`: RBTC gas price of the onchain operations.
-   `--rpc-provider`: RSK node endpoint.
-   `--contracts-version`: Lumino smart contracts version (current version is 0.12.0).
-   `--max-token-networks`: Maximum quantity of tokens registered into the Lumino network.

```
python -m lumino_contracts.deploy lumino --rpc-provider $PROVIDER --private-key $PRIV_KEY  --gas-price 10  --contracts-version $VERSION --max-token-networks $MAX_TOKENS

```


4.  After executing this script the console will show you the addresses of the contracts. For example:

```
$  python -m lumino_contracts.deploy lumino --rpc-provider $PROVIDER --private-key $PRIV_KEY  --gas-price 10  --contracts-version $VERSION --max-token-networks $MAX_UINT256
Web3 provider is RPC connection http://127.0.0.1:4444
Enter the private key password: 
INFO:raiden_contracts.deploy.contract_deployer:Skipped checks against the source code because it is not available.
DEBUG:raiden_contracts.deploy.contract_deployer:Deploying EndpointRegistry txHash=0xff1ea52647eab0825dbe9c90e145e41901f8a3e3bbf9cfcc0e699577639aa19b, contracts version 0.12.0
INFO:raiden_contracts.deploy.contract_deployer:EndpointRegistry address: 0x740023b027f107975ed092f87705ab912C937c4e. Gas used: 555302
DEBUG:raiden_contracts.deploy.contract_deployer:Deploying SecretRegistry txHash=0x1272185c2d2a0f77535cfe6acc0eb998c3f47aff63170f09d718662d65ff654a, contracts version 0.12.0
INFO:raiden_contracts.deploy.contract_deployer:SecretRegistry address: 0xff10e500973A0B0071e2263421e4AF60425834a6. Gas used: 313338
DEBUG:raiden_contracts.deploy.contract_deployer:Deploying TokenNetworkRegistry txHash=0x4b8ddaaa7840164023fbc7245d2db44ef4517a30d87bc0a959c9aaa30b1d2987, contracts version 0.12.0
INFO:raiden_contracts.deploy.contract_deployer:TokenNetworkRegistry address: 0x46492F3B5493a091fE5e7FEf2703A4D63b097A40. Gas used: 5236320
Deployment information for chain id = 33  has been updated at /home/marcos/rsk/raidenContractsMerge/raiden-contracts/raiden_contracts/data_0.12.0/deployment_private_net.json.
EndpointRegistry at 0x740023b027f107975ed092f87705ab912C937c4e matches the compiled data from contracts.json
SecretRegistry at 0xff10e500973A0B0071e2263421e4AF60425834a6 matches the compiled data from contracts.json
TokenNetworkRegistry at 0x46492F3B5493a091fE5e7FEf2703A4D63b097A40 matches the compiled data from contracts.json
Deployment info from /home/marcos/rsk/raidenContractsMerge/raiden-contracts/raiden_contracts/data_0.12.0/deployment_private_net.json has been verifiedand it is CORRECT.
{
    "EndpointRegistry": "0x740023b027f107975ed092f87705ab912C937c4e",
    "SecretRegistry": "0xff10e500973A0B0071e2263421e4AF60425834a6",
    "TokenNetworkRegistry": "0x46492F3B5493a091fE5e7FEf2703A4D63b097A40"
}

```
#### Deploy a new ERC20 Token into RSK

In order to register an ERC20 Token into de created Lumino network you need to first deploy it. To deploy a ERC20 you can use:

-   [Truffle](https://truffleframework.com/) 
-   [Remix](http://remix.ethereum.org/)
-   Use local version of  [MyEtherWallet](https://github.com/MyEtherWallet/MyEtherWallet/releases)  (doesn't need HTTPS RSK endpoint)
-   Any other mainstream deployment tool

Just make sure that

1.  Your RSK node accepts incoming connections for those domains
2.  Your ERC20 token satisfies the Lumino ERC20 Standard.

If you want to just poke arround with Lumino, without a specific ERC20 Token, you can use the  `lumino_contracts.deploy token`  script specifying:

-   `--private-key`: Path to the RSK account private key, typically a keystore file.
-   `--gas-price`: RBTC gas price of the onchain operations.
-   `--gas-limit`: RBTC gas limit of the operation.
-   `--token-supply`: RBTC total supply of the Token. Will be added to the owner of the contract, the deployer account.
-   `--rpc-provider`: RSK node endpoint.
-   `--token-name`: ERC20 standard name
-   `--token-symbol`: ERC20 standard symbol
-   `--contracts-version`: Lumino smart contracts version.

```
python -m lumino_contracts.deploy token --rpc-provider $PROVIDER --private-key $PRIV_KEY --gas-price 10 --token-supply 10000000000 --token-name LuminoToken --token-decimals 18 --token-symbol LUM --contracts-version $VERSION

```
After execution succeeds, a CustomToken address is revealed:

```
$  python -m lumino_contracts.deploy token --rpc-provider $PROVIDER --private-key $PRIV_KEY --gas-price 10 --gas-limit 6000000 --token-supply 10000000000 --token-name LuminoToken --token-decimals 18 --token-symbol LUM --contracts-version $VERSION
Web3 provider is RPC connection http://127.0.0.1:4444
Enter the private key password: 
INFO:raiden_contracts.deploy.contract_deployer:Skipped checks against the source code because it is not available.
DEBUG:raiden_contracts.deploy.contract_deployer:Deploying CustomToken txHash=0x2f4638cb44b908c52b1be9ca6ba2f287643ff75da03de48f0d397cce26a4bdc3, contracts version 0.12.0
INFO:raiden_contracts.deploy.contract_deployer:CustomToken address: 0xf2917b0EaA68b5f1BDdBA5241aDcfaC9C8F29B63. Gas used: 1475526
{
    "CustomToken": "0xf2917b0EaA68b5f1BDdBA5241aDcfaC9C8F29B63"
}

```

#### Register a new ERC20 Token into a Lumino network

Now that the Lumino contracts and a ERC20 Token were deployed is time to register the ERC20 token into the Lumino network.

For doing that, we encourage you to use the  `lumino_contracts.deploy register`  script. You must specify:

-   `--private-key`: Path to the RSK account private key, typically a keystore file.
-   `--gas-price`: RBTC gas price of the onchain operations.
-   `--gas-limit`: RBTC gas limit of the operation.
-   `--rpc-provider`: RSK node endpoint.
-   `--token-address`: RSK address of the deployed ERC20 Token
-   `--registry-address`: RSK address of the deployed TokenNetworkRegistry contract
-   `--channel-participant-deposit-limit`: Deposit limit (on wei) for each channel
-   `--token-network-deposit-limit`: Maximum summatory of deposit limits of the network


```
export TokenNetworkRegistry="0x46492F3B5493a091fE5e7FEf2703A4D63b097A40"
export TOKEN="0xf2917b0EaA68b5f1BDdBA5241aDcfaC9C8F29B63"

python -m lumino_contracts.deploy register --rpc-provider $PROVIDER --private-key $PRIV_KEY --gas-price 10 --gas-limit 6000000 --token-address $TOKEN --token-network-registry-address $TokenNetworkRegistry --contracts-version $VERSION --channel-participant-deposit-limit 1000000000000000000 --token-network-deposit-limit 10000000000000000000

```
If registration succeeds, the execution will end up showing the address of a TokenNetwork contract that was deployed:

```
$ python -m lumino_contracts.deploy register --rpc-provider $PROVIDER --private-key $PRIV_KEY --gas-price 10 --gas-limit 6000000 --token-address $TOKEN --token-network-registry-address $TokenNetworkRegistry --contracts-version $VERSION --channel-participant-deposit-limit 1000000000000000000 --token-network-deposit-limit 10000000000000000000
Web3 provider is RPC connection http://127.0.0.1:4444
Enter the private key password: 
INFO:raiden_contracts.deploy.contract_deployer:Skipped checks against the source code because it is not available.
DEBUG:raiden_contracts.deploy.contract_deployer:Sending txHash=0xf0d924624ccd676b15a62563ad213ae8c8413b40dd1d392cb83698c4bff2c7f7
DEBUG:raiden_contracts.deploy.contract_deployer:TokenNetwork address: 0x6fA48caE35eAd4353075c55Db839Fdb1000CAd77

```
Now you are ready to run your Lumino client.

## Additional help

The following sections are created using an Ubuntu 16.04.6

### Install Python 3.7

Download it from https://www.python.org/downloads/

### Install PIP3

```sudo apt update```

```sudo apt-get install python3-pip```

### Install virtualenv

```sudo apt update```

```sudo apt-get install virtualenv```


## Useful Links


* [RIF Lumino Network documentation](https://www.rifos.org/rif-lumino-network/)
* [http://explorer.lumino.rifos.org/](https://explorer.lumino.rifos.org/)
* [RIF Lumino Network](https://github.com/rsksmart/lumino) 
* [RIF Lumino Web](https://github.com/rsksmart/lumino-web) 
* [RIF Lumino Explorer](https://github.com/rsksmart/lumino-explorer) 
