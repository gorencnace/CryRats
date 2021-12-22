import json
from brownie import RatsCollectible, network
from scripts.helpful_scripts import get_size, get_accessory
from scripts.image_generator.create_rat_img import generate_rat
from metadata.sample_metadata import metadata_template, metadata_template_json
from pathlib import Path
import requests
import json
import os


def main():
    rat_collectible = RatsCollectible[-1]
    number_of_rat_collectibles = rat_collectible.tokenCounter()
    print(f"You have created {number_of_rat_collectibles} collectibles.")
    for token_id in range(number_of_rat_collectibles):
        (
            size,
            accessory,
            rat_primary,
            rat_secondary,
            rat_tertiary,
            rat_eyes,
            background,
            accessory_primary,
            accessory_secondary,
        ) = rat_collectible.tokenIdToRat(token_id)
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{size}-{accessory}"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to override.")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata[
                "name"
            ] = f"{get_size(size % 3)} {get_accessory(accessory)}"
            collectible_metadata[
                "description"
            ] = f"Randomly generated {get_size(size % 3)} {get_accessory(accessory)} rat!"
            collectible_metadata["attributes"] = [
                {"trait_type": "Shape", "value": get_size(size % 3)},
                {"trait_type": "Belly", "value": "False" if size < 3 else "True"},
                {"trait_type": "Accessory", "value": get_accessory(accessory)},
            ]
            image_path = generate_rat(
                token_id,
                size,
                accessory,
                rat_primary,
                rat_secondary,
                rat_tertiary,
                rat_eyes,
                background,
                accessory_primary,
                accessory_secondary,
            )
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name + ".json", "w") as file:
                json.dump(collectible_metadata, file)

            if os.getenv("UPLOAD_IPFS") == "true":
                token_uri = upload_to_ipfs(metadata_file_name + ".json")
                with open(metadata_file_name + "-path.json", "w") as file:
                    collectible_metadata = metadata_template_json
                    collectible_metadata["uri"] = token_uri
                    json.dump(collectible_metadata, file)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # split where "/" is, put it in array and grab the last part of the array
        # ("./img/0-PUG.png" -> "0-PUG.png")
        filename = filepath.split("/")[-1:][0]
        # "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.js"
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
