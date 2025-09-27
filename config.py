"""
Configuration module for the Immoscout Email to Telegram bot.
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables from .env file for local testing
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def validate_environment():
    """Validate that all required environment variables are set."""
    # Check if we're in test mode
    test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'
    
    if test_mode:
        logger.info("🧪 Running in TEST MODE - no real credentials needed")
        return True
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.info("Please check your .env file and ensure all variables are set.")
        sys.exit(1)
    
    logger.info("All required environment variables are set")
    return False