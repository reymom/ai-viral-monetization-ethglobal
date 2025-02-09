import schedule
import time
from base_token_distribution import distribute_rewards

# Define tweet ID and contract address (to be fetched dynamically in production)
TWEET_ID = "latest_tweet_id"  # Placeholder
CONTRACT_ADDRESS = "your_base_contract_address"

def scheduled_distribution():
    """Runs the token distribution every 12 hours."""
    print("Running scheduled reward distribution...")
    distribute_rewards(TWEET_ID, CONTRACT_ADDRESS)
    print("Reward distribution complete.")

# Schedule the job every 12 hours
schedule.every(12).hours.do(scheduled_distribution)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
