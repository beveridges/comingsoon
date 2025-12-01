#!/usr/bin/env python3
"""Upload German version files"""

import ftplib
import os

FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

def ensure_directory(ftp, dir_name):
    """Create directory if it doesn't exist"""
    try:
        ftp.cwd(dir_name)
        return True
    except:
        try:
            ftp.mkd(dir_name)
            ftp.cwd(dir_name)
            return True
        except Exception as e:
            print(f"Could not create directory {dir_name}: {e}")
            return False

def upload_file(ftp, local_path, remote_path):
    """Upload a file"""
    try:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        print(f"✓ Uploaded: {remote_path}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

try:
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    
    # Navigate to coming-soon
    ftp.cwd('/public_html/coming-soon')
    
    # Create de directory
    print("Creating de/ directory...")
    if ensure_directory(ftp, 'de'):
        print("✓ de/ directory ready")
    
    # Upload German index.html
    print("\nUploading de/index.html...")
    upload_file(ftp, 'de/index.html', 'index.html')
    
    ftp.quit()
    print("\n✓ German files uploaded!")
except Exception as e:
    print(f"Error: {e}")

