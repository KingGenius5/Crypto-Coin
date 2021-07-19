from brownie import AdvancedCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_meta
from pathlib import Path
import os
import requests
import json


meta_to_image_uri = {
    "ALIEN": "https://ipfs.io/ipfs/QmamJ18UXv17eDUk1YFJUfWQazbFsoR8p3ZjpZXAMEFQ5d?filename=alien.png",
}


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
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    meta.lower().replace("_", "-"))
                image_to_upload = upload_to_ipfs(
                    image_path)
            image_to_upload = meta_to_image_uri[meta] if not image_to_upload else image_to_upload
            collectible_metadata["image"] = image_to_upload
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)

# curl -X POST file=@img/stealth.png http://localhost:5001/api/v0/add
# We want to do ^ but in a function instead of through the terminal


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://localhost:5001"
        response = requests.post(ipfs_url + "/api/v0/add",
                                 files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        uri = "https://ipfs.io/ipfs/{}?filename={}".format(
            ipfs_hash, filename)
        print(uri)
        return uri
    return None
