#!/usr/bin/env python3
"""Check if German files exist on server"""

import ftplib

FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

try:
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    
    # Check coming-soon directory
    ftp.cwd('/public_html/coming-soon')
    files = ftp.nlst()
    
    print("Files in /coming-soon/:")
    for f in files:
        print(f"  - {f}")
    
    # Check for de directory
    try:
        ftp.cwd('de')
        de_files = ftp.nlst()
        print("\nFiles in /coming-soon/de/:")
        for f in de_files:
            print(f"  - {f}")
    except:
        print("\n✗ /coming-soon/de/ directory NOT FOUND")
    
    ftp.quit()
except Exception as e:
    print(f"Error: {e}")

