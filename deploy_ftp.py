#!/usr/bin/env python3
"""
FTP Deployment Script for MOVIOLABS Coming Soon Site

Fill in your FTP credentials below, then run:
    python deploy_ftp.py
"""

import ftplib
import os
from pathlib import Path

# ============================================
# FTP CONFIGURATION - FILL IN YOUR DETAILS
# ============================================
FTP_HOST = 'ftp.moviolabs.com'  # e.g., 'ftp.moviolabs.com' or IP address
FTP_USER = 'moviolab'        # Your FTP username
FTP_PASS = 'xTQSz1g,n2we'         # Your FTP password
FTP_PORT = 21                      # Usually 21, or 22 for SFTP (requires different library)

# Server paths
REMOTE_WEB_ROOT = '/public_html/coming-soon'  # Where your site files go
REMOTE_PRIVATE_DIR = '/private'               # Where .htaccess goes (outside public_html)

# ============================================
# Files and directories to upload
# ============================================
FILES_TO_UPLOAD = [
    'save_email.php',
    'config.php',  # You'll need to edit this on server with correct database path
    'remove_email.php',
    'view_emails.php',
    'detect_language.php',
    'coming-soon-index.php',
]

# Root-level files (upload to /public_html/, not /coming-soon/)
ROOT_FILES = [
    'index.php',   # Root redirect to coming-soon (instant server-side redirect)
    '.htaccess',   # Ensure index.php is served first
]

DIRS_TO_UPLOAD = [
    'css',
    'js',
    'img',
    'fonts',
    'video',
    'en',
    'es',
    'de',
]

# Files to exclude (already in .gitignore, but being explicit)
EXCLUDE_PATTERNS = [
    '.git',
    '.gitignore',
    '.DS_Store',
    'Thumbs.db',
    'desktop.ini',
    '*.sqlite',
    '*.sqlite3',
    '*.log',
    'error_log',
    '__pycache__',
    '*.pyc',
    '*.afdesign',
    'deploy_ftp.py',
    'DEPLOYMENT.md',
]

# ============================================
# Deployment Functions
# ============================================

def should_exclude(filepath):
    """Check if file should be excluded from upload"""
    name = os.path.basename(filepath)
    
    # Check for exact matches or patterns
    for pattern in EXCLUDE_PATTERNS:
        # Handle wildcard patterns (e.g., *.sqlite, *.afdesign)
        if pattern.startswith('*.'):
            extension = pattern[1:]  # Remove the *
            if name.endswith(extension):
                return True
        # Handle exact matches
        elif pattern in name:
            return True
    
    # Exclude hidden files (starting with .)
    if name.startswith('.'):
        return True
    
    return False

def ensure_remote_directory(ftp, remote_dir):
    """Ensure a remote directory exists, creating it if necessary (relative to current dir)"""
    if not remote_dir or remote_dir == '.':
        return True
    
    # Get current directory
    try:
        current_dir = ftp.pwd()
    except:
        current_dir = '/'
    
    # Split directory path into parts
    parts = [p for p in remote_dir.replace('\\', '/').split('/') if p]
    
    # Navigate/create each part
    for part in parts:
        try:
            # Try to change to the directory
            ftp.cwd(part)
        except:
            # Directory doesn't exist, create it
            try:
                ftp.mkd(part)
                ftp.cwd(part)
            except Exception as e:
                # Directory might have been created by another process, try to cd
                try:
                    ftp.cwd(part)
                except:
                    print(f"⚠️  Warning: Could not create/access directory {part}: {e}")
                    # Return to original directory
                    try:
                        ftp.cwd(current_dir)
                    except:
                        pass
                    return False
    
    # Return to original directory
    try:
        ftp.cwd(current_dir)
    except:
        pass
    
    return True

def upload_file(ftp, local_path, remote_path):
    """Upload a single file"""
    try:
        # Get current directory to return to later
        try:
            original_dir = ftp.pwd()
        except:
            original_dir = '/'
        
        # Create remote directory if needed (relative path)
        remote_dir = os.path.dirname(remote_path).replace('\\', '/')
        if remote_dir and remote_dir != '.':
            if not ensure_remote_directory(ftp, remote_dir):
                return False
        
        # Make sure we're back in the original directory
        try:
            ftp.cwd(original_dir)
        except:
            pass
        
        # Upload file (use just the filename if we're in the right directory, or full path)
        filename = os.path.basename(remote_path)
        remote_dir_part = os.path.dirname(remote_path).replace('\\', '/')
        
        # If there's a directory, change to it first
        if remote_dir_part and remote_dir_part != '.':
            try:
                ftp.cwd(remote_dir_part)
                store_path = filename
            except:
                # If we can't cd, try full path
                store_path = remote_path.replace('\\', '/')
        else:
            store_path = filename
        
        # Upload file
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {store_path}', f)
        
        # Return to original directory
        try:
            ftp.cwd(original_dir)
        except:
            pass
        
        print(f"✓ Uploaded: {remote_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to upload {remote_path}: {e}")
        return False

