from os import access
from brownie import network, RatsCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_account
import json

# We could save meta data in some files and pull the meta data from files instead


def main():
    print(f"Working on {network.show_active()}")
    rat_collectible = RatsCollectible[-1]
    number_of_collectibles = rat_collectible.tokenCounter()
    print(f"You have {number_of_collectibles} tokenIds.")
    for token_id in range(number_of_collectibles):
        (
            size,
            accessory,
            _,
            _,
            _,
            _,
            _,
            _,
            _,
        ) = rat_collectible.tokenIdToRat(token_id)
        # If it doesn't start with https we know that it hasn't been set yet
        if not rat_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{size}-{accessory}-path.json"
            data = json.load(open(metadata_file_name, "r"))
            set_tokenURI(token_id, rat_collectible, data["uri"])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}"
    )
    print("Please wait up to 20 minutes and hit refresh metadata button.")
