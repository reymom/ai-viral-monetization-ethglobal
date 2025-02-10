from base.cdp_wallet import WalletManager

if __name__ == "__main__":
    wallet_manager = WalletManager()

    print("\n🔹 Wallet Address:", wallet_manager.get_wallet_address())

    # ✅ Step 1: Deploy test token & NFT
    print("\n🚀 Deploying Test Token...")
    token_address = wallet_manager.deploy_token(
        name="TestToken",
        symbol="TTK",
        supply="1000000",
        tweet_id="123456789"
    )
    print(f"✅ Token deployed at: {token_address}")

    print("\n🚀 Minting Test NFT...")
    nft_address = wallet_manager.mint_nft(
        tweet_id="123456789",
        metadata_uri="ipfs://sampleMetadata"
    )
    print(f"✅ NFT deployed at: {nft_address}")

    # ✅ Step 2: Use latest engagement data format
    engagement_data = {
        "likes": ["0xReymon", "simonantzo", "dericaamani", "GuessSteph52287", "GlobalCoinHub", "LWell58215"],
        "comments": {
            "0xReymon": "0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0"
        }
    }

    # ✅ Step 3: Distribute rewards
    print("\n🎁 Distributing Rewards...")
    wallet_manager.distribute_rewards("123456789", engagement_data)

    print("\n🎉 Reward Distribution Completed!")
