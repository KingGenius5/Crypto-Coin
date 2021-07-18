from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_meta
from pathlib import Path


def main():
    print("Working on " + network.show_active())
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    number_of_tokens = advanced_collectible.tokenCounter()
    print("The number of tokens you've deployed is {}".format(number_of_tokens))
    write_metadata(number_of_tokens, advanced_collectible)


def write_metadata(number_of_tokens, nft_contract):
    for token_id in range(number_of_tokens):
        collectible_metadata = sample_metadata.metadata_template
        meta = get_meta(nft_contract.tokenIdToMeta(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active()) +
            str(token_id) + "-" + meta + ".json"
        )
        # basically creating a file path called metadata/rinkeby/0-STEALTH.json
        if Path(metadata_file_name).exists():
            print("{} already found!".format(metadata_file_name))
        else:
            print("Creating metadata file {}".format(metadata_file_name))
            collectible_metadata["name"] = get_meta(
                nft_contract.tokenIdToMeta(token_id))
            collectible_metadata["description"] = "Having the powers of {} doesn't stop this awesome person from killing it in the software engineering game!".format(
                collectible_metadata["name"])
            print(collectible_metadata)
