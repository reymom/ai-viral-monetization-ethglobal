import re
import requests
from twitter.auth import TwitterAuth


TWITTER_API_URL = "https://api.twitter.com/2"


def extract_wallet_address(text):
    """Extracts a valid wallet address (Ethereum/Base format) from a comment."""
    match = re.search(r"0x[a-fA-F0-9]{40}",
                      text)  # Ethereum/Base address format
    return match.group(0) if match else None


def get_tweet_engagement(tweet_id):
    """Fetches users who liked, retweeted, and commented with wallet addresses using direct API requests."""
    auth = TwitterAuth()
    access_token = auth.get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # ✅ Get users who liked the tweet
    likes_url = f"{TWITTER_API_URL}/tweets/{tweet_id}/liking_users"
    likes_response = requests.get(likes_url, headers=headers)

    if likes_response.status_code == 200:
        likes_data = likes_response.json()
        liking_users = [user["username"]
                        for user in likes_data.get("data", [])]
    else:
        print(f"❌ Failed to fetch likes: {likes_response.text}")
        liking_users = []

    # ✅ Get tweet replies (comments)
    comments = {}
    search_url = f"{TWITTER_API_URL}/tweets/search/recent"
    query_params = {
        "query": f"conversation_id:{tweet_id} -is:retweet",
        "expansions": "author_id",
        "tweet.fields": "author_id,text",
        "user.fields": "username"
    }

    search_response = requests.get(
        search_url, headers=headers, params=query_params)

    if search_response.status_code == 200:
        response_data = search_response.json()
        users_map = {user["id"]: user["username"]
                     for user in response_data.get("includes", {}).get("users", [])}

        for tweet in response_data.get("data", []):
            wallet_address = extract_wallet_address(tweet["text"])
            if wallet_address and tweet["author_id"] in users_map:
                comments[users_map[tweet["author_id"]]] = wallet_address
    else:
        print(f"❌ Failed to fetch comments: {search_response.text}")

    return {
        "likes": liking_users,
        "comments": comments
    }


if __name__ == "__main__":
    tweet_id = input("Enter tweet ID: ").strip()
    engagement = get_tweet_engagement(tweet_id)
    print("\n📊 Engagement Summary:")
    print("-" * 50)
    print(f"👍 Liked by: {engagement['likes']}")
    print(f"💬 Comments with wallet addresses: {engagement['comments']}")
    print("-" * 50)
