import os
import re
import traceback
import warnings
import replicate
from io import BytesIO
from PIL import Image
from openai import OpenAI
from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

warnings.simplefilter("ignore", category=FutureWarning)
load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
IMAGE_PROVIDER = os.getenv("IMAGE_GENERATION_PROVIDER", "openai").lower()


def execute_agent_request(query: str):
    """Executes a query through the AI Agent and extracts the response correctly."""
    print(f"🤖 Executing: {query}")

    HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
    if LLM_PROVIDER == "huggingface":
        llm_client = HuggingFaceEndpoint(
            repo_id=HF_MODEL,
            task="text-generation",
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
            temperature=0.9,
            max_new_tokens=280,
            do_sample=True,
            top_p=0.85,
            typical_p=0.9,
            model_kwargs={
                "frequency_penalty": 0.7,
                "presence_penalty": 0.6,
            }
        )
    elif LLM_PROVIDER == "openai":
        llm_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        raise ValueError(
            "❌ Invalid LLM_PROVIDER. Choose either 'openai' or 'huggingface'.")

    response = llm_client.invoke(query) if LLM_PROVIDER == "huggingface" else llm_client.completions.create(
        model="gpt-4-turbo",
        prompt=query,
        max_tokens=280,
        temperature=0.9
    ).choices[0].text.strip()

    if isinstance(response, dict):
        response_text = response.get("generated_text", "").strip()
    elif isinstance(response, list) and len(response) > 0:
        response_text = response[0].get("generated_text", "").strip()
    else:
        response_text = str(response).strip()

    # print("\n🚨 RAW LLM RESPONSE 🚨\n", response_text, "\n")

    return response_text


def extract_tweet(response: str) -> str:
    """Extracts the tweet from AI-generated text using regex."""
    match = re.search(r'Tweet:\s*["“”`]?(.+?)["“”`]?\s*$',
                      response, re.DOTALL | re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Fallback: Take last non-empty line as tweet
    lines = response.strip().split("\n")
    for line in reversed(lines):
        if line.strip():
            return line.strip()

    tweet = response.strip()
    if len(tweet) > 280:
        print(f"⚠️ Tweet is too long ({len(tweet)} chars). Truncating...")
        tweet = tweet[:277] + "..."

    return tweet


def generate_image(prompt: str):
    """Generates an AI image using the selected provider."""
    print(f"🎨 Generating AI Image using {IMAGE_PROVIDER.upper()}...")

    if IMAGE_PROVIDER == "openai":
        return generate_image_openai(prompt)
    elif IMAGE_PROVIDER == "replicate":
        return generate_image_replicate(prompt)
    else:
        return generate_image_huggingface(prompt)


def generate_image_openai(prompt: str):
    """Generates an AI image using DALL·E 2."""
    print("🖼️ Using OpenAI's DALL·E 2...")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url
    print(f"✅ OpenAI Image URL: {image_url}")
    return image_url


def generate_image_replicate(prompt: str):
    """Generates an AI image using Replicate (Stable Diffusion)."""
    print("🖼️ Using Replicate's Stable Diffusion...")

    replicate_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

    output = replicate_client.run(
        "lightweight-ai/model3_4:4b6b4c774ae7db5b833c900f791a8741aae3614d8f5b77e0be0c897d1c766feb",
        input={"prompt": prompt, "width": 1024, "height": 1024}
    )

    if not output:
        print("❌ Replicate did not return an image URL.")
        return None

    image_url = output[0]
    print(f"✅ Replicate Image URL: {image_url}")
    return image_url


def generate_image_huggingface(prompt):
    """Generates an image using Hugging Face's Free Stable Diffusion API with optimized settings."""

    base_model = "stabilityai/stable-diffusion-xl-base-1.0"
    refiner_model = "stabilityai/stable-diffusion-xl-refiner-1.0"

    params = {
        "width": 1152,
        "height": 1152,
        "num_inference_steps": 40,
        "guidance_scale": 8,
        "negative_prompt": (
            "blurry, distorted, deformed, unnatural, worst quality, artifacts, pixelated, low resolution, "
            "extra limbs, missing fingers, mutated faces, bad anatomy"
        )
    }

    client = InferenceClient(
        model=base_model, token=HUGGINGFACEHUB_API_TOKEN, timeout=180)
    try:
        response = client.text_to_image(
            prompt, params=params
        )

        if isinstance(response, Image.Image):
            image = response
        elif isinstance(response, bytes):
            image = Image.open(BytesIO(response))
        else:
            print(f"❌ Image generation failed: {response}")
            return None

        os.makedirs("data", exist_ok=True)
        base_image_path = "data/generated_image_base.png"
        image.save(base_image_path, format="PNG")
        print(f"✅ Image saved at: {base_image_path}")

        # ✅ Step 2: Optionally refine the image
        image_bytes = BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)
        client = InferenceClient(
            model=refiner_model, token=HUGGINGFACEHUB_API_TOKEN)
        response = client.image_to_image(
            image=image_bytes.getvalue(), prompt=prompt)
        if isinstance(response, bytes):
            refined_image = Image.open(BytesIO(response))
        elif isinstance(response, Image.Image):
            refined_image = response
        else:
            print(
                f"❌ Unexpected response type from REFINER model: {type(response)}")
            return base_image_path

        refined_image_path = "data/generated_image.png"
        refined_image.save(refined_image_path, format="PNG")
        print(f"✅ Refined Image saved at: {refined_image_path}")
        return refined_image_path

    except Exception as e:
        print(f"❌ Image generation error: {e}")
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("🔍 Testing AI Tweet & Image Generation...")

    prompt = (
        "Generate a high-impact, viral tweet (under 280 characters) "
        "about AI, Web3, and blockchain automation with AgentKit. "
        "Focus on:\n"
        "- The power of AI-driven onchain automation\n"
        "- NFTs & ERC-20 rewards for engagement\n"
        "- How AgentKit + Base enable decentralized monetization\n"
        "- Tagging @coinbaseDev, @BuildOnBase, and any key partners\n\n"
        "Output format: 'Tweet: <your tweet here>'"
    )

    raw_tweet_text = execute_agent_request(prompt)
    tweet_text = extract_tweet(raw_tweet_text)
    print(f"\n📝 Generated Tweet:\n{tweet_text}")

    tweet_text = "🤖+🔗+🌐=AI-driven #Web3 revolution! AgentKit's onchain automation just won @coinbaseDev's hackathon! 🏆 NFT & ERC-20 rewards for engagement, thanks to @BuildOnBase! Decentralized monetization is here! 🚀 Beyond hackathons, imagine AI-managed DAOs & smart contracts! 🤩 #AI #Blockchain #Web3"
    image_path = generate_image(
        f"Generate an AI image for this tweet: {tweet_text}")
    print("\n✅ Test completed successfully!")
