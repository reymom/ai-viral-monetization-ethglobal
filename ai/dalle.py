import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def generate_image(prompt: str, output_file: str = "output.png"):
    """Generates an AI image using DALL-E and saves it to a file."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    image_url = response["data"][0]["url"]

    # Download and save the image
    os.system(f"wget -O {output_file} {image_url}")
    print(f"Image saved as {output_file}")
    return output_file


if __name__ == "__main__":
    generate_image(
        "A futuristic AI-powered Twitter bot managing crypto transactions")
