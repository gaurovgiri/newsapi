# Automation Guide

Complete guide to automating news scraping with various scheduling methods.

## 🤖 GitHub Actions (Recommended)

The project includes a GitHub Actions workflow that automatically runs every 4 hours.

### Current Setup

The workflow file (`.github/workflows/scrape-news.yml`) is already configured:

```yaml
name: Scrape News

on:
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours
  workflow_dispatch:        # Manual trigger
  push:
    branches: [ main, master ]
```

### How It Works

1. **Runs every 4 hours** automatically
2. **Checks out repository** with full history
3. **Installs Python dependencies**
4. **Runs the scraper** (`python main.py`)
5. **Commits new data** to `data/` directory
6. **Pushes changes** back to the repository

### Manual Trigger

You can manually trigger the workflow:

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Scrape News" workflow
4. Click "Run workflow" button

### View Logs

1. Go to "Actions" tab
2. Click on any workflow run
3. View detailed logs for each step

### Customizing Schedule

Edit `.github/workflows/scrape-news.yml`:

```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
    - cron: '0 8 * * *'    # Daily at 8 AM UTC
    - cron: '0 0,12 * * *' # Twice daily (midnight and noon)
```

**Cron Format**: `minute hour day month weekday`

Examples:
- `0 * * * *` - Every hour
- `0 0 * * *` - Daily at midnight
- `0 6,18 * * *` - Twice daily (6 AM and 6 PM)
- `0 9 * * 1-5` - Weekdays at 9 AM

