## About the project

This simple Python script will always pull some lastest X emails from your mailbox every 10 seconds and then send a notification via LINE when it found a new ticket email.

Useful for some traditional ticket systems that do not provide APIs and LINE integration.

### Tested with
- Office365's IMAP server
- Python 3.9.2
- beautifulsoup4 (v4.9.3)
- requests (v2.25.1)

### Installation and Usage
1. Install beautifulsoup4 and requests
   ```sh
   pip install -r requirements.txt
   ```

2. Fill all variables below in ```run.py```
- EMAIL = 'your-email'
- PASSWORD = 'your-email-password'
- SERVER = 'your-imap-server'
- FILTER_FROM = 'filter-all-emails-from-X'
- FILTER_HEADER = 'filter-the-header-that-contains-X'

3. Paste your LINE token at ```line 6``` in  ```notifications.py```

4. Modify the ```extract_html``` function in ```run.py``` to match with your email body

5. Run the script
   ```sh
   python run.py
   ```
