import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_tweet(prompt: str = "AI and blockchain innovation"):
    """Generates a tweet based on a given topic."""
    print("📝 Generating AI-powered tweet...")

    response = client.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI specialized in writing engaging tweets under 280 characters."},
            {"role": "user", "content": f"Write an engaging tweet about {prompt} with hashtags and emojis."}
        ],
        max_tokens=100
    )

    tweet_text = response.choices[0].message.content.strip()

    if len(tweet_text) > 280:
        print("⚠️ Tweet too long, truncating...")
        # Truncate to fit within 280 characters
        tweet_text = tweet_text[:277] + "..."

    print(f"✅ Generated Tweet: {tweet_text}")
    return tweet_text


if __name__ == "__main__":
    topic = input("Enter tweet topic (default: AI and blockchain innovation): ").strip(
    ) or "AI and blockchain innovation"
    generate_tweet(topic)
