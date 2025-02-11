import sqlite3
import os

DB_FILE = "data/agentkit.db"


class DatabaseManager:
    """Handles SQLite database operations for storing token/NFT contracts and other persistent data."""

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates tables for storing deployed contracts and future auth tokens."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                tweet_id TEXT PRIMARY KEY,
                token_address TEXT,
                nft_address TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_tokens (
                provider TEXT PRIMARY KEY,  -- e.g., 'twitter'
                access_token TEXT,
                refresh_token TEXT,
                expires_at INTEGER
            )
        """)
        self.conn.commit()

    def store_contracts(self, tweet_id, token_address=None, nft_address=None):
        """Stores or updates token/NFT contract addresses for a given tweet."""
        self.cursor.execute("""
            INSERT INTO contracts (tweet_id, token_address, nft_address)
            VALUES (?, ?, ?) ON CONFLICT(tweet_id)
            DO UPDATE SET 
                token_address=COALESCE(EXCLUDED.token_address, token_address),
                nft_address=COALESCE(EXCLUDED.nft_address, nft_address)
        """, (tweet_id, token_address, nft_address))
        self.conn.commit()

    def get_contracts(self, tweet_id):
        """Retrieves token and NFT addresses for a tweet."""
        self.cursor.execute(
            "SELECT token_address, nft_address FROM contracts WHERE tweet_id = ?", (tweet_id,))
        result = self.cursor.fetchone()
        if result:
            return {"token": result[0], "nft": result[1]}
        return {}

    def store_auth_token(self, provider, access_token, refresh_token, expires_at):
        """Stores or updates OAuth access and refresh tokens."""
        self.cursor.execute("""
            INSERT INTO auth_tokens (provider, access_token, refresh_token, expires_at)
            VALUES (?, ?, ?, ?) 
            ON CONFLICT(provider) 
            DO UPDATE SET access_token = ?, refresh_token = ?, expires_at = ?
        """, (provider, access_token, refresh_token, expires_at,
              access_token, refresh_token, expires_at))
        self.conn.commit()

    def get_auth_token(self, provider):
        """Retrieves the stored OAuth tokens for a given provider."""
        self.cursor.execute("""
            SELECT access_token, refresh_token, expires_at FROM auth_tokens WHERE provider = ?
        """, (provider,))
        result = self.cursor.fetchone()
        if result:
            return {"access_token": result[0], "refresh_token": result[1], "expires_at": result[2]}
        return None

    def close(self):
        """Closes database connection."""
        self.conn.close()


# ✅ Singleton instance for global use
db_manager = DatabaseManager()
