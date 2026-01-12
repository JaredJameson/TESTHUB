# Deployment Guide - AI Marketing Test Platform

**Version:** 1.0
**Date:** 2026-01-12
**Application:** TESTHUB - AI w Marketingu

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Google Sheets Setup](#google-sheets-setup)
5. [Email Configuration](#email-configuration)
6. [Deployment Options](#deployment-options)
7. [Testing](#testing)
8. [Troubleshooting](#troubleshooting)
9. [Maintenance](#maintenance)

---

## Prerequisites

### System Requirements
- **Python:** 3.8 or higher
- **Operating System:** Linux, macOS, or Windows
- **Memory:** Minimum 512MB RAM
- **Storage:** Minimum 100MB free space

### Required Accounts
- **Google Account:** For Google Sheets API access
- **Gmail Account:** For SMTP email sending (optional)
- **Streamlit Cloud** (optional): For cloud deployment

### Dependencies
All dependencies are listed in `requirements.txt`:
- streamlit >= 1.30.0
- gspread
- oauth2client
- pandas
- python-dateutil

---

## Installation

### 1. Clone or Download Repository
```bash
git clone [repository-url]
cd TESTHUB
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Verify Installation
```bash
python tests/test_data_validation.py
python tests/test_code_structure.py
```

All tests should pass (100%).

---

## Configuration

### 1. Google Sheets Service Account

**Step 1:** Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Project name: "TESTHUB-AIMarketing" (or your choice)

**Step 2:** Enable Google Sheets API
1. In Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Sheets API"
3. Click "Enable"
4. Search for "Google Drive API"
5. Click "Enable"

**Step 3:** Create Service Account
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Service account name: "testhub-service"
4. Click "Create and Continue"
5. Role: "Editor" (or minimum required permissions)
6. Click "Done"

**Step 4:** Generate Service Account Key
1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" format
5. Click "Create"
6. Save the downloaded JSON file securely

**Step 5:** Extract Credentials
From the downloaded JSON file, you'll need these fields for secrets.toml:
- type
- project_id
- private_key_id
- private_key
- client_email
- client_id
- auth_uri
- token_uri
- auth_provider_x509_cert_url
- client_x509_cert_url

### 2. Create Secrets Configuration

Create `.streamlit/secrets.toml` file:

```toml
# Google Sheets API Configuration
[google_sheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"

# Application Configuration
[app]
spreadsheet_id = "your-google-sheets-id-here"

# Email Configuration (Optional)
[email]
sender_email = "your-email@gmail.com"
sender_password = "your-app-specific-password"
teacher_email = "teacher@example.com"
```

**Important Notes:**
- The `private_key` field must preserve line breaks with `\n`
- Use double quotes for all string values
- Never commit `secrets.toml` to version control
- Add `.streamlit/secrets.toml` to `.gitignore`

### 3. Security Best Practices

**File Permissions:**
```bash
chmod 600 .streamlit/secrets.toml
```

**Git Ignore:**
Add to `.gitignore`:
```
.streamlit/secrets.toml
*.pyc
__pycache__/
venv/
.env
```

---

## Google Sheets Setup

### 1. Create Google Sheets Document

**Step 1:** Create New Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet
3. Name it: "TESTHUB_AI_Marketing_Results"

**Step 2:** Create Required Sheets

Create **3 sheets** with exact names:

#### Sheet 1: Wyniki_Testow
Headers (Row 1):
```
Timestamp | Email | First_Name | Last_Name | Student_ID | Correct_Count |
Percentage | Grade | Grade_Text | Status | Time_Spent_Minutes | Details_JSON |
Test_Version | Browser_Info | Attempt_Number | Auto_Submitted | Zdany | Czas_Sekundy
```

Column Details:
- A: Timestamp (text)
- B: Email (text)
- C: First_Name (text)
- D: Last_Name (text)
- E: Student_ID (text)
- F: Correct_Count (number)
- G: Percentage (number)
- H: Grade (text)
- I: Grade_Text (text)
- J: Status (text)
- K: Time_Spent_Minutes (number)
- L: Details_JSON (text)
- M: Test_Version (text)
- N: Browser_Info (text)
- O: Attempt_Number (number)
- P: Auto_Submitted (boolean)
- Q: Zdany (boolean - formula)
- R: Czas_Sekundy (number)

**Formulas for auto-calculation:**
- Column Q (Zdany): `=IF(J2="ZALICZONY",TRUE,FALSE)`
- Column R (Czas_Sekundy): `=K2*60`

#### Sheet 2: Teachers
Headers (Row 1):
```
Email | Password_Hash | First_Name | Last_Name | Created_Date | Last_Login
```

Add initial teacher account:
```
teacher@example.com | [SHA256 hash of password] | Jan | Kowalski | 2026-01-12 |
```

To generate password hash:
```python
import hashlib
password = "your-secure-password"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(hash_value)
```

#### Sheet 3: Config (Optional - for future use)
Headers:
```
Key | Value | Description
```

Example rows:
```
max_attempts | 2 | Maximum test attempts per student
test_active | true | Whether test is currently active
maintenance_mode | false | Maintenance mode flag
```

### 2. Share with Service Account

**Important:** Share the spreadsheet with your service account email:
1. Click "Share" button in Google Sheets
2. Add service account email (e.g., `testhub-service@project-id.iam.gserviceaccount.com`)
3. Set permission to "Editor"
4. Uncheck "Notify people"
5. Click "Share"

### 3. Copy Spreadsheet ID

From the URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

Copy the `SPREADSHEET_ID` and add it to `secrets.toml`:
```toml
[app]
spreadsheet_id = "your-spreadsheet-id-here"
```

---

## Email Configuration

### Option 1: Gmail SMTP (Recommended)

**Step 1:** Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification"

**Step 2:** Generate App Password
1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Other (Custom name)"
3. Enter name: "TESTHUB"
4. Click "Generate"
5. Copy the 16-character password

**Step 3:** Add to secrets.toml
```toml
[email]
sender_email = "your-email@gmail.com"
sender_password = "abcd efgh ijkl mnop"  # 16-character app password
teacher_email = "teacher@example.com"
```

### Option 2: Disable Email (Testing)

If you want to test without email:
1. Remove `[email]` section from `secrets.toml`
2. Application will show warning but continue working
3. Test results will still save to Google Sheets

---

## Deployment Options

### Option 1: Local Development

**Start Application:**
```bash
streamlit run app.py
```

Application will open at: `http://localhost:8501`

**Stop Application:**
Press `Ctrl+C` in terminal

### Option 2: Streamlit Cloud (Free)

**Step 1:** Prepare Repository
1. Push code to GitHub (private repository recommended)
2. Ensure `requirements.txt` is up-to-date
3. DO NOT commit `secrets.toml`

**Step 2:** Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select repository and branch
5. Main file path: `app.py`
6. Click "Advanced settings"

**Step 3:** Configure Secrets
1. In "Secrets" section, paste contents of `secrets.toml`
2. Click "Save"
3. Click "Deploy"

**Step 4:** Custom Domain (Optional)
1. Go to app settings
2. Add custom domain
3. Follow DNS configuration instructions

### Option 3: Docker (Advanced)

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run:**
```bash
docker build -t testhub .
docker run -p 8501:8501 -v $(pwd)/.streamlit:/app/.streamlit testhub
```

### Option 4: VPS/Cloud Server

**Requirements:**
- Ubuntu 20.04+ / Debian 11+
- Python 3.8+
- Nginx (reverse proxy)
- Systemd (service management)

**Installation Steps:**

1. **Install Dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

2. **Setup Application:**
```bash
cd /opt
sudo git clone [repo-url] testhub
cd testhub
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt
```

3. **Configure Systemd Service:**

Create `/etc/systemd/system/testhub.service`:
```ini
[Unit]
Description=TESTHUB Streamlit Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/testhub
ExecStart=/opt/testhub/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx:**

Create `/etc/nginx/sites-available/testhub`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable and Start:**
```bash
sudo ln -s /etc/nginx/sites-available/testhub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
sudo systemctl enable testhub
sudo systemctl start testhub
```

---

## Testing

### Pre-Deployment Checklist

- [ ] All tests pass (data validation, code structure)
- [ ] Google Sheets configured and shared
- [ ] Service account has correct permissions
- [ ] secrets.toml configured correctly
- [ ] Email service tested (optional)
- [ ] Teacher account created in Google Sheets
- [ ] Test data validated (27 questions)

### Test Student Flow

1. Navigate to application URL
2. Click "Login Student"
3. Enter test student credentials:
   - Email: test.student@example.com
   - First Name: Test
   - Last Name: Student
4. Click "Rozpocznij Test"
5. Answer a few questions
6. Verify auto-save triggers
7. Complete test
8. Verify results display
9. Check Google Sheets for saved data
10. Check email inbox (if configured)

### Test Teacher Flow

1. Navigate to application URL
2. Click "Login Teacher"
3. Enter teacher credentials
4. Verify dashboard loads
5. Check global statistics
6. Check category analysis
7. Verify student list displays
8. Test filters and sorting
9. Export CSV
10. Search for specific student

---

## Troubleshooting

### Common Issues

#### Issue: "No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
```

#### Issue: "Error loading from Sheets"
**Solution:**
1. Verify spreadsheet_id in secrets.toml
2. Check service account has access to sheet
3. Verify Google Sheets API is enabled
4. Check service account key is valid

#### Issue: "Email service not configured"
**Solution:**
1. Add [email] section to secrets.toml
2. Verify Gmail app password
3. Check sender_email is correct
4. This is a warning, not an error - app will work without email

#### Issue: "Authentication failed"
**Solution:**
1. Check teacher credentials in Google Sheets
2. Verify password hash is correct (SHA256)
3. Check email format

#### Issue: "Timer not counting down"
**Solution:**
1. Check browser console for errors
2. Verify test initialization worked
3. Clear browser cache and refresh

### Debug Mode

Enable debug logging:
```bash
streamlit run app.py --logger.level=debug
```

### Logs Location

**Local Development:**
- Terminal output

**Streamlit Cloud:**
- Click "Manage app" > "Logs"

**VPS/Server:**
```bash
sudo journalctl -u testhub -f
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor application logs
- Check error rates
- Verify email delivery

**Weekly:**
- Export results backup
- Check Google Sheets quota
- Review student feedback

**Monthly:**
- Update dependencies
- Review security
- Performance optimization

### Backup Strategy

**Google Sheets Backup:**
1. File > Download > Microsoft Excel (.xlsx)
2. Store securely with date stamp
3. Automate with Google Apps Script (optional)

**Code Backup:**
1. Git repository (primary)
2. Regular commits
3. Tagged releases

### Update Procedure

1. **Test in Development:**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

2. **Test Thoroughly:**
- Run all tests
- Manual testing of key flows
- Verify data integrity

3. **Deploy to Production:**
- For Streamlit Cloud: Push to GitHub
- For VPS: Pull changes and restart service

4. **Monitor:**
- Check logs for errors
- Verify functionality
- Monitor user reports

### Security Updates

**Monthly Security Review:**
- Update Python packages
- Review Google Cloud audit logs
- Rotate service account keys (annually)
- Review access permissions

**Update Dependencies:**
```bash
pip list --outdated
pip install --upgrade [package-name]
pip freeze > requirements.txt
```

---

## Support & Contact

**Technical Issues:**
- Check troubleshooting section
- Review application logs
- Check GitHub issues (if applicable)

**Security Concerns:**
- Rotate service account keys immediately
- Review access logs
- Update secrets.toml

**Questions:**
- Review documentation
- Check code comments
- Consult handoff documents

---

## Appendix

### File Structure
```
TESTHUB/
├── app.py                          # Main entry point
├── requirements.txt                # Dependencies
├── .streamlit/
│   └── secrets.toml               # Secrets (not in git)
├── data/
│   ├── questions.json             # Test questions
│   └── test_config.json           # Test configuration
├── modules/
│   ├── __init__.py
│   ├── auth.py                    # Authentication
│   ├── sheets_manager.py          # Google Sheets integration
│   ├── test_engine.py             # Core test logic
│   ├── email_service.py           # Email notifications
│   ├── analytics.py               # Statistics & analysis
│   └── ui_components.py           # UI helpers
├── pages/
│   ├── 1_Student_Login.py         # Student login
│   ├── 2_Student_Test.py          # Test interface
│   ├── 3_Student_Results.py       # Results display
│   ├── 4_Teacher_Login.py         # Teacher login
│   ├── 5_Teacher_Dashboard.py     # Teacher dashboard
│   └── 6_Teacher_Details.py       # Student details
├── docs/
│   ├── handoffs/                  # Session handoff documents
│   └── testing/                   # Test documentation
└── tests/
    ├── test_data_validation.py    # Data tests
    └── test_code_structure.py     # Structure tests
```

### Environment Variables (Alternative to secrets.toml)

For production deployments, you can use environment variables instead:

```bash
export GOOGLE_SHEETS_TYPE="service_account"
export GOOGLE_SHEETS_PROJECT_ID="your-project-id"
# ... (all other credentials)
export APP_SPREADSHEET_ID="your-spreadsheet-id"
export EMAIL_SENDER="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
export EMAIL_TEACHER="teacher@example.com"
```

Then modify code to read from `os.environ` instead of `st.secrets`.

### Performance Optimization

**Caching:**
- Google Sheets queries cached for 60 seconds
- Analytics calculations cached
- Question data loaded once

**Optimization Tips:**
- Use Streamlit's `@st.cache_data` decorator
- Minimize API calls to Google Sheets
- Batch email sending
- Use CDN for static assets (if any)

### Scaling Considerations

**Current Limits:**
- Google Sheets: 10 million cells per spreadsheet
- Concurrent users: 50+ (Streamlit Cloud)
- Email sending: Gmail daily limits apply

**If Scaling Needed:**
- Consider PostgreSQL/MySQL instead of Google Sheets
- Use dedicated email service (SendGrid, AWS SES)
- Deploy on dedicated server or container service
- Implement load balancing
- Add Redis for caching

---

**Document Version:** 1.0
**Last Updated:** 2026-01-12
**Author:** Claude Code
**Status:** Production Ready
