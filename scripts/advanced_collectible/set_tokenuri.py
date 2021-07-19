from brownie import AdvancedCollectible, network, accounts, config
from scripts.helpful_scripts import get_meta

hero_metadata_dic = {
    "ALIEN": "https://ipfs.io/ipfs/QmamJ18UXv17eDUk1YFJUfWQazbFsoR8p3ZjpZXAMEFQ5d?filename=alien.png",
    "STEALTH": "https://ipfs.io/ipfs/QmS3PwVi9SitwcWhUpMhkzdVx9ZES4YkjUryCcZ128pzpX?filename=stealth.png",
}

OPENSEA_FORMAT = "https://testnets.opensea.io/assets/{}/{}"


def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(
        "The number of tokens you've deployed is: "
        + str(number_of_advanced_collectibles)
    )
    for token_id in range(number_of_advanced_collectibles):
        meta = get_meta(advanced_collectible.tokenIdToMeta(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, advanced_collectible,
                         hero_metadata_dic[meta])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = accounts.add(config["wallets"]["from_key"])
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button.')
