# DuckDuckGo AdGuard Blocklist

A blocklist that contains DuckDuckGo's App Tracking Protection blocklist converted to AdGuard format.

## About

This repository automatically converts [DuckDuckGo's tracker blocklist](https://github.com/duckduckgo/tracker-blocklists) (used in their App Tracking Protection feature) into a format that can be used with AdGuard and other ad blockers that support AdGuard syntax.

The blocklist is automatically updated daily via GitHub Actions whenever DuckDuckGo updates their source list.

## Usage

### Subscribe to the Blocklist

Add the following URL to your AdGuard or compatible ad blocker:

```
https://raw.githubusercontent.com/rahoolraj/duckduckgo-adguard-blocklist/main/adguard-blocklist.txt
```

### AdGuard Setup

1. Open AdGuard settings
2. Navigate to Filters → Custom filters
3. Add a new custom filter
4. Paste the URL above
5. Save and enable the filter

## How It Works

1. **Conversion Script** (`convert.py`): 
   - Fetches the latest `android-tds.json` from DuckDuckGo's tracker-blocklists repository
   - Extracts domains marked with `"default": "block"`
   - Converts them to AdGuard format (`||domain^`)
   - Generates `adguard-blocklist.txt` with appropriate headers

2. **Automated Updates** (`.github/workflows/update-blocklist.yml`):
   - Runs daily at midnight UTC
   - Executes the conversion script
   - Commits and pushes changes if the blocklist has been updated
   - Can also be triggered manually

## Manual Conversion

To manually run the conversion script:

```bash
python3 convert.py
```

This will generate `adguard-blocklist.txt` in the current directory.

## Source

- DuckDuckGo Tracker Blocklists: https://github.com/duckduckgo/tracker-blocklists
- Original Android TDS file: https://github.com/duckduckgo/tracker-blocklists/blob/main/app/android-tds.json

## License

MIT License - See [LICENSE](LICENSE) file for details.

The source data is provided by DuckDuckGo and is subject to their licensing terms.
