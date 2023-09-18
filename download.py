from telegram.ext import *
import os
import time
import re
from pytube import YouTube

#_______
def download_video(link):
    try:
        # Create a YouTube object
        yt = YouTube(link)

        # Get the highest resolution stream (stream with both audio and video)
        stream = yt.streams.get_highest_resolution()

        # Download the video
        print(f"Downloading: {yt.title}")
        title = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', yt.title)
        title = title.replace(" ","")

        stream.download(filename=f"{title}.mp4")

        print("Download complete!")
        return title

    except Exception as e:
        print(f"An error occurred: {str(e)}")
#_______


# Define the start command handler
def start_command(update, context):
    update.message.reply_text("Welcome. Please Enter the Video Link Below")


def input(update, context):
    user_message = update.message.text
    title =download_video(str(user_message))
    context.user_data["title"] = title
    update.message.reply_text("Video Downloaded. Click to /download")


def download_command(update, context):
    
    print('in download')
    title =context.user_data['title']
    print(title, "this it download_cmd")
    path = f"{title}.mp4"
    print(os.getcwd())
    video_file = open(path,"rb")
    update.message.reply_video(video=video_file)
    time.sleep(5)

    try:
    # Attempt to delete the file
        os.remove(path)
        print(f"File '{path}' has been deleted.")
    except FileNotFoundError:
        print(f"File '{path}' not found.")
    except PermissionError:
        print(f"You don't have permission to delete '{path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")









# Define the main function
def main():
    # Replace 'YOUR_TOKEN' with your actual Telegram Bot API token
    token = os.environ.get("TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("download", download_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, input))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
