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
    
    // Check if email exists
    $stmt = $db->prepare("SELECT COUNT(*) FROM emails WHERE email = ?");
    $stmt->execute([$email]);
    $exists = $stmt->fetchColumn() > 0;
    
    if (!$exists) {
        echo "This email address is not in our database.";
        exit;
    }
    
    // Remove email from database
    $stmt = $db->prepare("DELETE FROM emails WHERE email = ?");
    $stmt->execute([$email]);
    
    if ($stmt->rowCount() > 0) {
        echo "Success: Your email address has been removed from our list.";
    } else {
        echo "Error: Could not remove email address.";
    }
    
} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    echo "Error: Could not process your request. Please try again later.";
}

