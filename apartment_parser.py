"""
Apartment data parsing utilities.
"""
import re
from datetime import datetime
from config import logger

def parse_apartment_info(subject, body):
    """Parse apartment information from email content."""
    info = {
        'subject': subject,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Extract key information using regex patterns
    patterns = {
        'price': r'(\d+(?:[.,]\d+)?)\s*€',
        'rooms': r'(\d+(?:[.,]\d+)?)\s*Zimmer',
        'area': r'(\d+(?:[.,]\d+)?)\s*m²',
        'location': r'in\s+([^,\n]+)',
        'url': r'https?://[^\s]+'
    }
    
    text = f"{subject} {body}"
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            info[key] = match.group(1) if key != 'url' else match.group(0)
    
    return info

def format_telegram_message(apartment_info):
    """Format apartment information for Telegram message."""
    message = f"🏠 *New Apartment Alert*\n\n"
    message += f"📝 *Subject:* {apartment_info['subject']}\n"
    message += f"🕐 *Time:* {apartment_info['timestamp']}\n\n"
    
    if 'price' in apartment_info:
        message += f"💰 *Price:* {apartment_info['price']}€\n"
    if 'rooms' in apartment_info:
        message += f"🚪 *Rooms:* {apartment_info['rooms']}\n"
    if 'area' in apartment_info:
        message += f"📐 *Area:* {apartment_info['area']} m²\n"
    if 'location' in apartment_info:
        message += f"📍 *Location:* {apartment_info['location']}\n"
    if 'url' in apartment_info:
        message += f"🔗 *Link:* {apartment_info['url']}\n"
    
    return message