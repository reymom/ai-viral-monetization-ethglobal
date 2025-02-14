import requests
import time
import os
from twitter.auth import TwitterAuth


UPLOAD_URL = "https://api.x.com/2/media/upload"


def upload_media(access_token, image_path):
    """Uploads media to Twitter using API v2 chunked upload and returns media ID."""
    # ✅ Step 1: INIT - Initialize upload session
    media_id = init_upload(access_token, image_path)

    # ✅ Step 2: APPEND - Upload the file
    append_media(access_token, media_id, image_path)

    # ✅ Step 3: FINALIZE - Complete the upload
    return finalize_upload(access_token, media_id)


def init_upload(access_token, image_path):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    init_data = {
        "command": "INIT",
        "media_type": "image/png",
        "total_bytes": os.path.getsize(image_path),
        "media_category": "tweet_image"
    }

    print("📤 Initializing media upload...")
    response = requests.post(
        UPLOAD_URL, data=init_data, headers=headers)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"❌ Failed to INIT upload: {response.text}")

    media_id = response.json()["data"].get("id")
    print(f"✅ INIT successful! Media ID: {media_id}")
    return media_id


def append_media(access_token, media_id, image_path):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    with open(image_path, "rb") as media_file:
        files = {
            "media": (image_path, media_file, "application/octet-stream")
        }
        data = {
            "command": "APPEND",
            "media_id": media_id,
            "segment_index": "0",
        }

        response = requests.post(
            UPLOAD_URL, headers=headers, files=files, data=data)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"❌ Failed to APPEND media: {response.text}")

    print("✅ Media upload chunk appended successfully!")


def finalize_upload(access_token, media_id):
    """Finalizes media upload and checks processing status if required."""

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "command": "FINALIZE",
        "media_id": media_id
    }

    print("📤 Finalizing media upload...")
    response = requests.post(
        UPLOAD_URL, data=data, headers=headers)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(
            f"❌ Failed to FINALIZE upload: {response.status_code} {response.text}")

    response = response.json()

    # ✅ Check if async processing is required
    if "processing_info" in response["data"]:
        print("⏳ Media processing in progress, polling STATUS...")
        return check_media_status(access_token, media_id)

    print("✅ Media FINALIZED and ready for use!")
    return response["data"]["id"]


def check_media_status(access_token, media_id):
    """Polls the media processing status"""
    status_url = f"{UPLOAD_URL}?command=STATUS&media_id={media_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    while True:
        response = requests.get(status_url, headers=headers)

        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f"❌ Failed to check STATUS: {response.text}")

        status_data = response.json()
        state = status_data.get("processing_info", {}
                                ).get("state", "succeeded")

        if state == "succeeded":
            print("✅ Media processing complete!")
            return media_id
        elif state == "failed":
            raise Exception("❌ Media processing failed.")

        wait_time = status_data.get(
            "processing_info", {}).get("check_after_secs", 5)
        print(
            f"⏳ Media processing in progress... Checking again in {wait_time} seconds.")
        time.sleep(wait_time)


if __name__ == "__main__":
    auth = TwitterAuth()
    access_token = auth.get_access_token()
    media_id = upload_media(access_token, "data/futuristic_city.png")
