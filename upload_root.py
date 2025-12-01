#!/usr/bin/env python3
"""
Quick script to upload root index.html and .htaccess to /public_html/
"""

import ftplib
import os

# FTP Configuration (from deploy_ftp.py)
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
    print("Uploading root index.html and .htaccess to /public_html/")
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
        # Navigate to /public_html
        print("Navigating to /public_html/...")
        try:
            ftp.cwd('/public_html')
        except:
            try:
                ftp.cwd('public_html')
            except:
                print("⚠️  Could not navigate to /public_html")
                print("   Current directory:", ftp.pwd())
                return
        
        print("✓ In /public_html/ directory")
        print()
        
        # Upload index.html
        if os.path.exists('index.html'):
            print("Uploading index.html...")
            if upload_file(ftp, 'index.html', 'index.html'):
                print("✓ index.html uploaded successfully!")
            else:
                print("✗ Failed to upload index.html")
        else:
            print("✗ index.html not found in current directory")
        
        print()
        
        # Upload .htaccess
        if os.path.exists('.htaccess'):
            print("Uploading .htaccess...")
            if upload_file(ftp, '.htaccess', '.htaccess'):
                print("✓ .htaccess uploaded successfully!")
            else:
                print("✗ Failed to upload .htaccess")
        else:
            print("⚠️  .htaccess not found (optional)")
        
        print()
        print("=" * 60)
        print("Upload complete!")
        print("=" * 60)
        print()
        print("Visit https://www.moviolabs.com/ to test the redirect.")
        
    finally:
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == '__main__':
    main()

