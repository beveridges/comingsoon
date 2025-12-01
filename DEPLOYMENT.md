# Deployment Guide - MOVIOLABS Coming Soon Site

## Files to Upload

### ✅ Upload These Files:

1. **Root directory files:**
   - `save_email.php` - Email submission handler
   - `config.php` - Configuration (⚠️ edit on server with correct paths)

2. **Directories to upload:**
   - `css/` - Stylesheets
   - `js/` - JavaScript files
   - `img/` - Images (logo, icons, etc.)
   - `fonts/` - Web fonts
   - `video/` - Background videos
   - `en/` - English version HTML
   - `es/` - Spanish version HTML

3. **Security file:**
   - `private/.htaccess` → Upload to `/home/moviolab/private/.htaccess` (outside public_html)

### ❌ Do NOT Upload:

- `.git/` - Git repository
- `.gitignore` - Git ignore file
- `*.sqlite` - Database files (created on server)
- `deploy_ftp.py` - Deployment script
- `DEPLOYMENT.md` - This file
- Any `.DS_Store`, `Thumbs.db`, or other OS files

## Server Directory Structure

```
/home/moviolab/
├── public_html/
│   └── coming-soon/          ← Upload site files here
│       ├── en/
│       ├── es/
│       ├── css/
│       ├── js/
│       ├── img/
│       ├── fonts/
│       ├── video/
│       ├── save_email.php
│       └── config.php
│
└── private/                  ← Database location (outside public_html)
    ├── .htaccess            ← Upload .htaccess here
    └── email_list.sqlite    ← Created automatically
```

## Using the FTP Deployment Script

1. **Edit `deploy_ftp.py`:**
   - Fill in `FTP_HOST` (your FTP server address)
   - Fill in `FTP_USER` (your FTP username)
   - Fill in `FTP_PASS` (your FTP password)
   - Adjust `REMOTE_WEB_ROOT` if needed (default: `/public_html/coming-soon`)

2. **Run the script:**
   ```bash
   python deploy_ftp.py
   ```

3. **Manual steps after upload:**
   - Edit `config.php` on server to verify database path
   - Set permissions: `chmod 600 /home/moviolab/private/email_list.sqlite` (after first submission)
   - Test the email form

## Manual Upload via cPanel File Manager

If you prefer to upload manually:

1. **Upload site files:**
   - Navigate to `public_html/coming-soon/` in cPanel File Manager
   - Upload all files and folders (except those in the "Do NOT Upload" list)

2. **Upload .htaccess:**
   - Navigate to `private/` directory (outside public_html)
   - Upload `private/.htaccess` file

3. **Edit config.php:**
   - Open `config.php` in cPanel File Manager
   - Verify database path is: `/home/moviolab/private/email_list.sqlite`

## Post-Deployment Checklist

- [ ] All files uploaded to correct locations
- [ ] `.htaccess` uploaded to `/home/moviolab/private/`
- [ ] `config.php` has correct database path
- [ ] Test email submission form (English version)
- [ ] Test email submission form (Spanish version)
- [ ] Verify reCAPTCHA is working
- [ ] Check that database file is created in `private/` directory
- [ ] Set database file permissions (chmod 600)
- [ ] Test rate limiting (try submitting multiple times)

## Security Notes

- Database is stored outside `public_html` in `private/` directory
- `.htaccess` prevents web access to private directory
- Rate limiting prevents spam (5/hour, 20/day per IP)
- reCAPTCHA verification on all submissions
- IP addresses are logged for monitoring

## Troubleshooting

**Database errors:**
- Check that `private/` directory exists and is writable
- Verify database path in `config.php`
- Check file permissions on database file

**reCAPTCHA errors:**
- Verify site key and secret key match your Google reCAPTCHA account
- Check that keys are for the correct domain

**Upload errors:**
- Ensure FTP credentials are correct
- Check that remote directories exist or script can create them
- Verify file permissions on server

