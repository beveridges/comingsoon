#!/usr/bin/env python3
"""
Check if view_emails.php exists on server
"""

import ftplib

# FTP Configuration
FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

def main():
    print("Checking if view_emails.php exists on server...")
    
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        
        # Check in coming-soon directory
        try:
            ftp.cwd('/public_html/coming-soon')
            files = ftp.nlst()
            if 'view_emails.php' in files:
                print("✓ view_emails.php exists in /coming-soon/")
            else:
                print("✗ view_emails.php NOT FOUND in /coming-soon/")
                print(f"   Files in directory: {files}")
        except:
            print("Could not check /coming-soon/ directory")
        
        ftp.quit()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

