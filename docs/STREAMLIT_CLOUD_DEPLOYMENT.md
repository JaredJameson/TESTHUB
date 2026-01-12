# Streamlit Cloud Deployment - Quick Start Guide

## Prerequisites Checklist

Before deploying, ensure you have:

- [ ] GitHub account
- [ ] Google Cloud service account JSON (from Google Sheets setup)
- [ ] Google Sheets ID (from your spreadsheet URL)
- [ ] Gmail account with app-specific password
- [ ] Teacher email configured

---

## Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository (if not already done)

```bash
cd /home/jarek/projects/TESTHUB

# Initialize git if needed
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Secrets
.streamlit/secrets.toml
secrets.toml
*.json
!data/*.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml

# Logs
*.log
logs/
EOF
```

### 1.2 Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
streamlit>=1.30.0
pandas>=2.0.0
gspread>=5.11.0
oauth2client>=4.1.3
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.1.1
EOF
```

### 1.3 Verify Critical Files

```bash
# Check that these files exist and are properly formatted
ls -la data/questions.json
ls -la data/test_config.json
ls -la app.py
ls -la modules/
ls -la pages/
```

### 1.4 Create GitHub Repository

```bash
# Add all files
git add .

# Initial commit
git commit -m "Initial commit: AI Marketing Test Platform

- Student test flow with 27 questions
- Teacher dashboard with analytics
- Email notifications
- Google Sheets integration
- Production ready for Streamlit Cloud deployment"

# Create repository on GitHub (via browser):
# 1. Go to https://github.com/new
# 2. Repository name: TESTHUB (or your preferred name)
# 3. Description: AI Marketing Test Platform for UKEN
# 4. Set to Public or Private
# 5. DO NOT initialize with README (you already have files)
# 6. Click "Create repository"

# Add remote and push (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/TESTHUB.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Streamlit Cloud

### 2.1 Access Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click **"Sign up"** or **"Sign in"** with your GitHub account
3. Authorize Streamlit Cloud to access your GitHub repositories

### 2.2 Create New App

1. Click **"New app"** button
2. Fill in the deployment settings:
   - **Repository:** Select your `TESTHUB` repository
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL (optional):** Choose a custom URL like `uken-ai-marketing-test`

3. Click **"Advanced settings"** (IMPORTANT!)
4. **Python version:** Select `3.11` or `3.10`
5. Keep other settings as default
6. Click **"Deploy!"**

### 2.3 Initial Deployment

The app will start deploying. You'll see:
```
Preparing deployment...
Installing dependencies...
Starting application...
```

**Expected:** The app will fail initially because secrets are not configured yet. This is normal!

---

## Step 3: Configure Secrets

### 3.1 Access Secrets Management

1. In Streamlit Cloud dashboard, click on your app
2. Click the **"⋮"** menu (three dots) in the top right
3. Select **"Settings"**
4. Go to the **"Secrets"** tab

### 3.2 Add Secrets

Copy and paste the following into the secrets editor, replacing the placeholder values with your actual credentials:

```toml
# Google Sheets Configuration
[google_sheets]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Content-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"

# Application Configuration
[app]
spreadsheet_id = "your-google-sheets-id-from-url"

# Email Configuration
[email]
sender_email = "your-email@gmail.com"
sender_password = "your-16-char-app-specific-password"
teacher_email = "teacher@example.com"
```

### 3.3 Get Your Credentials

#### Google Sheets Credentials (from service account JSON):

If you have your service account JSON file, open it and copy the values:

```bash
# View your service account JSON
cat path/to/your-service-account.json
```

Copy these fields:
- `project_id`
- `private_key_id`
- `private_key` (IMPORTANT: Keep the \n characters for line breaks)
- `client_email`
- `client_id`
- `client_x509_cert_url`

#### Google Sheets ID:

From your Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/1ABC...XYZ/edit
                                      ^^^^^^^^^^^
                                      This is your spreadsheet_id
