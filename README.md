# Tik8 Bot

Tik8 Bot is a Telegram bot designed to help users implement the Tik8 study method. It facilitates structured review schedules for better learning retention by scheduling lessons over consecutive days and additional intervals.

## General Overview

Tik8 Bot assists users in managing their study tasks using the Tik8 method, where small parts of lessons are reviewed for 8 consecutive days. Users can also set additional review intervals (e.g., 15th and 30th day) for further reinforcement.


## User Interaction

Tik8 Bot is interacted with via Telegram. Users can utilize the following commands:

- **/start:** Initiates interaction with the bot, providing a welcome message or access instructions.
- **/today <worksheet_name>:** Displays tasks scheduled for today from the specified Google Sheets worksheet.
- **/lessons:** Lists all lessons from the user's Google Sheets.

**New feature ideas are coming soon!**

## Setup and Configuration

To set up Tik8 Bot, follow these steps:

1. **Create Telegram Bot:**
   - Create a bot in Telegram using the BotFather and obtain the bot token.
   - Put the bot token in the `TOKEN` variable in the `const.py` file.

2. **Enable Google Sheets API:**
   - Enable the Google Sheets API for your project in the Google Cloud Console.
   - Download the `client_secret.json` file and place it in the app folder.

3. **Grant Access to Google Sheet:**
   - Grant access to the desired Google Sheet to the service account associated with the `client_secret.json` file.
   - Ensure that the service account has appropriate permissions to read from the Google Sheet.

4. **Complete `const.py` File:**
   - Provide necessary configurations such as Telegram bot token, allowed user IDs, and Google Sheet names in the `const.py` file.

5. **Run the Docker Compose:**
   - Execute the Docker Compose file to build and run the application container.

For any problems or talks, I'm available at **<u>hajibeygi.armin@gmail.com</u>** ^^