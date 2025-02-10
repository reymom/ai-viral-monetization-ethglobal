import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def generate_image(prompt: str, output_file: str = "data/output.png"):
    """Generates an AI image using DALL-E and saves it to a file."""
    print("🎨 Generating AI Image...")

    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response.data[0].url

    output_dir = os.path.dirname(output_file)
    if output_dir:  # ✅ Prevents FileNotFoundError
        os.makedirs(output_dir, exist_ok=True)

    # ✅ Download and save the image
    image_data = requests.get(image_url).content
    with open(output_file, "wb") as img_file:
        img_file.write(image_data)

    print(f"✅ Image saved at: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_image(
        "A futuristic AI-powered Twitter bot managing crypto transactions")
