# Immoscout Email to Telegram

This project runs as a GitHub Actions workflow to monitor a Gmail inbox for Immobilien Scout apartment notification emails and forwards relevant information to a Telegram chat via a bot.

## Features
- **Automated Gmail polling** every 15 minutes
- **Secure IMAP connection** to Gmail
- Filters and parses apartment notification emails from multiple sources
- Extracts key apartment details (price, rooms, area, location, URL)
- Sends formatted messages to Telegram with apartment information
- Marks processed emails as read to avoid duplicates
- Comprehensive logging for monitoring and debugging

## Prerequisites

### Gmail Setup
1. **Enable IMAP in Gmail**:
   - Gmail → Settings → Forwarding and POP/IMAP
   - Enable IMAP access

2. **Create an App Password** (for 2FA-enabled accounts):
   - Google Account → Security → 2-Step Verification
   - App passwords → Generate password for "Mail"
   - Use this password instead of your regular Gmail password

3. **Set up Gmail filter** (optional but recommended):
   - Gmail → Settings → Filters and Blocked Addresses → Create new filter  
   - **From:** `*@immobilienscout24.de` OR `*@immonet.de` OR `*@immowelt.de`
   - **Action:** Apply label "Apartments" for easy identification

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
2. Set up Gmail IMAP access (see Prerequisites above)
3. Add the following secrets to your GitHub repository:
   - `EMAIL_ADDRESS`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail app password
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
- **Automatic polling**: Workflow runs every 15 minutes to check for new emails
- **Manual trigger**: You can also run manually from the Actions tab
- **Automatic filtering**: Only emails from apartment websites are processed
- **Duplicate prevention**: Processed emails are marked as read to avoid reprocessing

## Configuration
- **Email Filtering**: Modify Gmail filter criteria to include other apartment websites
- **Message Format**: Customize the `format_telegram_message` function in `apartment_parser.py`
- **Polling Schedule**: Modify cron expression in `.github/workflows/email-to-telegram.yml`
- **IMAP Settings**: Adjust server/port in config if using different email provider

## Project Structure
```
├── main.py                           # Main application entry point
├── config.py                         # Configuration and environment validation
├── email_processor.py                # Gmail IMAP email processing
├── apartment_parser.py               # Email parsing and data extraction
├── telegram_bot.py                   # Telegram bot integration
├── test_utils.py                     # Mock testing utilities
├── requirements.txt                  # Python dependencies
├── .github/workflows/email-to-telegram.yml  # GitHub Actions workflow
├── .env.example                      # Environment variables template
├── .gitignore                        # Git ignore file
└── README.md                         # This file
```

## Security Notes
- Use Gmail App Passwords instead of your regular password
- Store all credentials securely in GitHub Secrets
- Enable 2FA on your Gmail account for enhanced security
- IMAP connection uses SSL/TLS encryption

## Troubleshooting

### Gmail Connection Issues
- **Authentication failed**: Verify Gmail app password is correct
- **IMAP not enabled**: Check Gmail settings → Forwarding and POP/IMAP
- **No emails found**: Check Gmail filters and spam folder

### General Issues
- Check GitHub Actions logs for detailed error messages
- Test Telegram bot token with a simple API call
- Verify the bot can send messages to your chat
- Ensure all required secrets are configured in GitHub repository

## License
This project is open source and available under the MIT License.
