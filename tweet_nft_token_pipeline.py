import time

from base.cdp_wallet import WalletManager
from base.generate_metadata import upload_image_to_pinata, generate_metadata
from twitter.post_tweet import post_tweet_with_image
from twitter.track_engagement import get_tweet_engagement


class TweetNFTPipeline:
    """Handles the full pipeline: Tweet -> NFT & Token -> Engagement -> Reward Distribution."""

    def __init__(self, interval=300):
        self.wallet_manager = WalletManager()
        self.interval = interval  # Time in seconds before reward distribution

    def execute_pipeline(self, tweet_text: str, image_path: str):
        """Executes the full pipeline for posting, minting, and rewarding."""
        print("🐦 Posting tweet...")
        tweet_id = post_tweet_with_image(tweet_text, image_path)
        if not tweet_id:
            print("❌ Failed to post tweet. Stopping pipeline.")
            return

        print("🚀 Uploading image to IPFS...")
        image_ipfs_uri = upload_image_to_pinata(image_path)
        if not image_ipfs_uri:
            print("❌ Image upload failed. Stopping pipeline.")
            return

        print("📄 Generating metadata and uploading to IPFS...")
        metadata_ipfs_uri = generate_metadata(
            tweet_id, image_ipfs_uri, tweet_text)
        if not metadata_ipfs_uri:
            print("❌ Metadata upload failed. Stopping pipeline.")
            return

        print("🔗 Deploying ERC-20 Token...")
        token_address = self.wallet_manager.deploy_token(
            f"Agentic-{tweet_id}", f"AGENTIC{tweet_id[-4:]}", 1000000, tweet_id)
        if not token_address:
            print("❌ Token deployment failed. Stopping pipeline.")
            return

        print("🎨 Minting NFT...")
        nft_address = self.wallet_manager.mint_nft(tweet_id, metadata_ipfs_uri)
        if not nft_address:
            print("❌ NFT minting failed. Stopping pipeline.")
            return

        print(
            f"✅ Tweet {tweet_id} processed! Waiting {self.interval} seconds before reward distribution...")
        time.sleep(self.interval)

        print("📊 Checking tweet engagement...")
        engagement_data = get_tweet_engagement(tweet_id)

        print("💰 Distributing rewards...")
        self.wallet_manager.distribute_rewards(tweet_id, engagement_data)
        print("✅ Pipeline execution complete.")


if __name__ == "__main__":
    pipeline = TweetNFTPipeline(interval=200)

    tweet_text = (
        "🚀 The Future of AI x Blockchain at #ETHGlobal Agentic! 🔥\n\n"
        "💡 Using @CoinbaseDev AgentKit on @BuildOnBase to create AI-powered onchain automation!\n"
        "🔗 NFTs & ERC-20 rewards for engagement and monetization on every tweet!\n\n"
        "#Web3 #AI #Base #NFT #Crypto #ETHGlobal"
    )
    image_path = "data/futuristic_city.png"

    print("✅ Running test pipeline with pre-defined tweet and image...")
    pipeline.execute_pipeline(tweet_text, image_path)
    print("🎉 Test pipeline executed successfully!")
