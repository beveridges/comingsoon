#!/bin/bash
# Cron job setup script for database backups
# 
# This script sets up a daily backup of the SQLite database
# 
# To set up:
# 1. Upload this script to your server (e.g., /home/moviolab/backup_database.sh)
# 2. Make it executable: chmod +x /home/moviolab/backup_database.sh
# 3. Add to crontab: crontab -e
# 4. Add this line (runs daily at 2 AM Bogota time):
#    0 2 * * * /usr/bin/php /home/moviolab/public_html/coming-soon/backup_database.php >> /home/moviolab/backup_log.txt 2>&1
#
# Or run via the shell script:
#    0 2 * * * /home/moviolab/backup_database.sh

# Path to PHP script
PHP_SCRIPT="/home/moviolab/public_html/coming-soon/backup_database.php"

# Run the backup
/usr/bin/php "$PHP_SCRIPT"

# Optional: Email the backup file (uncomment and configure if needed)
# BACKUP_DIR="/home/moviolab/private/backups"
# LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/email_list_backup_*.sqlite | head -1)
# echo "Backup completed: $LATEST_BACKUP" | mail -s "Database Backup - $(date +%Y-%m-%d)" telemetry@moviolabs.com

