# Immoscout Email to Telegram

This project runs as a GitHub Actions workflow to monitor a Gmail inbox for Immobilien Scout apartment notification emails and forwards relevant information to a Telegram chat via a bot.

## Features
- Connects to Gmail using IMAP with robust error handling
- Filters and parses Immobilien Scout apartment notification emails
- Extracts key apartment details (price, rooms, area, location, URL)
- Sends formatted messages to Telegram with apartment information
- Runs automatically on a schedule via GitHub Actions
- Comprehensive logging for monitoring and debugging

## Prerequisites

### Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Enable IMAP access in Gmail settings
3. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"

### Telegram Setup
1. Create a Telegram bot:
   - Message @BotFather on Telegram
   - Use `/newbot` command and follow instructions
   - Save the bot token
2. Get your chat ID:
   - Start a chat with your bot
   - Send any message
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

## Installation

### For GitHub Actions (Recommended)
1. Fork or clone this repository
2. Add the following secrets to your GitHub repository:
   - `GMAIL_USER`: Your Gmail address
   - `GMAIL_APP_PASSWORD`: Your Gmail App Password
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### For Local Testing
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .\.venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your credentials
5. Run locally: `python main.py`

## Usage
- The GitHub Actions workflow runs every 15 minutes automatically
- You can also trigger it manually from the Actions tab
- The script processes only unread emails from Immobilien Scout
- Successfully processed emails are marked as read

## Configuration
- **Schedule**: Modify the cron expression in `.github/workflows/email-to-telegram.yml`
- **Email Sources**: Update the search criteria in `main.py` to include other senders
- **Message Format**: Customize the `format_telegram_message` function

## Project Structure
```
├── main.py                           # Main application entry point
├── config.py                         # Configuration and environment validation
├── email_processor.py                # Gmail IMAP operations
├── apartment_parser.py               # Email parsing and data extraction
├── telegram_bot.py                   # Telegram bot integration
├── test_utils.py                     # Mock testing utilities
├── requirements.txt                  # Python dependencies
├── .github/workflows/email-to-telegram.yml  # GitHub Actions workflow
├── .env.example                      # Environment variables template
├── .env.test                         # Test mode configuration
├── setup.ps1 / setup.sh              # Setup scripts for Windows/Unix
├── .gitignore                        # Git ignore file
├── .venv/                            # Virtual environment (not committed)
└── README.md                         # This file
```

## Security Notes
- Never commit credentials to the repository
- Use GitHub Secrets for sensitive information
- The `.env` file is ignored by Git for local testing
- App passwords are more secure than your main Gmail password

## Troubleshooting
- Check GitHub Actions logs for detailed error messages
- Ensure all environment variables are properly set
- Verify Gmail IMAP is enabled and App Password is correct
- Test Telegram bot token with a simple API call

## License
This project is open source and available under the MIT License.
