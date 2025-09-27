"""
Email processing module for Gmail IMAP operations.
"""
import imapclient
import email
from email.header import decode_header
from config import GMAIL_USER, GMAIL_APP_PASSWORD, logger

def decode_email_header(header):
    """Safely decode email header."""
    if not header:
        return ""
    
    try:
        decoded_parts = decode_header(header)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += part
        return decoded_string
    except Exception as e:
        logger.warning(f"Failed to decode header: {e}")
        return str(header)

def extract_email_content(msg):
    """Extract text content from email message."""
    content = ""
    
    try:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    payload = part.get_payload(decode=True)
                    if payload:
                        content = payload.decode('utf-8', errors='ignore')
                        break
                elif part.get_content_type() == 'text/html' and not content:
                    # Fallback to HTML if no plain text found
                    payload = part.get_payload(decode=True)
                    if payload:
                        content = payload.decode('utf-8', errors='ignore')
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                content = payload.decode('utf-8', errors='ignore')
    except Exception as e:
        logger.error(f"Failed to extract email content: {e}")
        content = "Failed to extract email content"
    
    return content

def test_gmail_connection():
    """Test Gmail IMAP connection."""
    try:
        with imapclient.IMAPClient('imap.gmail.com', ssl=True) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.select_folder('INBOX')
            logger.info("✅ Gmail connection test successful!")
            
            # Get recent email count for info
            all_messages = server.search(['ALL'])
            unread_messages = server.search(['UNSEEN'])
            logger.info(f"📧 Total emails in inbox: {len(all_messages)}")
            logger.info(f"📩 Unread emails: {len(unread_messages)}")
            
            return True
    except Exception as e:
        logger.error(f"❌ Gmail connection test failed: {e}")
        return False

def fetch_immoscout_emails():
    """Fetch unread emails from Immobilien Scout."""
    try:
        with imapclient.IMAPClient('imap.gmail.com', ssl=True) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.select_folder('INBOX')
            
            # Search for unread Immobilien Scout emails
            search_criteria = ['UNSEEN', 'OR', 'FROM', 'noreply@immobilienscout24.de', 'FROM', 'service@immobilienscout24.de']
            messages = server.search(search_criteria)
            
            if not messages:
                logger.info("No new emails found")
                return []
            
            logger.info(f"Found {len(messages)} new emails")
            
            email_data = []
            for uid in messages:
                try:
                    message_data = server.fetch([uid], ['RFC822'])
                    msg = email.message_from_bytes(message_data[uid][b'RFC822'])
                    
                    # Decode subject and sender
                    subject = decode_email_header(msg['Subject'])
                    sender = decode_email_header(msg['From'])
                    
                    # Extract email content
                    body = extract_email_content(msg)
                    
                    email_data.append({
                        'uid': uid,
                        'subject': subject,
                        'sender': sender,
                        'body': body
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to process email {uid}: {e}")
                    continue
            
            return email_data, server
            
    except Exception as e:
        logger.error(f"Failed to fetch emails: {e}")
        return []

def mark_email_as_read(server, uid):
    """Mark an email as read."""
    try:
        server.add_flags([uid], [imapclient.SEEN])
        return True
    except Exception as e:
        logger.error(f"Failed to mark email {uid} as read: {e}")
        return False