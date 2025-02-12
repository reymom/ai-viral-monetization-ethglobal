import requests
from twitter.auth import TwitterAuth
from twitter.upload_media import upload_media
from dotenv import load_dotenv

load_dotenv()


TWEET_URL = "https://api.x.com/2/tweets"


def post_tweet(access_token: str, text: str, media_ids):
    """Posts a tweet using Twitter API v2 with direct API request."""

    if not access_token:
        raise ValueError("❌ Invalid or missing Twitter Access Token!")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}
    if media_ids:
        payload["media"] = {"media_ids": media_ids}

    print("payload = ", payload)
    response = requests.post(TWEET_URL, json=payload, headers=headers)

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
    auth = TwitterAuth()
    access_token = auth.get_access_token()

    media_ids = []
    if image_path:
        media_id = upload_media(access_token, image_path)
        media_ids.append(media_id)
        print("✅ Media uploaded successfully!")

    tweet_id = post_tweet(access_token, text, media_ids)
    return tweet_id


if __name__ == "__main__":
    post_tweet_with_image(
        "This is a test tweet with an AI-generated image!",
        "data/futuristic_city.png"
    )
