#!/usr/bin/env python3
"""
Quick file upload script - upload individual files to the server

Usage:
    python upload_file.py <file_path> [remote_directory]
    
Examples:
    python upload_file.py downloads/index.html
    python upload_file.py css/style.css
    python upload_file.py js/script.js
    python upload_file.py en/index.html coming-soon/en/
    python upload_file.py index.html public_html/
"""

import ftplib
import os
import sys

# FTP Configuration
FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

# Default remote paths based on file location
DEFAULT_PATHS = {
    'downloads/': '/public_html/downloads/',
    'en/': '/public_html/coming-soon/en/',
    'es/': '/public_html/coming-soon/es/',
    'css/': '/public_html/coming-soon/css/',
    'js/': '/public_html/coming-soon/js/',
    'img/': '/public_html/coming-soon/img/',
    'video/': '/public_html/coming-soon/video/',
    'fonts/': '/public_html/coming-soon/fonts/',
}

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

def determine_remote_path(local_file):
    """Determine the remote path based on local file path"""
    # Check if it's in downloads
    if local_file.startswith('downloads/'):
        return '/public_html/downloads/', local_file.replace('downloads/', '')
    
    # Check if it's root level
    if '/' not in local_file or local_file.startswith('./'):
        if local_file == 'index.html' or local_file == '.htaccess':
            return '/public_html/', local_file
    
    # Check for coming-soon subdirectories
    for local_dir, remote_dir in DEFAULT_PATHS.items():
        if local_file.startswith(local_dir):
            filename = local_file.replace(local_dir, '')
            return remote_dir, filename
    
    # Default: assume coming-soon root
    return '/public_html/coming-soon/', local_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_file.py <file_path> [remote_directory]")
        print("\nExamples:")
        print("  python upload_file.py downloads/index.html")
        print("  python upload_file.py css/style.css")
        print("  python upload_file.py index.html public_html/")
        return
    
    local_file = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(local_file):
        print(f"✗ File not found: {local_file}")
        return
    
    # Determine remote path
    if len(sys.argv) >= 3:
        remote_dir = sys.argv[2]
        if not remote_dir.endswith('/'):
            remote_dir += '/'
        remote_file = os.path.basename(local_file)
    else:
        remote_dir, remote_file = determine_remote_path(local_file)
    
    remote_path = remote_file
    
    print("=" * 60)
    print("Quick File Upload")
    print("=" * 60)
    print(f"Local file:  {local_file}")
    print(f"Remote dir:  {remote_dir}")
    print(f"Remote file: {remote_path}")
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
        # Navigate to remote directory
        print(f"Navigating to {remote_dir}...")
        try:
            # Try absolute path first
            ftp.cwd(remote_dir)
        except:
            try:
                # Try relative path
                parts = remote_dir.strip('/').split('/')
                for part in parts:
                    if part:
                        try:
                            ftp.cwd(part)
                        except:
                            print(f"⚠️  Directory {part} doesn't exist, creating...")
                            ftp.mkd(part)
                            ftp.cwd(part)
            except Exception as e:
                print(f"✗ Could not navigate to {remote_dir}: {e}")
                print(f"   Current directory: {ftp.pwd()}")
                return
        
        print("✓ In target directory")
        print()
        
        # Upload file
        print(f"Uploading {local_file}...")
        if upload_file(ftp, local_file, remote_path):
            print()
            print("=" * 60)
            print("✓ Upload complete!")
            print("=" * 60)
        else:
            print()
            print("✗ Upload failed")
        
    finally:
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == '__main__':
    main()

