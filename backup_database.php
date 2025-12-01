<?php
/**
 * SQLite Database Backup Script
 * 
 * This script creates a backup of the email database.
 * Can be run manually or via cron job.
 * 
 * Usage:
 *   - Via browser: https://www.moviolabs.com/coming-soon/backup_database.php
 *   - Via cron: php /path/to/backup_database.php
 *   - Via SSH: php backup_database.php
 */

// Set timezone
date_default_timezone_set('America/Bogota');

// Load configuration
$config = require __DIR__ . '/config.php';
$db_path = $config['db_path'];

// If db_path is a placeholder, use local database.sqlite
if (strpos($db_path, 'YOUR_ACCOUNT') !== false) {
    $db_path = __DIR__ . '/database.sqlite';
}

// Backup settings
$backup_dir = dirname($db_path) . '/backups'; // Store backups in same directory as database
$backup_filename = 'email_list_backup_' . date('Y-m-d_His') . '.sqlite';
$backup_path = $backup_dir . '/' . $backup_filename;

// Number of backups to keep (delete older ones)
$keep_backups = 30; // Keep last 30 backups

// Create backup directory if it doesn't exist
if (!is_dir($backup_dir)) {
    mkdir($backup_dir, 0755, true);
}

// Check if database exists
if (!file_exists($db_path)) {
    die("Error: Database file not found at: $db_path\n");
}

// Copy database file
if (copy($db_path, $backup_path)) {
    // Set permissions
    chmod($backup_path, 0644);
    
    $backup_size = filesize($backup_path);
    $backup_size_mb = round($backup_size / 1024 / 1024, 2);
    
    // Clean up old backups (keep only the most recent N backups)
    $backups = glob($backup_dir . '/email_list_backup_*.sqlite');
    if (count($backups) > $keep_backups) {
        // Sort by modification time (newest first)
        usort($backups, function($a, $b) {
            return filemtime($b) - filemtime($a);
        });
        
        // Delete oldest backups
        $backups_to_delete = array_slice($backups, $keep_backups);
        foreach ($backups_to_delete as $old_backup) {
            unlink($old_backup);
        }
    }
    
    // Output result
    if (php_sapi_name() === 'cli') {
        // Command line output
        echo "✓ Backup created successfully!\n";
        echo "  Location: $backup_path\n";
        echo "  Size: $backup_size_mb MB\n";
        echo "  Date: " . date('Y-m-d H:i:s T') . "\n";
    } else {
        // Web output
        header('Content-Type: text/html; charset=utf-8');
        ?>
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Database Backup</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #0d1117;
                    color: #e6edf3;
                }
                .success {
                    background: #238636;
                    color: white;
                    padding: 20px;
                    border-radius: 6px;
                    margin-bottom: 20px;
                }
                .info {
                    background: #161b22;
                    border: 1px solid #30363d;
                    padding: 15px;
                    border-radius: 6px;
                    margin: 10px 0;
                }
                .info strong {
                    color: #1e90ff;
                }
                a {
                    color: #1e90ff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="success">
                <h2>✓ Backup Created Successfully!</h2>
            </div>
            
            <div class="info">
                <strong>Backup Location:</strong><br>
                <?php echo htmlspecialchars($backup_path); ?>
            </div>
            
            <div class="info">
                <strong>Backup Size:</strong> <?php echo $backup_size_mb; ?> MB
            </div>
            
            <div class="info">
                <strong>Date/Time (Bogota):</strong> <?php echo date('Y-m-d H:i:s T'); ?>
            </div>
            
            <div class="info">
                <strong>Total Backups Kept:</strong> <?php echo min(count($backups), $keep_backups); ?>
            </div>
            
            <p style="margin-top: 20px;">
                <a href="view_emails.php">← Back to Email Viewer</a>
            </p>
        </body>
        </html>
        <?php
    }
} else {
    $error = "Error: Failed to create backup. Check file permissions.";
    if (php_sapi_name() === 'cli') {
        echo "$error\n";
    } else {
        header('Content-Type: text/html; charset=utf-8');
        echo "<html><body style='font-family: Arial; padding: 20px;'><h2 style='color: red;'>$error</h2></body></html>";
    }
    exit(1);
}
?>

