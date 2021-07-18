from brownie import AdvancedCollectible, accounts, config
from scripts.helpful_scripts import get_meta
import time

STATIC_SEED = 123


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    transaction = advanced_collectible.createCollectible(
        STATIC_SEED, "None", {"from": dev})
    print("Waiting on second transaction...")
    # wait for the 2nd transaction
    transaction.wait(1)
    time.sleep(35)
    requestId = transaction.events["requestedCollectible"]["requestId"]
    token_id = advanced_collectible.requestIdToTokenId(requestId)
    meta = get_meta(advanced_collectible.tokenIdToMeta(token_id))
    print("Hero meta of tokenId {} is {}".format(token_id, meta))
