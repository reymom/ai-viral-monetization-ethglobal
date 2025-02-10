import os
import requests
from dotenv import load_dotenv
load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
PINATA_JSON_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
PINATA_FILE_UPLOAD_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"


def upload_image_to_pinata(image_path):
    """Uploads an image to Pinata (IPFS) and returns the IPFS URI."""
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    with open(image_path, "rb") as file:
        files = {"file": file}
        response = requests.post(
            PINATA_FILE_UPLOAD_URL, headers=headers, files=files)

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"ipfs://{ipfs_hash}"
    else:
        raise Exception(f"❌ Failed to upload image: {response.text}")


def upload_metadata_to_pinata(metadata):
    """Uploads NFT metadata to Pinata (IPFS) and returns the IPFS URI."""
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(PINATA_JSON_UPLOAD_URL, headers=headers, json={
                             "pinataContent": metadata})

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"ipfs://{ipfs_hash}"
    else:
        raise Exception(f"❌ Failed to upload metadata: {response.text}")


def generate_metadata(tweet_id: str, image_url: str, tweet_text: str):
    """Generates NFT metadata for a given tweet and image, then uploads it to IPFS."""
    metadata = {
        "name": f"TweetNFT-{tweet_id}",
        "description": tweet_text,
        "image": image_url,
        "attributes": [
            {"trait_type": "Tweet ID", "value": tweet_id}
        ]
    }

    metadata_uri = upload_metadata_to_pinata(metadata)
    return metadata_uri


if __name__ == "__main__":
    tweet_id = input("Enter Tweet ID: ").strip()
    image_path = "data/futuristic_city.png"
    tweet_text = input("Enter Tweet Text: ").strip()

    image_uri = upload_image_to_pinata(image_path)
    print(f"🔗 Image URI: {image_uri}")
    metadata_uri = generate_metadata(tweet_id, image_uri, tweet_text)
    print(f"🔗 Metadata URI: {metadata_uri}")
