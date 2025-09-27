# Immoscout Email to Telegram

This project runs as a GitHub Actions workflow to monitor a Gmail inbox for Immobilien Scout apartment notification emails and forwards relevant information to a Telegram chat via a bot.

## Features
- **Instant email processing** via Gmail forwarding to GitHub Issues
- **No Gmail credentials required** in GitHub Actions
- Filters and parses Immobilien Scout apartment notification emails
- Extracts key apartment details (price, rooms, area, location, URL)
- Sends formatted messages to Telegram with apartment information
- Triggered instantly when new emails arrive (no polling delays)
- Comprehensive logging for monitoring and debugging

## Prerequisites

### Email Forwarding Setup
1. **Set up Gmail forwarding**:
   - Gmail → Settings → Forwarding and POP/IMAP
   - Add forwarding address: `marta-pekar+immoscout-email-to-telegram@users.noreply.github.com`
   - Verify the forwarding address via email confirmation

2. **Create Gmail filter**:
   - Gmail → Settings → Filters and Blocked Addresses → Create new filter
   - **From:** `*@immobilienscout24.de`
   - **Action:** Forward to your GitHub repository email
   - This ensures only apartment emails trigger the workflow

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
2. Set up email forwarding (see Prerequisites above)
3. Add the following secrets to your GitHub repository:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID

**Note:** No Gmail credentials needed! Email forwarding handles authentication automatically.

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
- **Instant processing**: Workflow triggers immediately when Immobilien Scout sends email
- **Manual trigger**: You can also run manually from the Actions tab
- **Automatic filtering**: Only emails from Immobilien Scout domains are processed
- **Email audit trail**: Forwarded emails appear as GitHub Issues for tracking

## Configuration
- **Email Filtering**: Modify Gmail filter criteria to include other senders
- **Message Format**: Customize the `format_telegram_message` function in `apartment_parser.py`
- **Issue Processing**: Adjust keyword detection in `github_email_processor.py`
- **Backup Schedule**: Modify cron expression if you want to keep polling as backup

## Project Structure
```
├── main.py                           # Main application entry point
├── config.py                         # Configuration and environment validation
├── github_email_processor.py         # GitHub Issues email processing
├── apartment_parser.py               # Email parsing and data extraction
├── telegram_bot.py                   # Telegram bot integration
├── test_utils.py                     # Mock testing utilities
├── requirements.txt                  # Python dependencies
├── .github/workflows/email-to-telegram.yml  # GitHub Actions workflow
├── EMAIL_FORWARDING_SETUP.md         # Detailed email forwarding guide
├── .env.example                      # Environment variables template
├── .env.test                         # Test mode configuration
├── .gitignore                        # Git ignore file
└── README.md                         # This file
```

## Security Notes
- **No Gmail credentials needed** - email forwarding handles authentication
- Use GitHub Secrets for Telegram bot credentials only
- Email forwarding is more secure than storing email passwords
- All email content is processed through GitHub's secure infrastructure

## Troubleshooting

### Email Forwarding Issues
- **Emails not triggering workflow**: Verify Gmail forwarding is set up correctly
- **Wrong emails being processed**: Check Gmail filter criteria
- **No GitHub Issues created**: Confirm forwarding address is correct

### General Issues
- Check GitHub Actions logs for detailed error messages
- Test Telegram bot token with a simple API call
- Verify the bot can send messages to your chat
- Check that GitHub Issues are being created from forwarded emails

## License
This project is open source and available under the MIT License.
