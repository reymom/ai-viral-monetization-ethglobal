import random
import os
import json
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from base.config import CDP_API_KEY_NAME, CDP_API_KEY_PRIVATE_KEY, NETWORK_ID
from database.db_manager import db_manager


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
        existing_contracts = db_manager.get_contracts(tweet_id)
        if existing_contracts.get("token"):
            print(
                f"🔄 Token already deployed at {existing_contracts['token']} for tweet {tweet_id}. Reusing it.")
            return existing_contracts["token"]

        print(
            f"🚀 Deploying {name} ({symbol}) with supply {supply} on {NETWORK_ID}...")

        if "deploy_token" not in self.tools:
            raise ValueError("❌ `deploy_token` tool not found in AgentKit!")

        deploy_tool = self.tools["deploy_token"]
        tx = deploy_tool.run(
            {"name": name, "symbol": symbol, "total_supply": str(supply)})

        contract_address = tx if isinstance(
            tx, str) else tx["contract_address"]
        db_manager.store_contracts(tweet_id, token_address=contract_address)

        return contract_address

    def mint_nft(self, tweet_id: str, metadata_uri: str):
        """Mints an ERC-721 NFT using AgentKit."""
        existing_contracts = db_manager.get_contracts(tweet_id)
        if existing_contracts.get("nft"):
            print(
                f"🔄 NFT already deployed at {existing_contracts['nft']} for tweet {tweet_id}. Reusing it.")
            return existing_contracts["nft"]

        name = f"AgenticNFT-{tweet_id}"
        symbol = f"AGNTC{tweet_id[-4:]}"
        print(
            f"🚀 Minting NFT {name} ({symbol}) with metadata at {metadata_uri} on {NETWORK_ID}...")

        if "deploy_nft" not in self.tools:
            raise ValueError("❌ `deploy_nft` tool not found in AgentKit!")

        deploy_nft_tool = self.tools["deploy_nft"]
        tx = deploy_nft_tool.run(
            {"name": name, "symbol": symbol, "base_uri": metadata_uri})

        contract_address = tx if isinstance(
            tx, str) else tx["contract_address"]
        db_manager.store_contracts(tweet_id, nft_address=contract_address)

        return contract_address

    def distribute_rewards(self, tweet_id: str, engagement_data: dict):
        """Distributes ERC-20 tokens to users who liked/retweeted/commented and selects one to receive the NFT."""
        contracts = db_manager.get_contracts(tweet_id)
        token_address = contracts.get("token")
        nft_address = contracts.get("nft")

        if not token_address:
            print("❌ No token deployed for this tweet.")
            return
        if not nft_address:
            print("❌ No NFT deployed for this tweet.")
            return

        if "transfer" not in self.tools:
            raise ValueError("❌ `transfer` tool not found in AgentKit!")

        transfer_tool = self.tools["transfer"]

        # ✅ Match likes with comments (only send tokens to users who both liked & commented with wallet)
        users_with_wallets = engagement_data.get(
            "comments", {})
        eligible_users = [user for user in engagement_data.get(
            "likes", []) if user in users_with_wallets]

        # ✅ Send 100 tokens to each eligible user
        for user in eligible_users:
            wallet_address = users_with_wallets[user]
            print(
                f"💰 Sending 100 tokens to {wallet_address} from {token_address}...")
            transfer_tool.run({
                "destination": wallet_address,
                "amount": "100",
                "asset_id": token_address
            })

        # ✅ Randomly select one user for the NFT
        if nft_address and eligible_users:
            selected_user = random.choice(eligible_users)
            wallet_address = users_with_wallets[selected_user]
            print(
                f"🎨 Sending NFT {nft_address} to {selected_user} ({wallet_address})...")
            transfer_tool.run({
                "destination": wallet_address,
                "amount": "1",
                "asset_id": nft_address
            })
        else:
            print("❌ No valid wallet addresses found in comments, NFT not distributed.")

        print("✅ Rewards distributed successfully.")
