import os
from dotenv import load_dotenv

load_dotenv()

CDP_API_KEY_NAME = os.getenv("CDP_API_KEY_NAME")
CDP_API_KEY_PRIVATE_KEY = os.getenv("CDP_API_KEY_PRIVATE_KEY")
NETWORK_ID = os.getenv("NETWORK_ID", "base-sepolia")

if not CDP_API_KEY_NAME or not CDP_API_KEY_PRIVATE_KEY:
    raise ValueError(
        "❌ CDP API keys are missing. Please add them to your .env file.")
