from base.cdp_wallet import WalletManager

if __name__ == "__main__":
    wallet_manager = WalletManager()

    # ✅ Print wallet address to confirm it's consistent
    print("🔹 Wallet Address:", wallet_manager.get_wallet_address())

    # ✅ Deploy a test ERC-20 token
    print("\n🚀 Deploying Test Token...")
    token_address = wallet_manager.deploy_token(
        name="TestToken",
        symbol="TTK",
        supply="1000000",
        tweet_id="123456789"
    )

    # ✅ Mint an NFT for testing
    print("\n🚀 Minting Test NFT...")
    nft_address = wallet_manager.mint_nft(
        tweet_id="123456789",
        metadata_uri="ipfs://sampleMetadata"
    )

    print("\n🎉 Done. Check Base explorer for deployed contracts!")
