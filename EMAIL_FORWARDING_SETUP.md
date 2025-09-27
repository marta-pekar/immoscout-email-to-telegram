# Email Forwarding Setup Guide

This guide explains how to set up email forwarding from Gmail to GitHub to trigger the pipeline instantly instead of polling every 15 minutes.

## 🔄 **Email Forwarding Options**

### Option 1: Gmail → GitHub Issues (Recommended)

#### **Setup Steps:**

1. **Get your GitHub repository's email address:**
   - Go to your repository: `https://github.com/marta-pekar/immoscout-email-to-telegram`
   - Go to **Settings** → **Email notifications**
   - Find the unique email address for creating issues (format: `username+reponame@users.noreply.github.com`)

2. **Set up Gmail forwarding:**
   - Gmail → Settings → **Forwarding and POP/IMAP**
   - Click **"Add a forwarding address"**
   - Add your GitHub repository email
   - Verify the forwarding address

3. **Create Gmail filter:**
   - Gmail → Settings → **Filters and Blocked Addresses**
   - Create new filter with criteria:
     - **From:** `*@immobilienscout24.de`
     - **Subject:** Contains apartment-related keywords
   - Action: **Forward to** your GitHub repository email

4. **Update workflow trigger:**
   ```yaml
   on:
     issues:
       types: [opened]  # Triggered when email creates new issue
     schedule:
       - cron: '*/15 * * * *'  # Backup polling
   ```

#### **Benefits:**
- ✅ **Instant notifications** (no 15-minute delay)
- ✅ **No Gmail credentials** needed in GitHub
- ✅ **Audit trail** (emails visible as GitHub issues)
- ✅ **Backup polling** still works if forwarding fails

#### **Workflow:**
```
Immobilienscout → Gmail → GitHub Issue → Workflow Trigger → Telegram
```

---

### Option 2: Gmail → Webhook Service → GitHub

#### **Setup Steps:**

1. **Use a webhook service** (Zapier, IFTTT, or custom)
2. **Gmail trigger:** New email from Immobilienscout
3. **Action:** HTTP POST to GitHub repository dispatch endpoint
4. **GitHub workflow** listens for `repository_dispatch` events

#### **Benefits:**
- ✅ **More flexible** filtering and processing
- ✅ **Can modify email content** before sending to GitHub
- ❌ **Requires third-party service**

---

### Option 3: Gmail → Email Parser → GitHub API

#### **Custom Implementation:**
1. **Deploy a small service** (e.g., on Vercel, Netlify Functions)
2. **Service receives emails** via webhook
3. **Parses apartment data** immediately
4. **Calls GitHub API** to trigger workflow with parsed data

---

## 🚀 **Implementation Status**

The code has been prepared to support both:
- **Gmail IMAP polling** (current method)  
- **GitHub Issues email forwarding** (new method)

### **Files Updated:**
- ✅ `github_email_processor.py` - Handles GitHub Issue emails
- ✅ `.github/workflows/email-to-telegram.yml` - Added issue trigger
- ✅ `main.py` - Detects source and processes accordingly

### **To Enable Email Forwarding:**
1. **Set up Gmail forwarding** as described above
2. **Test by sending** a test email to your GitHub repository
3. **Verify workflow triggers** when issue is created
4. **No code changes needed** - it's already implemented!

## 🔧 **Testing the Setup**

1. **Create a test issue** manually in your repository
2. **Add email-like content** in the issue body
3. **Check if workflow triggers** and processes the content
4. **Verify Telegram message** is sent

The system will automatically detect whether it's processing a GitHub Issue or Gmail emails and handle accordingly!