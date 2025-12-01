#!/usr/bin/env python3
"""
Upload .htaccess to /public_html/downloads/ to disable directory listing
"""

import ftplib
import os

# FTP Configuration
FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

def upload_file(ftp, local_path, remote_path):
    """Upload a single file"""
    try:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        print(f"✓ Uploaded: {remote_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to upload {remote_path}: {e}")
        return False

def main():
    print("=" * 60)
    print("Uploading .htaccess to /public_html/downloads/")
    print("=" * 60)
    print()
    
    # Connect to FTP server
    print(f"Connecting to {FTP_HOST}...")
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("✓ Connected successfully!")
        print()
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return
    
    try:
        # Navigate to /public_html/downloads
        print("Navigating to /public_html/downloads/...")
        try:
            ftp.cwd('/public_html/downloads')
        except:
            try:
                ftp.cwd('public_html')
                ftp.cwd('downloads')
            except:
                print("⚠️  Could not navigate to /public_html/downloads")
                print("   Current directory:", ftp.pwd())
                return
        
        print("✓ In /public_html/downloads/ directory")
        print()
        
        # Upload .htaccess
        htaccess_path = 'downloads/.htaccess'
        if os.path.exists(htaccess_path):
            print("Uploading .htaccess...")
            if upload_file(ftp, htaccess_path, '.htaccess'):
                print("✓ .htaccess uploaded successfully!")
                print()
                print("=" * 60)
                print("Upload complete!")
                print("=" * 60)
                print()
                print("The directory listing should now be disabled.")
                print("Visit https://www.moviolabs.com/downloads/ to verify.")
            else:
                print("✗ Failed to upload .htaccess")
        else:
            print(f"✗ File not found: {htaccess_path}")
            print("   Make sure the file exists in the downloads/ folder")
        
    finally:
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == '__main__':
    main()

