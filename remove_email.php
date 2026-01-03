<?php
header('Content-Type: text/plain');

// Set timezone to Bogota, Colombia
date_default_timezone_set('America/Bogota');

// Load configuration
$config = require __DIR__ . '/config.php';

$email = $_POST['email'] ?? '';

// Validate email
if (empty($email)) {
    echo "Error: Email address is required.";
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Error: Invalid email address.";
    exit;
}

// Normalize email (lowercase, trim)
$email = strtolower(trim($email));

// Connect to database
try {
    $db = new PDO('sqlite:' . $config['db_path']);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Add columns if they don't exist (for existing databases)
    try {
        $db->exec("ALTER TABLE emails ADD COLUMN removal_requested_at DATETIME");
    } catch (PDOException $e) {
        // Column might already exist, ignore error
    }
    
    try {
        $db->exec("ALTER TABLE emails ADD COLUMN cnx_req INTEGER DEFAULT 0");
    } catch (PDOException $e) {
        // Column might already exist, ignore error
    }
    
    // Check if email exists
    $stmt = $db->prepare("SELECT id, removal_requested_at, cnx_req, created_at FROM emails WHERE email = ?");
    $stmt->execute([$email]);
    $row = $stmt->fetch(PDO::FETCH_ASSOC);
    
    if (!$row) {
        echo "This email address is not in our database.";
        exit;
    }
    
    // Check if already marked for removal
    if ($row['cnx_req'] == 1 || $row['removal_requested_at']) {
        echo "Success: Your email address has already been marked for removal from our list.";
        exit;
    }
    
    // Mark email for removal (add tick in cnx_req column and timestamp)
    $stmt = $db->prepare("UPDATE emails SET cnx_req = 1, removal_requested_at = CURRENT_TIMESTAMP WHERE email = ?");
    $stmt->execute([$email]);
    
    if ($stmt->rowCount() > 0) {
        // Send email notification if enabled
        if (!empty($config['notification_email']) && !empty($config['notification_enabled']) && $config['notification_enabled']) {
            $to = $config['notification_email'];
            $subject = "Email Removal Request - MOVIOLABS";
            $message = "A user has requested removal from the email list.\n\n";
            $message .= "Email: " . $email . "\n";
            $message .= "Removal Requested: " . date('Y-m-d H:i:s') . " (Bogota time)\n";
            $message .= "Original Registration Date: " . ($row['created_at'] ?? 'N/A') . "\n\n";
            $message .= "View all emails: https://www.moviolabs.com/coming-soon/view_emails.php\n";
            
            $headers = "From: Moviolabs <noreply@moviolabs.com>\r\n";
            $headers .= "Reply-To: noreply@moviolabs.com\r\n";
            $headers .= "X-Mailer: PHP/" . phpversion();
            
            @mail($to, $subject, $message, $headers);
        }
        
        echo "Success: Your email address has been removed from our list.";
    } else {
        echo "Error: Could not remove email address.";
    }
    
} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    echo "Error: Could not process your request. Please try again later.";
}

