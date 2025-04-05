import os
from pyrogram import Client, filters
from PIL import Image, ExifTags

# Bot credentials (keep these secure)
API_ID = 16016703
API_HASH = "2e661b4ea5fa6d75640f12ea09f1c3a9"
BOT_TOKEN = "7063814310:AAERF6vLC44G-Pgu3hBn3xb_M04e-9uQ3xs"

# Initialize the bot client
app = Client("exif_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_exif(file_path):
    """
    Open an image file and extract its EXIF data.
    """
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return "No EXIF data found."
        exif = {}
        for tag, value in exif_data.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            exif[decoded] = value
        return exif
    except Exception as e:
        return f"Error reading EXIF data: {e}"

@app.on_message(filters.command("start"))
def start_command(client, message):
    """
    Respond to the /start command with a welcome message and instructions.
    """
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
    """
    Process image files sent as documents to extract and display EXIF data.
    """
    if not message.document.mime_type.startswith("image"):
        message.reply("**❌ Please send an image file as a document.**")
        return

    # Download the file to a temporary location
    file_path = message.download()
    exif_details = get_exif(file_path)
    
    # Remove the downloaded file after processing
    os.remove(file_path)
    
    # Format the EXIF details with an emoji per line
    if isinstance(exif_details, dict):
        header = "📸 **EXIF Details:**\n\n"
        exif_text = "\n".join(f"✨ **{key}:** {value}" for key, value in exif_details.items())
        reply_message = header + exif_text
    else:
        reply_message = f"**❌ {exif_details}**"

    # Send the formatted reply to the user
    message.reply(reply_message)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()