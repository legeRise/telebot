
#____________________________________________Required Imports____________________________________________________________________

# for downloading
import os
import time
import re
from yt_dlp import YoutubeDL

time.sleep(5)

# for telegram Bot
from telegram.ext import *

# for uploading to google drive
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account


#______________________________________________Functions___________________________________________________________________


# For Downloading age restricted videos

def start_download(url,title):
    ydl_opts = {
    'format': 'best',  # Choose the best available quality
    'outtmpl': f"{title}.mp4",  # Output file name and format
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)
    

#____________________________________________________________________
# get mb_size of video that has been downloaded 

def get_video_size(video_path):
    try:
        file_size_bytes = os.path.getsize(video_path)
        file_size_mb = file_size_bytes / (1024 * 1024)
        print(f"Video size: {file_size_mb:.2f} MB")
        return round(file_size_mb, 2)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

#_____________________________Function to upload video to google drive________________________________________________________________
def upload_to_gdrive(title, file_path):
    # Path to your service account JSON key file
    service_account_file = os.environ.get("uploader_service_account.json")
    scopes = ['https://www.googleapis.com/auth/drive']

    # Authenticate using service account credentials
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)

    # Create Google Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)

    # Find the folder ID of the folder you shared with the service account
    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    print(folder_id)

    # Create a media file upload instance
    media = MediaFileUpload(file_path, mimetype='video/mp4')

    # Create a file metadata
    file_metadata = {
        'name': title,
        'parents': [folder_id]
    }

    # Upload the file to Google Drive
    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Get the file ID
    file_id = uploaded_file.get('id')

    # Construct the full link to the uploaded file
    full_link = f"https://drive.google.com/uc?id={file_id}"

    print("File uploaded successfully!")
    return full_link


#_______________________Download Video in the directory of the bot___________________________________________________________________________________________________
def download_video(link):
    print("Downloading video...")
    try:
        # Create a yt-dlp instance
        ydl_opts = {
            'format': 'best',  # Start with the best available format     
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            if 'formats' in info_dict:
                available_formats = info_dict['formats']
                print("These are the available formats: ",available_formats)

                # Filter out format entries without a 'height' attribute
                valid_formats = [fmt for fmt in available_formats if fmt.get('height') is not None]

                if valid_formats:
                    # Find the highest available resolution stream
                    highest_resolution_stream = max(valid_formats, key=lambda x: x['height'])
                    format_resolution = highest_resolution_stream.get('resolution', 'N/A')
                    format_note = highest_resolution_stream.get('format_note', 'N/A')
                else:
                    print("No valid streams available for this video.")
                    return None
                
                title = re.sub(r'[^a-zA-Z0-9]', '', str(info_dict['title']))
                title = title.replace(" ","")
                print(f"Downloading video: {info_dict['title']} ({format_resolution} | {format_note})")
                print(title,"my title is this ")
                start_download(link,title)  # Download the video
                print("Download complete!")
                return title
            else:
                print("No streams available for this video.")
                return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")


#__________________________________________________________________________________________________________________
#_____________________________________ TELEGRAM YT VIDEO DOWNLOADER BOT____________________________________________
#__________________________________________________________________________________________________________________


# Define the start command handler
def start_command(update, context):  
    update.message.reply_text("Please Enter the Video Link Below")
    
# Takes video link as input and initiates video downloading in bot directory by using download_video function
def input(update, context):
    # check if link is valid or not
    link_validater = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$')
    
    link = update.message.text
    is_valid_link =link_validater.match(link)
    if not is_valid_link:
        update.message.reply_text("Invalid Link")
        start_command(update,context)

    # initiate video download
    title =download_video(str(link))
    print("line no 225 - title received",title)
    time.sleep(5)
    context.user_data["title"] = title
    print("line no 228 the size of the video is: ",get_video_size(f"/work/{title}.mp4"))
    context.user_data["size"] = get_video_size(f"/work/{title}.mp4")
    # send message to user
    update.message.reply_text("Video Downloaded. Click to /download")


# Uploads video to user's chat or google drive(if size is greater than 40 MB)
def download_command(update, context):
    print(context.user_data["size"])
    if context.user_data["size"]  <= 40:

        title =context.user_data['title']
        print("title",title,'going to  upload to telegram')
        path = f"{title}.mp4"
        print(os.getcwd())
        video_file = open(path,"rb")
        update.message.reply_video(video=video_file)
        time.sleep(5)


    else:
        title = context.user_data["title"]
        print("title",title,'going to  upload to drive')
        path = f"{title}.mp4"
        print(os.getcwd())
        link =upload_to_gdrive(title,path)
        update.message.reply_text(f" Since the video was too big to be sent here. We have uploaded it to google drive. Here is the download link {link} ")

    
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
    



# Starts and controls the bot
def main():
    
    token = os.environ.get("TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register a command handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("download", download_command))

    # handles user input to the bot
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, input))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()