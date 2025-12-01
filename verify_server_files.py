#!/usr/bin/env python3
"""Verify DE is in the HTML files on server"""

import ftplib

FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

def check_file_for_de(ftp, filepath):
    """Check if file contains DE link"""
    try:
        content = []
        ftp.retrlines(f'RETR {filepath}', content.append)
        content_str = '\n'.join(content)
        if 'href="../de/"' in content_str or "href='../de/'" in content_str:
            return True, content_str
        return False, content_str
    except Exception as e:
        return None, str(e)

try:
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    
    ftp.cwd('/public_html/coming-soon')
    
    print("Checking en/index.html...")
    ftp.cwd('en')
    has_de, content = check_file_for_de(ftp, 'index.html')
    if has_de:
        print("✓ DE link found in en/index.html")
    else:
        print("✗ DE link NOT found in en/index.html")
        # Show language switcher section
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'language-switcher' in line:
                print(f"\nLanguage switcher section (lines {i+1}-{i+6}):")
                for j in range(6):
                    if i+j < len(lines):
                        print(f"  {lines[i+j]}")
                break
    
    ftp.cwd('..')
    print("\nChecking es/index.html...")
    ftp.cwd('es')
    has_de, content = check_file_for_de(ftp, 'index.html')
    if has_de:
        print("✓ DE link found in es/index.html")
    else:
        print("✗ DE link NOT found in es/index.html")
        # Show language switcher section
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'language-switcher' in line:
                print(f"\nLanguage switcher section (lines {i+1}-{i+6}):")
                for j in range(6):
                    if i+j < len(lines):
                        print(f"  {lines[i+j]}")
                break
    
    ftp.quit()
except Exception as e:
    print(f"Error: {e}")

