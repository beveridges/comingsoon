#!/usr/bin/env python3
"""
Check and download the parent .htaccess file
"""

import ftplib

# FTP Configuration
FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

def main():
    print("=" * 60)
    print("Checking parent /public_html/.htaccess")
    print("=" * 60)
    print()
    
    # Connect to FTP server
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
        ftp.cwd('/public_html')
        print("✓ In /public_html/ directory")
        print()
        
        # Download .htaccess
        print("Downloading .htaccess...")
        try:
            with open('parent_htaccess.txt', 'wb') as f:
                ftp.retrbinary('RETR .htaccess', f.write)
            print("✓ Downloaded .htaccess to parent_htaccess.txt")
            print()
            print("Contents of /public_html/.htaccess:")
            print("-" * 60)
            with open('parent_htaccess.txt', 'r') as f:
                print(f.read())
            print("-" * 60)
        except Exception as e:
            print(f"✗ Could not download .htaccess: {e}")
        
    finally:
        ftp.quit()
        print("\nDisconnected from FTP server.")

if __name__ == '__main__':
    main()

