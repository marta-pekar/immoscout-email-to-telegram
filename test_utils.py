"""
Test utilities for mock testing without real credentials.
"""
import asyncio
from apartment_parser import parse_apartment_info, format_telegram_message
from config import logger

async def mock_test_connections():
    """Mock connection tests for demo purposes."""
    logger.info("🧪 Running MOCK connection tests...")
    
    # Mock Telegram test
    logger.info("📡 Testing Telegram connection...")
    await asyncio.sleep(1)  # Simulate network delay
    logger.info("✅ Telegram connection test successful! (MOCK)")
    
    # Mock Gmail test
    logger.info("📧 Testing Gmail connection...")
    await asyncio.sleep(1)  # Simulate network delay
    logger.info("✅ Gmail connection test successful! (MOCK)")
    logger.info("📧 Total emails in inbox: 245 (MOCK)")
    logger.info("📩 Unread emails: 12 (MOCK)")
    
    logger.info("🎉 All mock tests passed! This demonstrates the testing workflow.")
    return True

def create_mock_email_data():
    """Create mock email data for testing."""
    mock_emails = [
        {
            'subject': 'Neue Wohnung in Berlin-Mitte - 2 Zimmer, 65m²',
            'sender': 'noreply@immobilienscout24.de',
            'body': '''Hallo,

wir haben eine neue Wohnung für Sie gefunden:

2-Zimmer-Wohnung in Berlin-Mitte
Größe: 65 m²
Preis: 1.200 €
Adresse: Hackescher Markt 5, 10178 Berlin

Link: https://www.immobilienscout24.de/expose/123456789

Viele Grüße
Ihr ImmobilienScout24 Team'''
        },
        {
            'subject': 'ImmobilienScout24: 3-Zimmer-Wohnung in München verfügbar',
            'sender': 'service@immobilienscout24.de', 
            'body': '''Neue Suchanfrage Match!

3 Zimmer Wohnung in München
Wohnfläche: 85 m²
Kaltmiete: 1.800 €
Lage: in Schwabing-West

Zur Anzeige: https://www.immobilienscout24.de/expose/987654321

ImmobilienScout24'''
        }
    ]
    return mock_emails

async def mock_email_processing():
    """Mock the full email processing workflow."""
    logger.info("🧪 Running MOCK email processing...")
    
    # Simulate connecting to Gmail
    logger.info("📧 Connecting to Gmail... (MOCK)")
    await asyncio.sleep(1)
    
    # Get mock emails
    mock_emails = create_mock_email_data()
    logger.info(f"📩 Found {len(mock_emails)} new emails (MOCK)")
    
    processed_count = 0
    for i, email_data in enumerate(mock_emails, 1):
        logger.info(f"📄 Processing email {i}: {email_data['subject'][:50]}...")
        
        # Parse apartment information
        apartment_info = parse_apartment_info(email_data['subject'], email_data['body'])
        
        # Format Telegram message
        telegram_message = format_telegram_message(apartment_info)
        
        # Mock sending to Telegram
        logger.info("📱 Sending to Telegram... (MOCK)")
        await asyncio.sleep(0.5)
        
        # Show what would be sent
        logger.info("📝 Mock Telegram message:")
        logger.info("─" * 50)
        logger.info(telegram_message.replace('*', ''))
        logger.info("─" * 50)
        
        logger.info(f"✅ Successfully processed email from {email_data['sender']} (MOCK)")
        processed_count += 1
    
    logger.info(f"🎉 Successfully processed {processed_count} emails (MOCK)")
    return True

def show_parsing_examples():
    """Show parsing examples without any network operations."""
    logger.info("📊 Demonstrating email parsing...")
    mock_emails = create_mock_email_data()
    for i, email_data in enumerate(mock_emails, 1):
        logger.info(f"\n📄 Email {i}: {email_data['subject']}")
        apartment_info = parse_apartment_info(email_data['subject'], email_data['body'])
        logger.info(f"📊 Parsed data: {apartment_info}")
        
        formatted_message = format_telegram_message(apartment_info)
        logger.info("📱 Formatted Telegram message:")
        logger.info("─" * 30)
        logger.info(formatted_message.replace('*', ''))
        logger.info("─" * 30)