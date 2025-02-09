from twitter.auth import get_twitter_client
import re


def extract_wallet_address(text):
    """Extracts a valid wallet address (Ethereum/Base format) from a comment."""
    match = re.search(r"0x[a-fA-F0-9]{40}",
                      text)  # Ethereum/Base address format
    return match.group(0) if match else None


def get_tweet_engagement(tweet_id):
    """Fetches users who liked, retweeted, and commented with wallet addresses."""
    client = get_twitter_client()

    # Get users who liked the tweet
    # likes = client.get_liking_users(id=tweet_id)
    # liking_users = [user.username for user in likes.data] if likes.data else []

    # Get tweet replies (comments)
    comments = {}
    response = client.search_recent_tweets(
        query=f"conversation_id:{tweet_id} -is:retweet",
        expansions="author_id",
        tweet_fields=["author_id", "text"]
    )

    if response.data:
        for tweet in response.data:
            wallet_address = extract_wallet_address(tweet.text)
            if wallet_address:
                comments[tweet.author_id] = wallet_address

    return {
        # "likes": liking_users,
        "comments": comments
    }


if __name__ == "__main__":
    tweet_id = input("Enter tweet ID: ").strip()
    engagement = get_tweet_engagement(tweet_id)
    print(f"📊 Engagement stats: {engagement}")
