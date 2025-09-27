"""
Telegram bot integration module.
"""
from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, logger

async def test_telegram_connection():
    """Test Telegram bot connection."""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text="🧪 Test message from Immoscout Email Bot\n\nIf you see this, the Telegram connection is working!"
        )
        logger.info("✅ Telegram connection test successful!")
        return True
    except Exception as e:
        logger.error(f"❌ Telegram connection test failed: {e}")
        return False

async def send_telegram_message(message):
    """Send message to Telegram with error handling."""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID, 
            text=message,
            parse_mode='Markdown',
            disable_web_page_preview=False
        )
        logger.info("Message sent to Telegram successfully")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send Telegram message: {e}")
        # Try sending without markdown if parsing fails
        try:
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message.replace('*', ''))
            logger.info("Message sent to Telegram without formatting")
            return True
        except TelegramError as e2:
            logger.error(f"Failed to send plain message: {e2}")
            return False