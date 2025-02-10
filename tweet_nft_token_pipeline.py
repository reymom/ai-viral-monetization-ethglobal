import time
import sys

from base.cdp_wallet import WalletManager
from base.generate_metadata import upload_image_to_pinata, generate_metadata
from twitter.post_tweet import post_tweet_with_image
from twitter.track_engagement import get_tweet_engagement
from base.agent import execute_agent_request


class TweetNFTPipeline:
    """Handles the full pipeline: Tweet -> NFT & Token -> Engagement -> Reward Distribution."""

    def __init__(self, interval=300):
        self.wallet_manager = WalletManager()
        self.interval = interval  # Time in seconds before reward distribution

    def execute_pipeline(self, tweet_prompt: str):
        """Executes the full pipeline for posting, minting, and rewarding."""
        print("\n" + "=" * 60)
        print("🤖 STEP 1: Generating AI-powered tweet...")
        print("=" * 60)
        tweet_text = execute_agent_request(tweet_prompt)
        print(f"\n📝 Generated Tweet:\n{tweet_text}\n")

        # Ask for user confirmation to proceed
        print("-" * 50)
        user_input = input(
            "👍 Do you like this tweet? (yes/no/edit): ").strip().lower()
        print("-" * 50)
        if user_input in ["no", "n"]:
            print("\n❌ Tweet rejected. Stopping pipeline.\n")
            return
        elif user_input in ["edit", "e"]:
            tweet_text = input("✍️ Enter your modified tweet: ").strip()
            print(f"\n✅ New Tweet: {tweet_text}\n")

        print("\n" + "=" * 60)
        print("🎨 STEP 2: Generating AI-powered image...")
        print("=" * 60)
        image_path = execute_agent_request(
            f"Generate an AI image for this tweet: {tweet_text}", "dalle-image-generator")
        print(f"\n🖼️ Image saved at: {image_path}\n")

        print("\n" + "=" * 60)
        print("🐦 STEP 3: Posting Tweet...")
        print("=" * 60)

        tweet_id = post_tweet_with_image(tweet_text, image_path)
        if not tweet_id:
            print("\n❌ Failed to post tweet. Stopping pipeline.\n")
            return
        print(f"🐦 Tweet posted: https://x.com/0xReymon/status/{tweet_id}")

        print("\n" + "=" * 60)
        print("🚀 STEP 4: Uploading Image & Generating Metadata...")
        print("=" * 60)

        image_ipfs_uri = upload_image_to_pinata(image_path)
        if not image_ipfs_uri:
            print("\n❌ Image upload failed. Stopping pipeline.\n")
            return

        metadata_ipfs_uri = generate_metadata(
            tweet_id, image_ipfs_uri, tweet_text)
        if not metadata_ipfs_uri:
            print("\n❌ Metadata upload failed. Stopping pipeline.\n")
            return

        print("\n" + "=" * 60)
        print("🔗 STEP 5: Deploying ERC-20 Token & Minting NFT...")
        print("=" * 60)
        token_address = self.wallet_manager.deploy_token(
            f"Agentic-{tweet_id}", f"AGENTIC{tweet_id[-4:]}", 1000000, tweet_id)
        if not token_address:
            print("\n❌ Token deployment failed. Stopping pipeline.\n")
            return
        print(f"✅ Token deployed at: {token_address}")

        nft_address = self.wallet_manager.mint_nft(tweet_id, metadata_ipfs_uri)
        if not nft_address:
            print("\n❌ NFT minting failed. Stopping pipeline.\n")
            return
        print(f"✅ NFT deployed at: {nft_address}")

        print("\n" + "=" * 60)
        print(
            f"✅ Tweet {tweet_id} processed! Waiting {self.interval} seconds before reward distribution...")
        print("=" * 60)

        print("\n" + "=" * 60)
        print("📊 STEP 6: Checking Tweet Engagement & Distributing Rewards...")
        print("=" * 60)
        engagement_data = get_tweet_engagement(tweet_id)
        print("\n📊 Engagement Summary:")
        print("-" * 50)
        print(f"👍 Liked by: {engagement_data['likes']}")
        print(
            f"💬 Comments with wallet addresses: {engagement_data['comments']}")
        print("-" * 50)

        self.wallet_manager.distribute_rewards(tweet_id, engagement_data)
        print("✅ Pipeline execution complete.")


def countdown_timer(seconds):
    """Displays a countdown timer before execution."""
    for remaining in range(seconds, 0, -1):
        sys.stdout.write(
            f"\r⏳ Waiting {remaining} seconds before reward distribution...")
        sys.stdout.flush()
        time.sleep(1)
    print("\n✅ Time's up! Distributing rewards...\n")


if __name__ == "__main__":
    pipeline = TweetNFTPipeline(interval=200)

    print("\n" + "=" * 80)
    print("✅ Running test pipeline with pre-defined tweet and image...")
    print("=" * 80 + "\n")

    tweet_prompt = """
        🔥 Generate a high-impact, viral tweet about AI, Web3, and blockchain automation with AgentKit. Focus on:
        The power of AI-driven onchain automation
        NFTs & ERC-20 rewards for engagement
        How AgentKit + Base enable decentralized monetization
        Exciting future applications beyond the hackathon
        Tagging @coinbaseDev, @BuildOnBase, and any key partners
        Use of 🔥 emojis & concise phrasing to drive engagement
    """
    pipeline.execute_pipeline(
        "Generate a viral tweet about AI, Web3, and blockchain automation with AgentKit.")
    print("\n🎉 Test pipeline executed successfully!\n")
