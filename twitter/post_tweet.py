import os
import requests
import tweepy
from twitter.auth import TwitterAuth
from dotenv import load_dotenv

load_dotenv()


def twitter_api():
    """Initialize Tweepy API for media upload using OAuth 1.0a."""
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN_OAUTH1')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_OAUTH1_SECRET')

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        raise ValueError(
            "❌ Missing Twitter API credentials! Check your .env file.")

    auth = tweepy.OAuthHandler(
        consumer_key, consumer_secret, access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)


def post_tweet_v2(text: str, media_ids):
    """Posts a tweet using Twitter API v2 with direct API request (instead of Tweepy)."""

    # Get OAuth 2.0 token
    auth = TwitterAuth()
    access_token = auth.get_access_token()

    if not access_token:
        raise ValueError("❌ Invalid or missing Twitter Access Token!")

    print("🐦 Posting tweet using direct API request...")

    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}
    if media_ids:
        payload["media"] = {"media_ids": media_ids}

    response = requests.post(url, json=payload, headers=headers)

    # Debug API response
    print("🔍 Twitter API Response:", response.status_code, response.text)

    if response.status_code == 201:
        tweet_data = response.json()
        print(
            f"✅ Tweet posted successfully! Tweet ID: {tweet_data['data']['id']}")
        return tweet_data["data"]["id"]
    else:
        raise Exception(
            f"❌ Error posting tweet: {response.status_code} {response.text}")


def post_tweet_with_image(text: str, image_path: str = None):
    """Posts a tweet with optional image attachment, ensuring media is uploaded first."""
    api = twitter_api()
    media_ids = []
    if image_path:
        print("📤 Uploading media to Twitter...")
        media = api.media_upload(image_path)
        media_ids.append(media.media_id_string)
        print("✅ Media uploaded successfully!")

    tweet_id = post_tweet_v2(text, media_ids)

    return tweet_id


if __name__ == "__main__":
    post_tweet_with_image("This is a test tweet with an AI-generated image!",
                          "data/futuristic_city.png")
