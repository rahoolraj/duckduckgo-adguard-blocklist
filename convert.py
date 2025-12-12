#!/usr/bin/env python3
"""
Convert DuckDuckGo tracker blocklist to AdGuard format.

This script fetches the DuckDuckGo Android tracker blocklist (android-tds.json)
and converts it to AdGuard blocklist format.
"""

import json
import urllib.request
import sys
from datetime import datetime, timezone

# DuckDuckGo tracker blocklist URL
DUCKDUCKGO_URL = "https://raw.githubusercontent.com/duckduckgo/tracker-blocklists/main/app/android-tds.json"

def fetch_blocklist(url):
    """Fetch the DuckDuckGo blocklist from GitHub."""
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching blocklist: {e}", file=sys.stderr)
        sys.exit(1)

def convert_to_adguard(data):
    """
    Convert DuckDuckGo tracker data to AdGuard format.
    
    AdGuard format uses ||domain^ syntax to block domains.
    We only include domains with "default": "block" action.
    """
    blocklist = []
    trackers = data.get('trackers', {})
    
    for domain, info in sorted(trackers.items()):
        # Only include domains that should be blocked
        if info.get('default') == 'block':
            # AdGuard format: ||domain^
            blocklist.append(f"||{domain}^")
    
    return blocklist

def generate_header(version):
    """Generate header for the blocklist file."""
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    header = [
        "! Title: DuckDuckGo Tracker Blocklist (AdGuard Format)",
        "! Description: DuckDuckGo's App Tracking Protection blocklist converted to AdGuard format",
        "! Homepage: https://github.com/rahoolraj/duckduckgo-adguard-blocklist",
        "! Source: https://github.com/duckduckgo/tracker-blocklists",
        f"! Version: {version}",
        f"! Last modified: {timestamp}",
        "! Expires: 1 day",
        "!",
        "! This list is automatically generated from DuckDuckGo's tracker blocklist.",
        "! It contains domains that should be blocked to prevent app tracking.",
        "!"
    ]
    return header

def main():
    """Main function to orchestrate the conversion."""
    print("Fetching DuckDuckGo tracker blocklist...")
    data = fetch_blocklist(DUCKDUCKGO_URL)
    
    version = data.get('version', 'unknown')
    print(f"Blocklist version: {version}")
    
    print("Converting to AdGuard format...")
    blocklist = convert_to_adguard(data)
    
    print(f"Converted {len(blocklist)} domains")
    
    # Generate output
    output_file = "adguard-blocklist.txt"
    with open(output_file, 'w') as f:
        # Write header
        for line in generate_header(version):
            f.write(line + '\n')
        f.write('\n')
        
        # Write blocklist
        for domain in blocklist:
            f.write(domain + '\n')
    
    print(f"Blocklist saved to {output_file}")
    
    # Also save version for CI/CD tracking
    with open("version.txt", 'w') as f:
        f.write(str(version))
    
    print("Conversion complete!")

if __name__ == "__main__":
    main()
