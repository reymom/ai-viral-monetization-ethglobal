import os
import requests
import time
import base64
import random
import string
import tweepy
from urllib.parse import urlencode
from dotenv import load_dotenv, set_key

env_path = '.env'
load_dotenv(dotenv_path=env_path)


class TwitterAuth:
    """Handles Twitter API authentication using OAuth 2.0 with Refresh Token Flow."""

    def __init__(self):
        self.client_id = os.getenv("TWITTER_CLIENT_ID")
        self.client_secret = os.getenv("TWITTER_CLIENT_SECRET")
        self.refresh_token = os.getenv("TWITTER_REFRESH_TOKEN")
        self.redirect_uri = os.getenv("TWITTER_REDIRECT_URI")
        self.access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.token_expiry = float(os.getenv("TWITTER_TOKEN_EXPIRY", 0))
        self.code_verifier = None

    def generate_auth_url(self):
        """Generate the authorization URL to obtain the authorization code."""
        state = ''.join(random.choices(
            string.ascii_letters + string.digits, k=32))
        code_challenge = ''.join(random.choices(
            string.ascii_letters + string.digits, k=32))
        self.code_verifier = code_challenge

        auth_url = "https://twitter.com/i/oauth2/authorize"
        query_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "tweet.read tweet.write like.read users.read offline.access",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "plain",
        }
        return f"{auth_url}?{urlencode(query_params, safe=':/')}"

    def get_access_token(self, auth_code):
        """Exchange authorization code for access token."""
        url = "https://api.twitter.com/2/oauth2/token"
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = urlencode({
            "grant_type": "authorization_code",
            "code": auth_code,
            "code_verifier": self.code_verifier,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        })

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data.get(
                "refresh_token", self.refresh_token)  # Store the refresh token
            self.token_expiry = time.time() + token_data.get("expires_in",
                                                             7200)  # Default: 2 hours

            # Save the refresh token
            os.environ["TWITTER_REFRESH_TOKEN"] = self.refresh_token

            print("✅ Access token obtained successfully.")
            set_key(env_path, "TWITTER_ACCESS_TOKEN", self.access_token)
            set_key(env_path, "TWITTER_REFRESH_TOKEN", self.refresh_token)
            return self.access_token
        else:
            raise Exception(f"Failed to obtain access token: {response.text}")

    def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        if not self.refresh_token:
            raise Exception("No refresh token available. Reauthorize the app.")

        if time.time() < self.token_expiry - 60:
            print("🔄 Token still valid, skipping refresh.")
            return self.access_token

        url = "https://api.twitter.com/2/oauth2/token"
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = urlencode({
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        })

        response = requests.post(url, headers=headers, data=data)
        print(response)

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.refresh_token = token_data.get(
                "refresh_token", self.refresh_token)
            self.token_expiry = time.time() + token_data.get("expires_in", 7200)
            print(
                f"🔄 Access token refreshed! Expires in {token_data['expires_in']} seconds.")

            print("🔄 Access token refreshed.")
            set_key(env_path, "TWITTER_ACCESS_TOKEN", self.access_token)
            set_key(env_path, "TWITTER_REFRESH_TOKEN", self.refresh_token)
            set_key(env_path, "TWITTER_TOKEN_EXPIRY", str(self.token_expiry))
            return self.access_token
        else:
            raise Exception(f"Failed to refresh access token: {response.text}")


def get_twitter_client():
    """Creates an authenticated Tweepy client with refreshed access token."""
    auth = TwitterAuth()
    auth.refresh_access_token()

    return tweepy.Client(auth.access_token)


if __name__ == "__main__":
    print("🔍 Checking Twitter API authentication...")

    auth = TwitterAuth()
    expiry_timestamp = auth.token_expiry
    print(
        f"expires at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiry_timestamp))}")
    auth.refresh_access_token()
