from base.cdp_wallet import WalletManager

if __name__ == "__main__":
    wallet_manager = WalletManager()

    # ✅ Step 1: Print wallet address
    print("\n🔹 Wallet Address:", wallet_manager.get_wallet_address())

    # ✅ Step 2: Deploy test token & NFT
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

    # ✅ Step 3: Simulate engagement data
    engagement_data = {
        "likes": ["user1", "user2", "user3"],
        "retweets": ["user1", "user4"],
        "comments": {
            "user1": "0x60e40ecf531F13bAa71Ff23aCff347BF47fa3274",
            "user3": "0xd9A870f56Aa563A9671028518b1222d8B4Ce02e0",
        }
    }

    # ✅ Step 4: Distribute rewards based on engagement
    print("\n🎁 Distributing Rewards...")
    wallet_manager.distribute_rewards("123456789", engagement_data)

    print("\n🎉 Reward Distribution Completed!")
