#!/usr/bin/env python3
"""
Test what the server actually returns for /downloads/
"""

import urllib.request
import urllib.error

def test_url(url):
    """Test what a URL returns"""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
            content_type = response.headers.get('Content-Type', '')
            status = response.getcode()
            
            print(f"Status Code: {status}")
            print(f"Content-Type: {content_type}")
            print(f"Content Length: {len(content)} bytes")
            print()
            print("First 500 characters of response:")
            print("-" * 60)
            print(content[:500])
            print("-" * 60)
            
            # Check if it's HTML or directory listing
            if 'Index of' in content or '<title>Index of' in content:
                print("\n⚠️  SERVER IS STILL RETURNING DIRECTORY LISTING!")
                print("   The index files are being ignored by the server.")
            elif 'redirecting' in content.lower() or 'coming-soon' in content.lower():
                print("\n✓ Server is returning index.html (redirect page)")
            elif '<html' in content.lower():
                print("\n✓ Server is returning HTML (likely index file)")
            else:
                print("\n? Unknown response type")
                
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    print("=" * 60)
    print("Testing: https://www.moviolabs.com/downloads/")
    print("=" * 60)
    print()
    test_url('https://www.moviolabs.com/downloads/')

