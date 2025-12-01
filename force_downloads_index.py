#!/usr/bin/env python3
"""
Force upload index files with multiple names to ensure server recognizes one
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
        print(f"✗ Failed: {remote_path} - {e}")
        return False

def main():
    print("=" * 60)
    print("FORCING index files to /downloads/")
    print("=" * 60)
    print()
    
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        print("✓ Connected")
        
        ftp.cwd('/public_html/downloads')
        print("✓ In /downloads/")
        print()
        
        # Upload multiple index file names (some servers use different defaults)
        files_to_upload = [
            ('downloads/index.html', 'index.html'),
            ('downloads/default.html', 'default.html'),
            ('downloads/index.php', 'index.php'),
        ]
        
        for local, remote in files_to_upload:
            if os.path.exists(local):
                print(f"Uploading {remote}...")
                upload_file(ftp, local, remote)
            else:
                print(f"⚠️  {local} not found")
        
        print()
        print("=" * 60)
        print("All index files uploaded!")
        print("=" * 60)
        print()
        print("The server should now serve one of these index files.")
        print("If it still shows directory listing, the server has")
        print("directory indexing FORCED ON at the server level.")
        print()
        print("You MUST contact your hosting support to disable it.")
        
        ftp.quit()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

