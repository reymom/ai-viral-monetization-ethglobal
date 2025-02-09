from twitter.post_tweet import post_tweet
from base.generate_metadata import generate_metadata, upload_image_to_ipfs
from base.cdp_wallet import WalletManager


def tweet_to_nft_and_token(tweet_text: str, image_path: str):
    """Posts a tweet, uploads image & metadata to IPFS, deploys token, and mints an NFT."""
    print("🚀 Posting tweet...")
    tweet_id = post_tweet(tweet_text, image_path)

    print("🖼️ Uploading image to IPFS...")
    image_ipfs_uri = upload_image_to_ipfs(image_path)

    print("📄 Generating metadata and uploading to IPFS...")
    metadata_ipfs_uri = generate_metadata(tweet_id, image_ipfs_uri, tweet_text)

    wallet = WalletManager()
    print("🔗 Deploying ERC-20 Token on Base L2...")
    token_contract_address = wallet.deploy_token(
        f"Tweet-{tweet_id}", f"TWT{tweet_id[-4:]}", 1000000)

    print("🔗 Minting NFT on Base L2...")
    nft_contract_address = wallet.mint_nft(tweet_id, metadata_ipfs_uri)

    print(f"✅ Token for Tweet {tweet_id} deployed at {token_contract_address}")
    print(f"✅ NFT for Tweet {tweet_id} minted at {nft_contract_address}")
    return nft_contract_address


if __name__ == "__main__":
    tweet_text = input("Enter Tweet Text: ").strip()
    image_path = input("Enter Image Path: ").strip()
    token_address, nft_address = tweet_to_nft_and_token(tweet_text, image_path)
    print(f"🎉 Token Minted: {token_address}")
    print(f"🎉 NFT Minted: {nft_address}")
