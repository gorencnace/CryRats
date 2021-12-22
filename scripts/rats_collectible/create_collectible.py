from brownie import RatsCollectible
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3


def create():
    account = get_account()
    rats_collectible = RatsCollectible[-1]
    fund_with_link(rats_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = rats_collectible.createCollectible({"from": account})
    creation_transaction.wait(1)
    print("Collectible created!")


def main():
    create()
