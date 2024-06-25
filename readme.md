# Telegram YouTube Video Downloader Bot

This repository contains a Telegram bot for downloading YouTube videos and uploading them to Google Drive if the size exceeds 40 MB.

## Features

- **Download YouTube Videos**: Download the best available quality of YouTube videos.
- **Upload to Google Drive**: Upload videos larger than 40 MB to Google Drive and share the download link.

## Setup

### Prerequisites

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Google API Client](https://developers.google.com/drive/api/v3/quickstart/python)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/legeRise/telebot.git
    ```

   ```bash
     cd telebot
    ```

2. **Create a virtual environment**
   
    ```bash
    python -m venv venv
     ```


3. **Activate the virtual environment**
   
    ```bash
    venv\scripts\activate
    ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    
5. **Set up environment variables**:
    - `TOKEN`: Your Telegram bot token.
    - `uploader_service_account.json`: Path to your Google Service Account JSON file.
    - `DRIVE_FOLDER_ID`: Google Drive folder ID where videos will be uploaded.

6. **Run the bot**:
    ```bash
    python code.py
    ```

## Usage

1. **Start the bot**: Send `/start` to the bot.
2. **Provide YouTube link**: Enter the YouTube video link you want to download.
3. **Download video**: If the video is less than 40 MB, it will be sent directly via Telegram.
4. **Upload to Google Drive**: If the video is more than 40 MB, a Google Drive download link will be provided.

## Files

- `code.py`: Main script for the Telegram bot
