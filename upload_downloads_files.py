#!/usr/bin/env python3
"""
Upload both index.html and index.php to /public_html/downloads/
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

def list_files(ftp):
    """List files in current directory"""
    try:
        files = ftp.nlst()
        print(f"Files in current directory: {files}")
        return files
    except Exception as e:
        print(f"Could not list files: {e}")
        return []

def main():
    print("=" * 60)
    print("Uploading index files to /public_html/downloads/")
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
        
        # List existing files
        print("Checking existing files...")
        existing_files = list_files(ftp)
        print()
        
        # Upload index.html
        index_html_path = 'downloads/index.html'
        if os.path.exists(index_html_path):
            print("Uploading index.html...")
            if upload_file(ftp, index_html_path, 'index.html'):
                print("✓ index.html uploaded")
            else:
                print("✗ Failed to upload index.html")
        else:
            print(f"⚠️  File not found: {index_html_path}")
        
        print()
        
        # Upload index.php (higher priority than index.html on most servers)
        index_php_path = 'downloads/index.php'
        if os.path.exists(index_php_path):
            print("Uploading index.php...")
            if upload_file(ftp, index_php_path, 'index.php'):
                print("✓ index.php uploaded")
            else:
                print("✗ Failed to upload index.php")
        else:
            print(f"⚠️  File not found: {index_php_path}")
        
        print()
        
        # Upload .htaccess again
        htaccess_path = 'downloads/.htaccess'
        if os.path.exists(htaccess_path):
            print("Uploading .htaccess...")
            if upload_file(ftp, htaccess_path, '.htaccess'):
                print("✓ .htaccess uploaded")
            else:
                print("✗ Failed to upload .htaccess")
        else:
            print(f"⚠️  File not found: {htaccess_path}")
        
        print()
        print("=" * 60)
        print("Upload complete!")
        print("=" * 60)
        print()
        print("Files uploaded:")
        print("  - index.html (custom page)")
        print("  - index.php (redirect to coming-soon)")
        print("  - .htaccess (disable directory listing)")
        print()
        print("The server should now serve index.php or index.html")
        print("instead of showing the directory listing.")
        print()
        print("Visit https://www.moviolabs.com/downloads/ to verify.")
        
    finally:
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == '__main__':
    main()

