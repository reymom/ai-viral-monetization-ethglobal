import random
import re
import os
import json
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from base.config import CDP_API_KEY_NAME, CDP_API_KEY_PRIVATE_KEY, NETWORK_ID


WALLET_FILE = "data/wallet.json"


class WalletManager:
    """Manages the agent's wallet for deploying tokens, NFTs, and distributing rewards."""

    def __init__(self):
        self.load_wallet()

    def load_wallet(self):
        """Loads wallet from file if available, otherwise creates a new one."""
        wallet_data = self._read_wallet_data()
        values = {"cdp_wallet_data": wallet_data} if wallet_data else {}

        self.cdp = CdpAgentkitWrapper(
            api_key_name=CDP_API_KEY_NAME,
            api_key_private_key=CDP_API_KEY_PRIVATE_KEY,
            **values
        )

        if not wallet_data:
            self._save_wallet_data(self.cdp.export_wallet())

        self.toolkit = CdpToolkit.from_cdp_agentkit_wrapper(self.cdp)
        self.tools = {tool.name: tool for tool in self.toolkit.get_tools()}
        self.tweet_to_contracts = {}

    def get_wallet_address(self):
        """Returns the agent's wallet address."""
        return self.cdp.wallet.default_address.address_id

    def _read_wallet_data(self):
        """Reads wallet data from the local file if it exists and is valid."""
        if os.path.exists(WALLET_FILE):
            try:
                with open(WALLET_FILE, "r") as f:
                    data = json.load(f)
                    if not data:
                        raise ValueError("Empty wallet.json file")
                    return data
            except (json.JSONDecodeError, ValueError) as e:
                print(f"❌ Invalid wallet.json file, regenerating wallet: {e}")
                os.remove(WALLET_FILE)  # Delete corrupted file
        return None

    def _save_wallet_data(self, wallet_data):
        """Saves wallet data to a local file."""
        with open(WALLET_FILE, "w") as f:
            json.dump(wallet_data, f)

    def deploy_token(self, name: str, symbol: str, supply: int, tweet_id: str):
        """Deploys an ERC-20 token using AgentKit."""
        print(
            f"🚀 Deploying {name} ({symbol}) with supply {supply} on {NETWORK_ID}...")

        if "deploy_token" not in self.tools:
            raise ValueError("❌ `deploy_token` tool not found in AgentKit!")

        deploy_tool = self.tools["deploy_token"]
        tx = deploy_tool.run(
            {"name": name, "symbol": symbol, "total_supply": str(supply)})

        if isinstance(tx, str):
            contract_address = tx
        else:
            contract_address = tx["contract_address"]
        print(f"✅ Token deployed at {contract_address}")

        if tweet_id not in self.tweet_to_contracts:
            self.tweet_to_contracts[tweet_id] = {
                "token": contract_address, "nft": None}
        else:
            self.tweet_to_contracts[tweet_id]["nft"] = contract_address
        return contract_address

    def mint_nft(self, tweet_id: str, metadata_uri: str):
        """Mints an ERC-721 NFT using AgentKit."""
        name = f"AgenticNFT-{tweet_id}"
        symbol = f"AGNTC{tweet_id[-4:]}"
        print(
            f"🚀 Minting NFT {name} ({symbol}) with metadata at {metadata_uri} on {NETWORK_ID}...")

        if "deploy_nft" not in self.tools:
            raise ValueError("❌ `deploy_nft` tool not found in AgentKit!")

        deploy_nft_tool = self.tools["deploy_nft"]
        tx = deploy_nft_tool.run(
            {"name": name, "symbol": symbol, "base_uri": metadata_uri})

        if isinstance(tx, str):
            contract_address = tx  # If response is a raw string, use it directly
        else:
            contract_address = tx["contract_address"]
        print(f"✅ NFT contract deployed at {contract_address}")

        if tweet_id not in self.tweet_to_contracts:
            self.tweet_to_contracts[tweet_id] = {
                "token": None, "nft": contract_address}
        else:
            self.tweet_to_contracts[tweet_id]["nft"] = contract_address
        return contract_address

    def extract_wallet_address(self, comment: str):
        """Extracts a valid blockchain wallet address from a comment."""
        match = re.search(
            r"0x[a-fA-F0-9]{40}", comment)  # Matches Ethereum/Base addresses
        return match.group(0) if match else None

    def distribute_rewards(self, tweet_id: str, engagement_data: dict):
        """Distributes ERC-20 tokens to users who liked/retweeted/commented and selects one to receive the NFT."""
        if tweet_id not in self.tweet_to_contracts:
            print("❌ No deployed token or NFT found for this tweet.")
            return

        token_address = self.tweet_to_contracts[tweet_id]["token"]
        nft_address = self.tweet_to_contracts[tweet_id]["nft"]

        if not token_address:
            print("❌ No token deployed for this tweet.")
            return

        eligible_users = set(engagement_data.get("likes", [])) | set(
            engagement_data.get("retweets", []))
        # Reward each user with 100 tokens
        user_rewards = {user: 100 for user in eligible_users}

        if "transfer" not in self.tools:
            raise ValueError("❌ `transfer` tool not found in AgentKit!")

        transfer_tool = self.tools["transfer"]

        for user, amount in user_rewards.items():
            wallet_address = self.extract_wallet_address(
                engagement_data.get("comments", {}).get(user, ""))
            if wallet_address:
                print(
                    f"💰 Sending {amount} tokens to {wallet_address} from {token_address}...")
                transfer_tool.run({
                    "destination": wallet_address,
                    "amount": str(amount),
                    "asset_id": token_address
                })

        if nft_address:
            users_with_valid_addresses = [self.extract_wallet_address(comment) for comment in engagement_data.get(
                "comments", {}).values() if self.extract_wallet_address(comment)]
            if users_with_valid_addresses:
                selected_user = random.choice(users_with_valid_addresses)
                print(f"🎨 Sending NFT {nft_address} to {selected_user}...")
                transfer_tool.run({
                    "destination": selected_user,
                    "amount": "1",
                    "asset_id": nft_address
                })
            else:
                print(
                    "❌ No valid wallet addresses found in comments, NFT not distributed.")

        print("✅ Rewards distributed successfully.")
