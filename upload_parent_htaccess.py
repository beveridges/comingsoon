#!/usr/bin/env python3
"""
Upload updated .htaccess to /public_html/ to handle downloads directory
"""

import ftplib

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
    print("Uploading updated .htaccess to /public_html/")
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
                return
        
        print("✓ In /public_html/ directory")
        print()
        
        # Upload updated .htaccess
        htaccess_path = 'public_html_htaccess.txt'
        if os.path.exists(htaccess_path):
            print("Uploading updated .htaccess...")
            if upload_file(ftp, htaccess_path, '.htaccess'):
                print("✓ .htaccess uploaded successfully!")
                print()
                print("=" * 60)
                print("Upload complete!")
                print("=" * 60)
                print()
                print("The parent .htaccess now:")
                print("  - Disables directory listings globally")
                print("  - Redirects /downloads/ to /coming-soon/en/")
                print()
                print("Visit https://www.moviolabs.com/downloads/ to verify.")
            else:
                print("✗ Failed to upload .htaccess")
        else:
            print(f"✗ File not found: {htaccess_path}")
        
    finally:
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == '__main__':
    import os
    main()

