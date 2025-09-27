"""
Main application entry point for the Immoscout Email to Telegram bot.
Supports both Gmail IMAP and GitHub Issues email forwarding.
"""
import asyncio
import os
from config import validate_environment, logger
from email_processor import test_gmail_connection, fetch_immoscout_emails, mark_email_as_read
from github_email_processor import process_github_issue_email, should_process_github_event
from telegram_bot import test_telegram_connection, send_telegram_message
from apartment_parser import parse_apartment_info, format_telegram_message
from test_utils import mock_test_connections, mock_email_processing, show_parsing_examples

async def run_tests():
    """Run connection tests."""
    logger.info("🧪 Starting connection tests...")
    
    # Test Telegram first
    telegram_ok = await test_telegram_connection()
    
    # Test Gmail
    gmail_ok = test_gmail_connection()
    
    if telegram_ok and gmail_ok:
        logger.info("🎉 All tests passed! You're ready to run the full script.")
        return True
    else:
        logger.error("❌ Some tests failed. Please check your configuration.")
        return False

async def process_emails():
    """Process real emails from Gmail."""
    logger.info("📧 Connecting to Gmail...")
    
    # Fetch emails
    email_data = fetch_immoscout_emails()
    if not email_data:
        return
    
    emails, server = email_data
    processed_count = 0
    
    for email_info in emails:
        try:
            logger.info(f"� Processing email: {email_info['subject'][:50]}...")
            
            # Parse apartment information
            apartment_info = parse_apartment_info(email_info['subject'], email_info['body'])
            
            # Format and send Telegram message
            telegram_message = format_telegram_message(apartment_info)
            success = await send_telegram_message(telegram_message)
            
            if success:
                # Mark as read only if successfully sent
                mark_email_as_read(server, email_info['uid'])
                processed_count += 1
                logger.info(f"✅ Successfully processed email from {email_info['sender']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to process email {email_info['uid']}: {e}")
            continue
    
    logger.info(f"🎉 Successfully processed {processed_count} emails")

async def main():
    """Main function to process emails and send to Telegram."""
    test_mode = validate_environment()
    
    if test_mode:
        # Test mode menu
        mode = input("\n🧪 TEST MODE - Choose option:\n1. Test connections (mock)\n2. Run full email processing (mock)\n3. Show parsed data examples\nEnter choice (1, 2, or 3): ").strip()
        
        if mode == "1":
            await mock_test_connections()
        elif mode == "2":
            await mock_email_processing()
        elif mode == "3":
            show_parsing_examples()
        else:
            logger.error("Invalid choice. Exiting.")
    else:
        # Real mode menu
        mode = input("\nChoose mode:\n1. Test connections only\n2. Run full email processing\nEnter choice (1 or 2): ").strip()
        
        if mode == "1":
            await run_tests()
        elif mode == "2":
            await process_emails()
        else:
            logger.error("Invalid choice. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
