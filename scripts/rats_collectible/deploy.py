from brownie.network.main import show_active
from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    OPENSEA_URL,
    get_contract,
)
from brownie import RatsCollectible, network, config


def deploy():
    account = get_account()
    rats_collectible = RatsCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return rats_collectible


def main():
    deploy()
