"""
GitHub Issues email processor - Alternative to Gmail IMAP.
Processes emails that were forwarded to GitHub Issues.
"""
import os
import re
from datetime import datetime
from config import logger

def parse_github_issue_email(issue_body):
    """
    Parse email content from GitHub Issue body.
    GitHub formats forwarded emails in a specific way.
    """
    if not issue_body:
        return None
    
    # GitHub issue body contains the forwarded email
    # Look for email-like content patterns
    email_content = {
        'subject': '',
        'sender': '',
        'body': issue_body,
        'timestamp': datetime.now().isoformat()
    }
    
    # Try to extract subject from issue title or body
    subject_match = re.search(r'Subject:\s*(.+)', issue_body, re.MULTILINE)
    if subject_match:
        email_content['subject'] = subject_match.group(1).strip()
    
    # Try to extract sender
    sender_match = re.search(r'From:\s*(.+)', issue_body, re.MULTILINE)
    if sender_match:
        email_content['sender'] = sender_match.group(1).strip()
    
    # Check if this looks like an Immobilienscout email
    is_immoscout = any(keyword in issue_body.lower() for keyword in [
        'immobilienscout', 'immobilien scout', 'wohnung', 'zimmer', 'miete'
    ])
    
    if is_immoscout:
        logger.info(f"📧 Detected Immobilienscout email via GitHub Issue")
        return email_content
    
    logger.info("📧 Email doesn't appear to be from Immobilienscout, skipping")
    return None

def get_github_context():
    """Get GitHub context from environment variables."""
    return {
        'event_name': os.environ.get('GITHUB_EVENT_NAME'),
        'issue_number': os.environ.get('GITHUB_EVENT_ISSUE_NUMBER'),
        'issue_title': os.environ.get('GITHUB_EVENT_ISSUE_TITLE'),
        'issue_body': os.environ.get('GITHUB_EVENT_ISSUE_BODY'),
        'repository': os.environ.get('GITHUB_REPOSITORY')
    }

def should_process_github_event():
    """Determine if we should process this GitHub event."""
    context = get_github_context()
    
    # Only process issue events
    if context['event_name'] != 'issues':
        return False, "Not an issue event"
    
    # Check if issue title/body suggests it's an email
    issue_content = f"{context.get('issue_title', '')} {context.get('issue_body', '')}"
    
    # Look for email indicators
    email_indicators = ['@', 'subject:', 'from:', 'immobilienscout']
    has_email_content = any(indicator in issue_content.lower() for indicator in email_indicators)
    
    if not has_email_content:
        return False, "Issue doesn't appear to contain email content"
    
    return True, "Issue contains email content"

async def process_github_issue_email():
    """Process email content from GitHub Issue."""
    context = get_github_context()
    
    should_process, reason = should_process_github_event()
    if not should_process:
        logger.info(f"⏭️ Skipping GitHub event: {reason}")
        return []
    
    logger.info(f"📧 Processing GitHub Issue #{context.get('issue_number')}")
    
    # Parse the email from issue body
    email_data = parse_github_issue_email(context.get('issue_body', ''))
    
    if email_data:
        return [email_data]
    
    return []