def upload_directory(ftp, local_dir, remote_base):
    """Recursively upload a directory"""
    uploaded = 0
    failed = 0
    
    for root, dirs, files in os.walk(local_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        
        for file in files:
            if should_exclude(file):
                continue
            
            local_path = os.path.join(root, file)
            # Calculate relative path
            rel_path = os.path.relpath(local_path, local_dir)
            remote_path = f"{remote_base}/{rel_path}".replace('\\', '/')
            
            if upload_file(ftp, local_path, remote_path):
                uploaded += 1
            else:
                failed += 1
    
    return uploaded, failed

def main():
    print("=" * 60)
    print("MOVIOLABS Coming Soon - FTP Deployment Script")
    print("=" * 60)
    print()
    
    # Validate configuration
    if 'your-' in FTP_HOST or 'your-' in FTP_USER:
        print("⚠️  ERROR: Please fill in your FTP credentials in the script!")
        print("   Edit FTP_HOST, FTP_USER, and FTP_PASS at the top of this file.")
        return
    
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
        # Change to web root
        print(f"Changing to {REMOTE_WEB_ROOT}...")
        try:
            ftp.cwd(REMOTE_WEB_ROOT)
        except:
            print(f"⚠️  Directory {REMOTE_WEB_ROOT} doesn't exist. Creating...")
            # Try to create directory structure
            parts = REMOTE_WEB_ROOT.strip('/').split('/')
            current = ''
            for part in parts:
                current += '/' + part
                try:
                    ftp.cwd(current)
                except:
                    ftp.mkd(current)
                    ftp.cwd(current)
        
        print("✓ In web root directory")
        print()
        
        # Upload individual files
        print("Uploading files...")
        uploaded_files = 0
        failed_files = 0
        
        for file in FILES_TO_UPLOAD:
            if os.path.exists(file):
                if upload_file(ftp, file, file):
                    uploaded_files += 1
                else:
                    failed_files += 1
            else:
                print(f"⚠️  File not found: {file}")
        
        print()
        
        # Upload directories
        print("Uploading directories...")
        uploaded_dirs = 0
        failed_dirs = 0
        
        for dir_name in DIRS_TO_UPLOAD:
            if os.path.exists(dir_name) and os.path.isdir(dir_name):
                print(f"\nUploading {dir_name}/...")
                up, fail = upload_directory(ftp, dir_name, dir_name)
                uploaded_dirs += up
                failed_dirs += fail
            else:
                print(f"⚠️  Directory not found: {dir_name}")
        
        print()
        
        # Upload root-level files to /public_html/
        print("Uploading root-level files to /public_html/...")
        try:
            # Save current directory
            current_dir = ftp.pwd()
            
            # Navigate to /public_html
            ftp.cwd('/')
            try:
                ftp.cwd('public_html')
            except:
                # Try with leading slash
                ftp.cwd('/public_html')
            
            for file in ROOT_FILES:
                if os.path.exists(file):
                    print(f"  Uploading {file} to /public_html/...")
                    if upload_file(ftp, file, file):
                        uploaded_files += 1
                        print(f"  ✓ {file} uploaded to root")
                    else:
                        failed_files += 1
                        print(f"  ✗ Failed to upload {file}")
                else:
                    print(f"  ⚠️  File not found: {file}")
            
            # Return to coming-soon directory
            try:
                ftp.cwd(current_dir)
            except:
                ftp.cwd(REMOTE_WEB_ROOT)
        except Exception as e:
            print(f"⚠️  Could not upload root files: {e}")
            print(f"   Error details: {type(e).__name__}")
            import traceback
            traceback.print_exc()
        
        print()
        
        # Upload .htaccess to coming-soon directory
        print("Uploading .htaccess to coming-soon directory...")
        htaccess_coming_soon_local = '.htaccess-coming-soon'
        if os.path.exists(htaccess_coming_soon_local):
            # Make sure we're in coming-soon directory
            try:
                ftp.cwd(REMOTE_WEB_ROOT)
                upload_file(ftp, htaccess_coming_soon_local, '.htaccess')
                print("✓ .htaccess uploaded to coming-soon directory")
            except Exception as e:
                print(f"⚠️  Could not upload .htaccess to coming-soon: {e}")
        else:
            print("⚠️  .htaccess-coming-soon file not found")
        
        print()
        
        # Upload .htaccess to private directory
        print("Uploading .htaccess to private directory...")
        htaccess_local = 'private/.htaccess'
        if os.path.exists(htaccess_local):
            # Navigate to private directory (outside public_html)
            try:
                ftp.cwd('/')
                ftp.cwd(REMOTE_PRIVATE_DIR)
                upload_file(ftp, htaccess_local, '.htaccess')
                print("✓ .htaccess uploaded to private directory")
            except Exception as e:
                print(f"⚠️  Could not upload .htaccess to {REMOTE_PRIVATE_DIR}: {e}")
                print("   You may need to upload it manually via cPanel File Manager")
        else:
            print("⚠️  .htaccess file not found")
        
        print()
        print("=" * 60)
        print("Deployment Summary:")
        print(f"  Files uploaded: {uploaded_files}")
        print(f"  Files failed: {failed_files}")
        print(f"  Directory items uploaded: {uploaded_dirs}")
        print(f"  Directory items failed: {failed_dirs}")
        print("=" * 60)
        print()
        print("⚠️  IMPORTANT NEXT STEPS:")
        print("  1. Edit config.php on server to set correct database path")
        print("  2. Set file permissions: chmod 600 on database file")
        print("  3. Test the email submission form")
        print()
        
    finally:
        ftp.quit()
        print("Disconnected from FTP server.")

if __name__ == '__main__':
    main()

