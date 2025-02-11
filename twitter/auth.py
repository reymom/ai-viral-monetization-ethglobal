import os
import requests
import time
import base64
import random
import string
from urllib.parse import urlencode
from database.db_manager import db_manager
from dotenv import load_dotenv

load_dotenv()


TWITTER_CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
TWITTER_REDIRECT_URI = os.getenv("TWITTER_REDIRECT_URI")
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"


class TwitterAuth:
    """Handles Twitter API authentication using OAuth 2.0 with Refresh Token Flow."""

    def __init__(self):
        self.tokens = db_manager.get_auth_token("twitter")
        self.code_verifier = None

    def auth_headers(self):
        credentials = f"{TWITTER_CLIENT_ID}:{TWITTER_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        return {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def get_access_token(self):
        """Retrieves the stored access token or fetches a new one if expired."""
        self.tokens = db_manager.get_auth_token("twitter")

        if not self.tokens:
            raise ValueError(
                "❌ No stored Twitter tokens. Run authentication first!")

        access_token = self.tokens["access_token"]
        expires_at = self.tokens["expires_at"]

        if expires_at and time.time() > expires_at - 60:
            print("🔄 Access token expired, refreshing...")
            return self.refresh_access_token()

        print("🔄 Token still valid, skipping refresh.")
        return access_token

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
            "client_id": TWITTER_CLIENT_ID,
            "redirect_uri": TWITTER_REDIRECT_URI,
            "scope": "tweet.read tweet.write like.read users.read offline.access",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "plain",
        }
        return f"{auth_url}?{urlencode(query_params, safe=':/')}"

    def exchange_access_token(self, auth_code):
        """Exchange authorization code for access token."""

        data = urlencode({
            "grant_type": "authorization_code",
            "code": auth_code,
            "code_verifier": self.code_verifier,
            "redirect_uri": TWITTER_REDIRECT_URI,
            "client_id": TWITTER_CLIENT_ID,
        })

        response = requests.post(
            TOKEN_URL, headers=self.auth_headers(), data=data)

        if response.status_code == 200:
            token_data = response.json()
            new_access_token = token_data["access_token"]

            self.save_tokens(new_access_token,
                             token_data["refresh_token"], token_data.get("expires_in", 7200))

            print("✅ Access token obtained successfully.")
            self.tokens = db_manager.get_auth_token("twitter")
            return new_access_token
        else:
            raise Exception(f"Failed to obtain access token: {response.text}")

    def refresh_access_token(self):
        """Refresh the access token using the refresh token."""
        self.tokens = db_manager.get_auth_token("twitter")
        print("self.tokens = ", self.tokens)

        if not self.tokens:
            raise ValueError("❌ No refresh token found. Authenticate first!")

        if time.time() < self.tokens["expires_at"] - 60:
            print("🔄 Token still valid, skipping refresh.")
            return self.tokens["access_token"]

        refresh_token = self.tokens["refresh_token"]
        data = urlencode({
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": TWITTER_CLIENT_ID,
        })

        response = requests.post(
            TOKEN_URL, headers=self.auth_headers(), data=data)

        if response.status_code == 200:
            token_data = response.json()
            new_access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 7200)

            self.save_tokens(new_access_token,
                             token_data["refresh_token"], expires_in)

            expires_at = time.time() + expires_in
            print(f"🔄 Access token refreshed! Expires at {expires_at}")
            return new_access_token
        else:
            raise Exception(f"Failed to refresh access token: {response.text}")

    def save_tokens(self, access_token, refresh_token, expires_in):
        """Saves new tokens after the first authentication."""
        expires_at = int(time.time()) + expires_in
        db_manager.store_auth_token(
            "twitter", access_token, refresh_token, expires_at)
        print(f"✅ Tokens stored in database. Access expires at {expires_at}")


if __name__ == "__main__":
    print("🔍 Checking Twitter API authentication...")

    auth = TwitterAuth()
    auth.refresh_access_token()
