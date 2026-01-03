<?php
header('Content-Type: text/plain');

// Set timezone to Bogota, Colombia
date_default_timezone_set('America/Bogota');

// Load configuration
$config = require __DIR__ . '/config.php';

$email = $_POST['email'] ?? '';
$recaptcha_token = $_POST['recaptcha_token'] ?? '';

// Get client IP address (handles proxies)
function getClientIP() {
    $ip_keys = ['HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED', 'HTTP_X_CLUSTER_CLIENT_IP', 'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED', 'REMOTE_ADDR'];
    foreach ($ip_keys as $key) {
        if (array_key_exists($key, $_SERVER) === true) {
            foreach (explode(',', $_SERVER[$key]) as $ip) {
                $ip = trim($ip);
                if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) !== false) {
                    return $ip;
                }
            }
        }
    }
    return $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
}

$client_ip = getClientIP();

// Validate email format
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo "Invalid email address.";
    exit;
}

// Additional email validation: check for suspicious patterns
$email_lower = strtolower($email);
$suspicious_patterns = [
    'test@test', 'example@example', 'admin@', 'root@', 'postmaster@',
    'noreply@', 'no-reply@', 'mailer-daemon@'
];
foreach ($suspicious_patterns as $pattern) {
    if (strpos($email_lower, $pattern) !== false) {
        echo "Invalid email address.";
        exit;
    }
}

// Check email length (prevent extremely long strings)
if (strlen($email) > 254) {
    echo "Invalid email address.";
    exit;
}

// Verify reCAPTCHA token
if (empty($recaptcha_token)) {
    echo "reCAPTCHA verification failed.";
    exit;
}

$recaptcha_secret = $config['recaptcha_secret'];
$recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify';
$recaptcha_data = [
    'secret' => $recaptcha_secret,
    'response' => $recaptcha_token
];

$recaptcha_options = [
    'http' => [
        'method' => 'POST',
        'header' => 'Content-Type: application/x-www-form-urlencoded',
        'content' => http_build_query($recaptcha_data)
    ]
];

$recaptcha_context = stream_context_create($recaptcha_options);
$recaptcha_response = file_get_contents($recaptcha_url, false, $recaptcha_context);
$recaptcha_result = json_decode($recaptcha_response, true);

if (!$recaptcha_result || !isset($recaptcha_result['success']) || !$recaptcha_result['success']) {
    echo "reCAPTCHA verification failed. Please try again.";
    exit;
}

// Check reCAPTCHA score (if using v3, score should be > 0.5)
if (isset($recaptcha_result['score']) && $recaptcha_result['score'] < 0.5) {
    echo "reCAPTCHA verification failed. Please try again.";
    exit;
}

// Save email to database
try {
    $db_path = $config['db_path'];
    
    // If db_path is a placeholder, use local database.sqlite
    if (strpos($db_path, 'YOUR_ACCOUNT') !== false) {
        $db_path = __DIR__ . '/database.sqlite';
    }
    
    $db = new PDO('sqlite:' . $db_path);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Create tables if they don't exist
    $db->exec("CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        ip_address TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        removal_requested_at DATETIME,
        cnx_req INTEGER DEFAULT 0
    )");
    
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
    
    $db->exec("CREATE TABLE IF NOT EXISTS rate_limits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL,
        submission_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(ip_address, submission_time)
    )");
    
    // Rate limiting: Check submissions in the last hour
    $rate_limit_hour = $config['rate_limit_per_hour'] ?? 5;
    $stmt = $db->prepare("SELECT COUNT(*) as count FROM rate_limits WHERE ip_address = :ip AND submission_time > datetime('now', '-1 hour')");
    $stmt->execute([':ip' => $client_ip]);
    $hour_count = $stmt->fetch(PDO::FETCH_ASSOC)['count'];
    
    if ($hour_count >= $rate_limit_hour) {
        echo "Too many requests. Please try again later.";
        exit;
    }
    
    // Rate limiting: Check submissions in the last 24 hours
    $rate_limit_day = $config['rate_limit_per_day'] ?? 20;
    $stmt = $db->prepare("SELECT COUNT(*) as count FROM rate_limits WHERE ip_address = :ip AND submission_time > datetime('now', '-24 hours')");
    $stmt->execute([':ip' => $client_ip]);
    $day_count = $stmt->fetch(PDO::FETCH_ASSOC)['count'];
    
    if ($day_count >= $rate_limit_day) {
        echo "Too many requests. Please try again later.";
        exit;
    }
    
    // Insert email
    // Check if email was previously marked for removal
    $stmt_check = $db->prepare("SELECT removal_requested_at, cnx_req FROM emails WHERE email = :email");
    $stmt_check->execute([':email' => $email]);
    $existing = $stmt_check->fetch(PDO::FETCH_ASSOC);
    
    if ($existing && ($existing['removal_requested_at'] || $existing['cnx_req'] == 1)) {
        // Email was previously marked for removal, don't re-add it
        echo "This email address was previously removed from our list.";
        exit;
    }
    
    // Insert email (or ignore if already exists and not marked for removal)
    $stmt_email = $db->prepare("INSERT OR IGNORE INTO emails (email, ip_address) VALUES (:email, :ip)");
    $stmt_email->execute([':email' => $email, ':ip' => $client_ip]);
    $email_inserted = $stmt_email->rowCount() > 0;
    
    // Record rate limit entry
    $stmt = $db->prepare("INSERT OR IGNORE INTO rate_limits (ip_address) VALUES (:ip)");
    $stmt->execute([':ip' => $client_ip]);
    
    // Clean up old rate limit entries (older than 24 hours)
    $db->exec("DELETE FROM rate_limits WHERE submission_time < datetime('now', '-24 hours')");
    
    if ($email_inserted) {
        // Send email notification
        if ($config['notification_enabled'] ?? true) {
            sendEmailNotification($email, $client_ip, $config['notification_email'] ?? 'telemetry@moviolabs.com');
        }
        
        echo "Thanks! You'll be notified when we launch.";
    } else {
        echo "This email is already registered. Thanks!";
    }
} catch (Exception $e) {
    error_log("Database error: " . $e->getMessage());
    echo "Error saving email. Please try again later.";
}

/**
 * Send email notification when a new email is registered
 */
function sendEmailNotification($email, $ip_address, $to_email) {
    $subject = "New Email Registration - Moviolabs Coming Soon";
    
    // Format date in Bogota timezone
    $date = new DateTime('now', new DateTimeZone('America/Bogota'));
    $date_str = $date->format('Y-m-d H:i:s T');
    
    $message = "A new email has been registered on the Moviolabs Coming Soon page.\n\n";
    $message .= "Email: " . $email . "\n";
    $message .= "IP Address: " . $ip_address . "\n";
    $message .= "Date/Time (Bogota): " . $date_str . "\n";
    $message .= "\n";
    $message .= "Total registrations can be viewed at:\n";
    $message .= "https://www.moviolabs.com/coming-soon/view_emails.php\n";
    
    $headers = "From: Moviolabs <noreply@moviolabs.com>\r\n";
    $headers .= "Reply-To: noreply@moviolabs.com\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    
    // Send email (silently fail if mail server not configured)
    @mail($to_email, $subject, $message, $headers);
}
?>