```

#### Gmail App-Specific Password:

If you haven't created one yet:

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already enabled)
3. Search for "App passwords"
4. Create new app password:
   - Select app: "Mail"
   - Select device: "Other" (name it "TESTHUB")
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)
6. Remove spaces when adding to secrets: `xxxxxxxxxxxxxxxx`

### 3.4 Save Secrets

1. After pasting all secrets, click **"Save"**
2. The app will automatically restart with the new secrets
3. Wait for redeployment (usually 30-60 seconds)

---

## Step 4: Verify Deployment

### 4.1 Check Application Status

After secrets are saved:

1. **Watch the logs** in Streamlit Cloud dashboard
2. Look for successful startup messages:
   ```
   You can now view your Streamlit app in your browser.
   Network URL: http://xxx.xxx.xxx.xxx:8501
   External URL: https://your-app.streamlit.app
   ```

3. **If you see errors**, check the common issues below

### 4.2 Test the Application

#### Test Student Flow:

1. Click on your app URL
2. Click **"Logowanie Studenta"**
3. Enter test data:
   - Email: `test@example.com`
   - First Name: `Test`
   - Last Name: `Student`
   - Student ID: `12345`
4. Click **"Zaloguj się i rozpocznij test"**
5. Verify:
   - ✅ Timer starts at 30:00
   - ✅ Questions load (27 total)
   - ✅ Can navigate between questions
   - ✅ Can select answers
   - ✅ Progress bar updates

#### Test Teacher Flow:

1. Go back to home page
2. Click **"Panel Nauczyciela"**
3. Enter teacher credentials:
   - Email: (from your Google Sheets "Teachers" tab)
   - Password: (the original password, not the hash)
4. Verify:
   - ✅ Dashboard loads
   - ✅ Statistics display
   - ✅ Can see student results
   - ✅ Can export CSV

### 4.3 Verify Google Sheets Integration

1. Open your Google Sheets
2. Check "Wyniki_Testow" tab
3. Complete a test submission
4. Verify:
   - ✅ New row appears with test results
   - ✅ All columns populated correctly
   - ✅ Timestamp is accurate

### 4.4 Verify Email Functionality

1. Complete a test with a real email address you can access
2. Check inbox for:
   - ✅ Student result email
   - ✅ Teacher notification email (to teacher_email)
3. Check SPAM folder if not in inbox

---

## Step 5: Configure Custom Domain (Optional)

### 5.1 Use Streamlit's Default Domain

Your app is available at:
```
https://your-app-name.streamlit.app
```

This is free and includes SSL (HTTPS) automatically.

### 5.2 Custom Domain (Streamlit Cloud Pro Required)

If you have Streamlit Cloud Pro plan:

1. Go to app settings
2. Navigate to "Custom domain"
3. Add your domain
4. Update DNS records as instructed
5. Wait for DNS propagation (up to 48 hours)

For educational use, the default domain is perfectly fine.

---

## Common Issues and Solutions

### Issue 1: "No module named 'streamlit'"

**Cause:** requirements.txt missing or not in root directory

**Solution:**
```bash
# Ensure requirements.txt is in root directory
cat requirements.txt

# Verify it contains:
# streamlit>=1.30.0

# Commit and push
git add requirements.txt
git commit -m "Add requirements.txt"
git push
```

### Issue 2: "KeyError: 'google_sheets'"

**Cause:** Secrets not configured correctly

**Solution:**
1. Go to app settings → Secrets
2. Verify TOML format is correct (check brackets, quotes, indentation)
3. Ensure section names match: `[google_sheets]`, `[app]`, `[email]`
4. Save and wait for reboot

### Issue 3: "Permission denied" for Google Sheets

**Cause:** Service account doesn't have access to the spreadsheet

**Solution:**
1. Open your Google Sheets
2. Click "Share" button
3. Add service account email (from `client_email` in secrets)
4. Give "Editor" permissions
5. Click "Send"
6. Restart Streamlit app

### Issue 4: "Authentication failed" for Gmail

**Cause:** App-specific password incorrect or 2FA not enabled

**Solution:**
1. Verify 2FA is enabled on Gmail account
2. Generate new app-specific password:
   - https://myaccount.google.com/security
   - "App passwords"
   - Create new → Mail → Other
3. Copy 16-character password (no spaces)
4. Update secrets with new password
5. Save and reboot

### Issue 5: App keeps restarting

**Cause:** Error in code or missing dependencies

**Solution:**
1. Check logs in Streamlit Cloud dashboard
2. Look for Python errors
3. Verify all imports in requirements.txt
4. Check that data files (questions.json, test_config.json) are committed to git

### Issue 6: "File not found" errors

**Cause:** Data files not in repository

**Solution:**
```bash
# Verify data files are tracked by git
git ls-files data/

# Should show:
# data/questions.json
# data/test_config.json

# If missing, add them:
git add data/questions.json data/test_config.json
git commit -m "Add data files"
git push
```

### Issue 7: Timer not working

**Cause:** Browser compatibility or JavaScript issues

**Solution:**
1. Try different browser (Chrome, Firefox, Safari, Edge)
2. Clear browser cache
3. Disable browser extensions
4. Check if JavaScript is enabled

---

## Monitoring and Maintenance

### Monitor Application Health

1. **Streamlit Cloud Dashboard:**
   - View real-time logs
   - Monitor resource usage
   - Check error rates

2. **Google Sheets:**
   - Monitor new submissions
   - Check API usage (Google Cloud Console)
   - Verify data integrity

3. **Email:**
   - Monitor sending quota (Gmail: 500/day)
   - Check delivery rates
   - Review bounced emails

### Regular Maintenance

**Daily:**
- Check for new student submissions
- Review error logs
- Monitor email delivery

**Weekly:**
- Export data backup (CSV from Google Sheets)
- Review application performance
- Check for user feedback

**Monthly:**
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Review security updates
- Analyze usage statistics

### Update Deployed Application

When you make code changes:

```bash
# Make your changes to code
# Test locally first
streamlit run app.py