**Useful tool**: [crontab.guru](https://crontab.guru) - Cron schedule expression editor

---

## 🐧 Linux/macOS Automation

### Method 1: Cron Job (Recommended)

#### Setup

```bash
# Open crontab editor
crontab -e

# Add one of these lines:

# Daily at 6 AM
0 6 * * * cd /path/to/newsapi && /usr/bin/python3 main.py

# Every 4 hours
0 */4 * * * cd /path/to/newsapi && /usr/bin/python3 main.py

# Twice daily (6 AM and 6 PM)
0 6,18 * * * cd /path/to/newsapi && /usr/bin/python3 main.py

# With logging
0 6 * * * cd /path/to/newsapi && /usr/bin/python3 main.py >> /var/log/newsapi.log 2>&1
```

#### Find Python Path

```bash
which python3
# Output: /usr/bin/python3 or /usr/local/bin/python3
```

#### View Cron Jobs

```bash
# List all cron jobs
crontab -l

# Check cron logs (Debian/Ubuntu)
grep CRON /var/log/syslog

# Check cron logs (RedHat/CentOS)
grep CRON /var/log/cron
```

#### Remove Cron Job

```bash
# Edit and delete the line
crontab -e

# Or remove all cron jobs
crontab -r
```

### Method 2: systemd Timer

Create a more robust scheduled task using systemd.

#### Create Service File

```bash
sudo nano /etc/systemd/system/newsapi-scraper.service
```

```ini
[Unit]
Description=Nepali News API Scraper
After=network-online.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/newsapi
ExecStart=/usr/bin/python3 /path/to/newsapi/main.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### Create Timer File

```bash
sudo nano /etc/systemd/system/newsapi-scraper.timer
```

```ini
[Unit]
Description=Run Nepali News Scraper every 4 hours
Requires=newsapi-scraper.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=4h
Persistent=true

[Install]
WantedBy=timers.target
```

#### Enable and Start

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable timer (start on boot)
sudo systemctl enable newsapi-scraper.timer

# Start timer now
sudo systemctl start newsapi-scraper.timer

# Check status
sudo systemctl status newsapi-scraper.timer

# View logs
journalctl -u newsapi-scraper.service -f
```

#### Manage Timer

```bash
# Stop timer
sudo systemctl stop newsapi-scraper.timer

# Disable timer
sudo systemctl disable newsapi-scraper.timer

# Run service manually
sudo systemctl start newsapi-scraper.service
```

---

## 🪟 Windows Automation

### Method 1: Task Scheduler (GUI)

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**
   - Click "Create Basic Task" in right panel
   - Name: "Nepali News Scraper"
   - Description: "Automatically scrape Nepali news"

3. **Set Trigger**
   - Choose "Daily" or "Weekly"
   - Set time and recurrence

4. **Set Action**
   - Choose "Start a program"
   - Program: `python.exe` or `C:\Python311\python.exe`
   - Arguments: `main.py`
   - Start in: `C:\path\to\newsapi`

5. **Finish**
   - Review settings
   - Click "Finish"

### Method 2: Task Scheduler (Command Line)

```powershell
# Daily at 6 AM
schtasks /create /tn "Nepali News Scraper" /tr "python C:\path\to\newsapi\main.py" /sc daily /st 06:00

# Every 4 hours
schtasks /create /tn "Nepali News Scraper" /tr "python C:\path\to\newsapi\main.py" /sc hourly /mo 4

# With specific user
schtasks /create /tn "Nepali News Scraper" /tr "python C:\path\to\newsapi\main.py" /sc daily /st 06:00 /ru "DOMAIN\username" /rp password
```

### View Scheduled Tasks

```powershell
# List all tasks
schtasks /query

# View specific task
schtasks /query /tn "Nepali News Scraper" /fo list /v
```

### Modify Task

```powershell
# Change schedule to every 6 hours
schtasks /change /tn "Nepali News Scraper" /sc hourly /mo 6

# Change start time
schtasks /change /tn "Nepali News Scraper" /st 08:00
```

### Delete Task

```powershell
schtasks /delete /tn "Nepali News Scraper" /f
```

### Method 3: PowerShell Script

Create `run_scraper.ps1`:

```powershell
# Navigate to project directory
Set-Location "C:\path\to\newsapi"

# Activate virtual environment (if using)
# .\venv\Scripts\Activate.ps1

# Run scraper
python main.py

# Log output
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path "scraper.log" -Value "[$timestamp] Scraper completed"
```

Schedule this script:

```powershell
schtasks /create /tn "Nepali News Scraper" /tr "powershell.exe -File C:\path\to\newsapi\run_scraper.ps1" /sc daily /st 06:00
```

---

## 🐳 Docker Automation

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create data directory
RUN mkdir -p data

# Run scraper
CMD ["python", "main.py"]
```

### Docker Compose with Cron

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  scraper:
    build: .
    volumes:
      - ./data:/app/data
    environment:
      - TZ=Asia/Kathmandu
    restart: unless-stopped
    # Run as a cron job inside container
    entrypoint: >
      sh -c "
      echo '0 */4 * * * cd /app && python main.py' > /etc/crontabs/root &&
      crond -f
      "
```

### Build and Run

```bash
# Build image
docker build -t newsapi-scraper .

# Run once
docker run --rm -v $(pwd)/data:/app/data newsapi-scraper

# Run with cron (using alpine)
docker run -d --name newsapi-cron \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  alpine sh -c "apk add --no-cache python3 py3-pip && \
  pip3 install requests beautifulsoup4 lxml && \
  echo '0 */4 * * * cd /app && python3 main.py' > /etc/crontabs/root && \
  crond -f"
```

---

## ☁️ Cloud Automation

### AWS Lambda

1. **Package project**
```bash
pip install -r requirements.txt -t package/
cp main.py news_source.py package/
cp -r sources package/
cd package && zip -r ../lambda.zip . && cd ..
```

2. **Create Lambda function**
   - Runtime: Python 3.11
   - Handler: `main.lambda_handler`
   - Upload `lambda.zip`

3. **Add EventBridge trigger**
   - Rate: `rate(4 hours)`
   - Or cron: `cron(0 */4 * * ? *)`

### Google Cloud Functions

```bash
# Deploy
gcloud functions deploy newsapi-scraper \
  --runtime python311 \
  --trigger-topic scrape-news \
  --entry-point main

# Schedule with Cloud Scheduler
gcloud scheduler jobs create pubsub scrape-news-job \
  --schedule="0 */4 * * *" \
  --topic=scrape-news \
  --message-body="trigger"
```

### Heroku

1. **Create `Procfile`**
```
worker: python main.py
```

2. **Deploy**
```bash
heroku create
git push heroku main
```

3. **Add scheduler**
```bash
heroku addons:create scheduler:standard
heroku addons:open scheduler
```

Add job: `python main.py` to run every 4 hours

---

## 📊 Monitoring

### Check if Automation is Working

```bash
# Check last update time
ls -lh data/today.json

# Check file modification time
stat data/today.json

# View recent git commits
git log --oneline -n 10

# Check scrape timestamp in JSON
cat data/today.json | jq '.scrape_time'
```

### Email Notifications

Add to your script:

```python
import smtplib
from email.message import EmailMessage

def send_notification(status, message):
    msg = EmailMessage()
    msg['Subject'] = f'News Scraper: {status}'
    msg['From'] = 'scraper@example.com'
    msg['To'] = 'admin@example.com'
    msg.set_content(message)
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('user@gmail.com', 'password')
        smtp.send_message(msg)

# Use in main.py
try:
    scraper.run()
    send_notification('Success', f'Scraped {total} articles')
except Exception as e:
    send_notification('Failed', str(e))
```

### Logging

Add to your cron job:

```bash
# Log with timestamps
0 */4 * * * cd /path/to/newsapi && /usr/bin/python3 main.py 2>&1 | ts '[%Y-%m-%d %H:%M:%S]' >> /var/log/newsapi.log

# Rotate logs (keep last 7 days)
0 0 * * * find /var/log/newsapi.log -mtime +7 -delete
```

---

## 🔧 Troubleshooting

### Cron Job Not Running

```bash
# Check if cron daemon is running
sudo systemctl status cron  # Debian/Ubuntu
sudo systemctl status crond # RedHat/CentOS

# Check cron logs
tail -f /var/log/syslog | grep CRON

# Test script manually
cd /path/to/newsapi && /usr/bin/python3 main.py
```

### Permission Issues

```bash
# Make script executable
chmod +x main.py

# Check file ownership
ls -la main.py

# Fix ownership
chown username:username main.py
```

### Environment Variables

Cron doesn't load your shell environment. Use full paths:

```bash
# Bad (won't work in cron)
python main.py

# Good (works in cron)
/usr/bin/python3 /full/path/to/newsapi/main.py
```

---

## 📝 Best Practices

✅ **Use absolute paths** in cron jobs  
✅ **Log outputs** for debugging  
✅ **Test manually** before scheduling  
✅ **Monitor regularly** to catch failures  
✅ **Set up notifications** for critical errors  
✅ **Use timezones** appropriately (UTC vs local)  
✅ **Respect rate limits** - don't scrape too frequently  

---

**Need help?** Open an issue on [GitHub](https://github.com/gaurovgiri/newsapi/issues).
