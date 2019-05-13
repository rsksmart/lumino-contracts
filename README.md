# RIF Lumino Contracts

![Lumino Network](Lumino.png?raw=true "RIF Lumino Network")


## Overview

Lumino has a set of Smart Contracts, that must be deployed into the RSK network, that are in charge of handling all the on-chain operations.


## Pre requisites

1. RSK account with RBTC balance
2. Python 3.6
3. Pip
4. Virtualenv
5. Yarn (Latest Version)



## Build RIF Lumino contract 

1. Get the [RELEASE.NUMBER] code from [GITHUB.URL]
2. Go to the path you downloaded or cloned Lumino's code (lets call this path `$RIF_LUMINO_CONTRACTS_PATH`)
3. Create python virtual env for RIF Lumino (this has to be made one time)

```virtualenv -p <PATH_TO_PYTHON3.6> contractsVenv```

**Note 1:**
Replace `<PATH_TO_PYTHON3.6>` for the path where Python3.6 is installed in your system, in the case of Ubuntu this usually is on path `/usr/bin/python3.6`

**Note 2:**
If you receive an error please check ***Additional Help*** section.

4. Activate python virtual env

```$ source contractsVenv/bin/activate```

5. Check Python version is correct inside the virtual environment

Run:

```$ python --version```

This command should output version 3.6.x

6. Install RIF Lumino contracts requirements

Inside the virtual environment run the following command to install the Lumino deployment scripts dependencies:

```$ pip install -r requirements-dev.txt```


## Creating a Lumino custom network

Lumino network is defined by a set of Smart Contracts deployed into RSK. This is a step by step guide for those who wants to create a private custom Lumino network. The guide is based on a regtest node or local cluster of RegTest nodes, but the same steps applies for MainNet or TestNet.

#### Deploy the set of Lumino contracts into RSK
To deploy the TokenNetworkRegistry, SecretRegistry and EndpointRegistry, we encourage you to use the `lumino_contracts.deploy lumino` script specifying:

-   `--private-key`: Path to the RSK account private key, typically a keystore file.
-   `--gas-price`: RBTC gas price of the onchain operations.
-   `--gas-limit`: RBTC gas limit of the onchain operations.
-   `--rpc-provider`: RSK node endpoint.
-   `--contracts-version`: Lumino smart contracts version. Use "0.3._" for development.

```
$ python -m lumino_contracts.deploy lumino --rpc-provider http://127.0.0.1:4444 --private-key PATH-TO-YOUR-KEY-STORE --gas-price 10 --gas-limit 6000000 --contracts-version "0.3._"
```

4.  After executing this script the console will show you the addresses of the contracts. For example:

