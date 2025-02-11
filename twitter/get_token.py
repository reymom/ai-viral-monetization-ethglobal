from twitter.auth import TwitterAuth

if __name__ == "__main__":
    auth = TwitterAuth()

    # Step 1: Get Authorization URL
    print("🔗 Visit this URL to authenticate:")
    print(auth.generate_auth_url())

    # Step 2: Exchange Authorization Code for Access Token
    auth_code = input("\nEnter the authorization code from Twitter: ").strip()
    access_token = auth.exchange_access_token(auth_code)
