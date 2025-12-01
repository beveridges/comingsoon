#!/usr/bin/env python3
"""
Check what files are actually on the server in /downloads/
"""

import ftplib

# FTP Configuration
FTP_HOST = 'ftp.moviolabs.com'
FTP_USER = 'moviolab'
FTP_PASS = 'xTQSz1g,n2we'
FTP_PORT = 21

def main():
    print("=" * 60)
    print("Checking /public_html/downloads/ on server")
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
                return
        
        print("✓ In /public_html/downloads/ directory")
        print()
        
        # List ALL files including hidden ones
        print("Files in /downloads/ directory:")
        print("-" * 60)
        try:
            # Use MLSD for detailed listing
            files = []
            ftp.retrlines('LIST', files.append)
            for line in files:
                print(line)
        except:
            # Fallback to NLST
            files = ftp.nlst()
            for f in files:
                print(f"  - {f}")
        
        print()
        print("-" * 60)
        
        # Check for .htaccess
        print("\nChecking for .htaccess...")
        try:
            ftp.retrbinary('RETR .htaccess', lambda x: None)
            print("✓ .htaccess exists")
        except:
            print("✗ .htaccess NOT FOUND or not readable")
        
        # Check for index files
        print("\nChecking for index files...")
        for index_file in ['index.php', 'index.html', 'index.htm']:
            try:
                ftp.retrbinary(f'RETR {index_file}', lambda x: None)
                print(f"✓ {index_file} exists")
            except:
                print(f"✗ {index_file} NOT FOUND")
        
        # Check parent directory for .htaccess
        print("\nChecking parent directory (/public_html/) for .htaccess...")
        try:
            ftp.cwd('..')
            try:
                ftp.retrbinary('RETR .htaccess', lambda x: None)
                print("⚠️  WARNING: .htaccess exists in parent directory!")
                print("   This might be overriding the downloads/.htaccess")
            except:
                print("✓ No .htaccess in parent directory")
        except:
            print("Could not check parent directory")
        
    finally:
        ftp.quit()
        print("\nDisconnected from FTP server.")

if __name__ == '__main__':
    main()

