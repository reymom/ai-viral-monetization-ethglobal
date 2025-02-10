import os
import re
import requests
import warnings
import replicate
from PIL import Image
from openai import OpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.agent_toolkits.load_tools import load_tools
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper
from base.cdp_wallet import WalletManager
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

warnings.simplefilter("ignore", category=FutureWarning)
load_dotenv()

# ✅ Load Image Generation Provider from Config
IMAGE_PROVIDER = os.getenv("IMAGE_GENERATION_PROVIDER", "openai").lower()

# ✅ OpenAI Client (if using DALL·E)
client = None
if IMAGE_PROVIDER == "openai":
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")
HF_MODEL = "runwayml/stable-diffusion-v1-5"


# ✅ Initialize LangChain LLM
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN"),
    temperature=0.7,
    model_kwargs={"max_length": 512},
)

# ✅ Initialize AgentKit Wallet
wallet_manager = WalletManager()

# ✅ Initialize CDP AgentKit Wrapper & Toolkit
cdp = CdpAgentkitWrapper()
cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(cdp)
cdp_tools = cdp_toolkit.get_tools()

# ✅ Load Additional AI Tools
dalle_tool = load_tools(["dalle-image-generator"])

# ✅ Combine All Tools
all_tools = cdp_tools + dalle_tool

# ✅ Agent Configuration
memory = {}
config = {"configurable": {"thread_id": "CDP AgentKit Chatbot"}}


def execute_agent_request(query: str, tool_name=None):
    """Executes a query through the AI Agent. Uses DALL·E if tool_name is specified."""
    print(f"🤖 Executing: {query}")

    if tool_name == "dalle-image-generator":
        response = client.images.generate(
            model="dall-e-2",
            prompt=query,
            n=1,
            size="1024x1024"
        )

        image_url = response.data[0].url
        return image_url
    else:
        response = llm.invoke(query)

    print(f"🔍 Agent Response: {response}")
    return response.strip()


def extract_tweet(text: str) -> str:
    """Extracts the tweet from AI-generated text by removing instructions."""
    # Match text inside quotes or remove prompt repetition
    match = re.search(r'["“](.+?)["”]', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


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


def save_image(image_url: str, filename: str = "generated_image.png") -> str:
    """Saves AI-generated image to `data/` folder only if the URL is valid."""
    print(f"📥 Attempting to save image from URL: {image_url}")

    if not image_url or not image_url.startswith("http"):
        print(f"❌ Invalid image URL: {image_url}")
        return None

    os.makedirs("data", exist_ok=True)
    image_path = os.path.join("data", filename)

    try:
        response = requests.get(image_url)
        response.raise_for_status()

        with open(image_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Image saved successfully at: {image_path}")
        return image_path

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download image: {e}")
        return None


def generate_image_huggingface(prompt):
    """Generates an image using Hugging Face's Free Stable Diffusion API with optimized settings."""
    print("🖼️ Using Hugging Face's Stable Diffusion v1.5 (Light)...")

    client = InferenceClient(model=HF_MODEL, token=HUGGINGFACE_API_KEY)

    response = client.text_to_image(
        prompt, params={"width": 384, "height": 384,
                        "num_inference_steps": 15, "guidance_scale": 5.0}
    )

    if isinstance(response, Image.Image):
        image_path = "data/generated_image.png"
        os.makedirs("data", exist_ok=True)
        response.save(image_path, format="PNG")
        print(f"✅ Image saved at: {image_path}")
        return image_path
    else:
        print(f"❌ Image generation failed: {response}")
        return None


if __name__ == "__main__":
    print("🔍 Testing AI Tweet & Image Generation...")

    raw_tweet_text = execute_agent_request(
        "Generate a viral tweet about AI, Web3, and blockchain automation with AgentKit.")
    tweet_text = extract_tweet(raw_tweet_text)
    print(f"\n📝 Generated Tweet:\n{tweet_text}")

    image_path = generate_image(
        f"Generate an AI image for this tweet: {tweet_text}")

    print("\n✅ Test completed successfully!")