```
$ python -m lumino_contracts.deploy lumino --rpc-provider http://127.0.0.1:4444 --private-key PATH-TO-YOUR-PRIVATE-KEY --gas-price 10 --gas-limit 6000000 --contracts-version "0.3._"
Web3 provider is RPC connection http://127.0.0.1:4444
Enter the private key password: 
INFO:__main__:Skipped checks against the source code because it is not available.
DEBUG:__main__:Deploying EndpointRegistry txHash=0x1b2053f94092b5a7b5d26f3530a19b8ac1e61b8b992eb10c81e30c722e8de73f, contracts version 0.3._
INFO:__main__:EndpointRegistry address: 0x0ccCe6E177b2293d896704CC27be7E8F02a0AFe1. Gas used: 590283
DEBUG:__main__:Deploying SecretRegistry txHash=0x1c704596ebbb4bca02dafcd8105beae905670756399739e0298b76084cd1dee3, contracts version 0.3._
INFO:__main__:SecretRegistry address: 0x9d899260624419e562794e9d3809d48Aa00B83F2. Gas used: 332473
DEBUG:__main__:Deploying TokenNetworkRegistry txHash=0x5ab5e616299d638cdbcd012974fff7fd79922c6f78810cf5ffe4d758928c7637, contracts version 0.3._
INFO:__main__:TokenNetworkRegistry address: 0x9c6eA70ea1A2Fcbd427D1cBE7DC06D048cf7a3B7. Gas used: 5718316
Deployment information for chain id = 33  has been updated at /home/user/rsk/lumino-contracts/lumino_contracts/data_0.3._/deployment_private_net.json.
EndpointRegistry at 0x0ccCe6E177b2293d896704CC27be7E8F02a0AFe1 matches the compiled data from contracts.json
SecretRegistry at 0x9d899260624419e562794e9d3809d48Aa00B83F2 matches the compiled data from contracts.json
TokenNetworkRegistry at 0x9c6eA70ea1A2Fcbd427D1cBE7DC06D048cf7a3B7 matches the compiled data from contracts.json
Deployment info from /home/user/rsk/lumino-contracts/lumino_contracts/data_0.3._/deployment_private_net.json has been verified and it is CORRECT.
{
    "EndpointRegistry": "0x0ccCe6E177b2293d896704CC27be7E8F02a0AFe1",
    "SecretRegistry": "0x9d899260624419e562794e9d3809d48Aa00B83F2",
    "TokenNetworkRegistry": "0x9c6eA70ea1A2Fcbd427D1cBE7DC06D048cf7a3B7"
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
-   `--token-supply`: RBTC total supply of the Token. Will be added to the owner of the contract, the deployer account.
-   `--rpc-provider`: RSK node endpoint.
-   `--token-name`: ERC20 standard name
-   `--token-symbol`: ERC20 standard symbol
-   `--contracts-version`: Lumino smart contracts version. Use "0.3._" for development.

```
$ python -m lumino_contracts.deploy token --rpc-provider http://127.0.0.1:4444 --private-key PATH-TO-YOUR-PRIVATE-KEY --gas-price 10 --token-supply 10000000 --token-name LuminoToken --token-decimals 18 --token-symbol LUM --contracts-version "0.3._"
```
After execution succeeds, a CustomToken address is revealed:

```
$ python -m lumino_contracts.deploy token --rpc-provider http://127.0.0.1:4444 --private-key PATH-TO-YOUR-PRIVATE-KEY --gas-price 10 --token-supply 10000000 --token-name LuminoToken --token-decimals 18 --token-symbol LUM --contracts-version "0.3._"
Web3 provider is RPC connection http://127.0.0.1:4444
Enter the private key password: 
INFO:__main__:Skipped checks against the source code because it is not available.
DEBUG:__main__:Deploying CustomToken txHash=0x9eb3b7b304f4941527d182f10fdaf7bae034ab9167ad2e835a1f52dbbea4dab0, contracts version 0.3._
INFO:__main__:CustomToken address: 0x22AA07C35ACE7F9A5A1A5D4317EE973389A17Be7. Gas used: 1480697
{
    "CustomToken": "0x22AA07C35ACE7F9A5A1A5D4317EE973389A17Be7"
}
```

#### Register a new ERC20 Token into a Lumino network

Now that the Lumino contracts and a ERC20 Token were deployed is time to register the ERC20 token into the Lumino network.

For doing that, we encourage you to use the  `lumino_contracts.deploy register`  script. You must specify:

-   `--private-key`: Path to the RSK account private key, typically a keystore file.
-   `--gas-price`: RBTC gas price of the onchain operations.
-   `--rpc-provider`: RSK node endpoint.
-   `--token-address`: RSK address of the deployed ERC20 Token
-   `--registry-address`: RSK address of the deployed TokenNetworkRegistry contract

```
python -m lumino_contracts.deploy register --rpc-provider http://127.0.0.1:4444 --private-key PATH-TO-YOUR-PRIVATE-KEY --gas-price 10 --token-address 0x22AA07C35ACE7F9A5A1A5D4317EE973389A17Be7 --registry-address 0x9c6eA70ea1A2Fcbd427D1cBE7DC06D048cf7a3B7 --contracts-version '0.3._'
```
If registration succeeds, the execution will end up showing the address of a TokenNetwork contract that was deployed:

```
$ python -m lumino_contracts.deploy register --rpc-provider http://127.0.0.1:4444 --private-key PATH-TO-YOUR-PRIVATE-KEY --gas-price 10 --token-address 0x22AA07C35ACE7F9A5A1A5D4317EE973389A17Be7 --registry-address 0x9c6eA70ea1A2Fcbd427D1cBE7DC06D048cf7a3B7  --contracts-version '0.3._'
Web3 provider is RPC connection http://127.0.0.1:4444
Enter the private key password: 
DEBUG:__main__:calling createERC20TokenNetwork(0x22AA07C35ACE7F9A5A1A5D4317EE973389A17Be7) txHash=0xd1b842929aecc88aef3b54a4bc5357af4435fbb96602b3075ca309f3178fab86
TokenNetwork address: 0x01D9e450B0DeBe353023D3f58B17d3D00393c74A Gas used: 3837108
```
Now you are ready to run your Lumino client.

## Additional help

The following sections are created using an Ubuntu 16.04.6

### Install Python 3.6

(source: [http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/]())

Add a new repository to you apt:

```sudo add-apt-repository ppa:jonathonf/python-3.6```

Update your local APT repository:

```sudo apt-get update```

Install Python 3.6:

```sudo apt-get install python3.6```

### Install PIP3

If you didn't update your local APT repository:

```sudo apt update```

Install pip3:

```sudo apt-get install python3-pip```

### Install virtualenv

If you didn't update your local APT repository:

```sudo apt update```

Install virtualenv:

```sudo apt-get install virtualenv```


## Useful Links

* [RIF Lumino Network](https://www.rifos.org/rif-lumino-network/)
* [RIF Lumino Explorer](http://explorer.lumino.rifos.org/)