# Commit and push
git add .
git commit -m "Description of changes"
git push

# Streamlit Cloud auto-deploys from main branch
# No manual redeployment needed!
```

---

## Performance Optimization

### Caching

The app already uses caching (60-second TTL) for Google Sheets. Monitor if this needs adjustment:

```python
# In modules/sheets_manager.py
@st.cache_data(ttl=60)  # Adjust TTL if needed
def get_all_results(self):
    # ...
```

### Resource Limits

Streamlit Cloud free tier includes:
- 1 GB RAM
- 1 CPU core
- Unlimited bandwidth

For larger deployments, consider:
- Streamlit Cloud Pro (more resources)
- Self-hosted deployment (VPS)

---

## Security Best Practices

### ✅ Already Implemented

- ✅ Secrets stored in Streamlit Cloud (not in code)
- ✅ Service account authentication
- ✅ Password hashing (SHA256)
- ✅ HTTPS enabled by default
- ✅ No sensitive data in repository

### Additional Recommendations

1. **Regular Updates:**
   - Update dependencies monthly
   - Monitor security advisories
   - Update Python version annually

2. **Access Control:**
   - Limit who has GitHub repository access
   - Rotate service account keys periodically
   - Change teacher passwords regularly

3. **Monitoring:**
   - Set up email alerts for errors
   - Monitor Google Sheets API quota
   - Review access logs periodically

---

## Cost Breakdown

### Free Tier (Streamlit Cloud)

✅ **FREE:**
- Unlimited public apps
- 1 GB RAM per app
- 1 CPU core per app
- HTTPS included
- Auto-deployment from GitHub
- Community support

**Limitations:**
- Public apps only (unless using Streamlit Cloud for Teams)
- Resource limits (1 GB RAM, 1 CPU)
- Shared infrastructure

### External Services

✅ **FREE:**
- Google Sheets API (free tier: 100 requests/100 seconds)
- Gmail SMTP (free tier: 500 emails/day)
- GitHub (free tier: unlimited public repositories)

**Paid Options (if needed):**
- Streamlit Cloud Teams: $250/month (private apps, more resources)
- Google Workspace: $6-18/user/month (higher API quotas)
- Professional SMTP: $10-50/month (unlimited emails)

**Recommended for Educational Use:** Free tier is sufficient

---

## Success Checklist

### Deployment Complete When:

- [ ] App accessible at `https://your-app.streamlit.app`
- [ ] Student login works
- [ ] Test can be completed
- [ ] Results display correctly
- [ ] Teacher dashboard loads
- [ ] Google Sheets receives data
- [ ] Emails are sent successfully
- [ ] No errors in logs

### Post-Deployment:

- [ ] Test with real users (pilot group)
- [ ] Share URL with students and teachers
- [ ] Provide user guides (STUDENT_GUIDE.md, TEACHER_GUIDE.md)
- [ ] Set up monitoring and alerts
- [ ] Schedule regular backups
- [ ] Document any custom configurations

---

## Getting Help

### Documentation

- **Streamlit Cloud:** https://docs.streamlit.io/streamlit-community-cloud
- **Streamlit Forums:** https://discuss.streamlit.io/
- **Google Sheets API:** https://developers.google.com/sheets/api
- **Project Docs:** `/docs/DEPLOYMENT_GUIDE.md`

### Troubleshooting

1. Check Streamlit Cloud logs first
2. Review Google Sheets permissions
3. Verify secrets configuration
4. Test locally if possible
5. Search Streamlit forums for similar issues

### Support Channels

- **Streamlit Community:** https://discuss.streamlit.io/
- **GitHub Issues:** Create issue in your repository
- **Stack Overflow:** Tag with `streamlit`

---

## Next Steps After Deployment

1. **Pilot Test:**
   - Test with 5-10 students
   - Gather feedback
   - Monitor performance
   - Fix any issues

2. **Full Deployment:**
   - Share URL with all students
   - Provide user guides
   - Monitor submissions
   - Respond to support requests

3. **Iterate:**
   - Collect feedback
   - Implement improvements
   - Update documentation
   - Scale as needed

---

**Deployment Guide Version:** 1.0
**Last Updated:** 2026-01-12
**Status:** Production Ready ✅

**Your App URL:** https://[your-app-name].streamlit.app

**Good luck with your deployment! 🚀**
