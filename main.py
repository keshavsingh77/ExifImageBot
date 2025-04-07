import os
from pyrogram import Client, filters
from PIL import Image, ExifTags
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot credentials from .env file
API_ID = int(os.getenv("9028935"))
API_HASH = os.getenv("208bf560e644253ff8a50a94b46fe517")
BOT_TOKEN = os.getenv("7234076217:AAEg7RVx9P_tAoJHulN90e4cqFdIZAh3AZo")

# Initialize the bot client
app = Client("exif_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_exif(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return "No EXIF data found."
        exif = {ExifTags.TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        return exif
    except Exception as e:
        return f"Error reading EXIF data: {e}"

@app.on_message(filters.command("start"))
def start_command(client, message):
    welcome_text = (
        "**👋 Hello! I'm the EXIF Bot.**\n\n"
        "📸 **How to use me:**\n"
        "• Send me an image as a file (not as a photo) to preserve the original EXIF data.\n"
        "• I'll extract and display the EXIF details with some cool emojis.\n\n"
        "Give it a try by sending an image file!"
    )
    message.reply_text(welcome_text)

@app.on_message(filters.document)
def document_handler(client, message):
    if not message.document.mime_type.startswith("image"):
        message.reply("**❌ Please send an image file as a document.**")
        return

    file_path = message.download()
    exif_details = get_exif(file_path)
    os.remove(file_path)

    if isinstance(exif_details, dict):
        header = "📸 **EXIF Details:**\n\n"
        exif_text = "\n".join(f"✨ **{key}:** {value}" for key, value in exif_details.items())
        reply_message = header + exif_text
    else:
        reply_message = f"**❌ {exif_details}**"

    message.reply(reply_message)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
