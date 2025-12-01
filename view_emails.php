<?php
// Simple email database viewer
// IMPORTANT: Protect this file! Either password protect it or move it outside public_html

// Simple password protection (change this password!)
$admin_password = 'xTQSz1g,n2we';
$is_authenticated = false;

// Check if password is set in session or POST
session_start();
if (isset($_SESSION['admin_authenticated']) && $_SESSION['admin_authenticated'] === true) {
    $is_authenticated = true;
}

// Handle login
if (isset($_POST['password']) && $_POST['password'] === $admin_password) {
    $_SESSION['admin_authenticated'] = true;
    $is_authenticated = true;
}

// Handle logout
if (isset($_GET['logout'])) {
    session_destroy();
    $is_authenticated = false;
}

// Set timezone
date_default_timezone_set('America/Bogota');

// Load configuration
$config = require __DIR__ . '/config.php';
$db_path = $config['db_path'];

// If db_path is a placeholder, use local database.sqlite
if (strpos($db_path, 'YOUR_ACCOUNT') !== false) {
    $db_path = __DIR__ . '/database.sqlite';
}

// Show login form if not authenticated
if (!$is_authenticated) {
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Admin Login</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 400px; 
                margin: 100px auto; 
                padding: 20px; 
                background: #0d1117;
                color: #e6edf3;
            }
            h2 {
                color: #1e90ff;
                margin-bottom: 20px;
            }
            input[type="password"], button { 
                width: 100%; 
                padding: 12px; 
                margin: 10px 0; 
                border: 1px solid #30363d;
                background: #161b22;
                color: #e6edf3;
                border-radius: 6px;
                box-sizing: border-box;
            }
            button { 
                background: #1e90ff; 
                color: white; 
                border: none; 
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: #0077cc;
            }
            .error {
                color: #f85149;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h2>Email Database Viewer - Login</h2>
        <?php if (isset($_POST['password']) && $_POST['password'] !== $admin_password): ?>
            <div class="error">Incorrect password. Please try again.</div>
        <?php endif; ?>
        <form method="POST">
            <input type="password" name="password" placeholder="Enter password" required autofocus>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    <?php
    exit;
}

// Connect to database
try {
    $db = new PDO('sqlite:' . $db_path);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Get all emails
    $stmt = $db->query("SELECT * FROM emails ORDER BY created_at DESC");
    $emails = $stmt->fetchAll(PDO::FETCH_ASSOC);
    
    // Get statistics
    $total_emails = $db->query("SELECT COUNT(*) FROM emails")->fetchColumn();
    $today_count = $db->query("SELECT COUNT(*) FROM emails WHERE DATE(created_at) = DATE('now')")->fetchColumn();
    $this_week = $db->query("SELECT COUNT(*) FROM emails WHERE created_at > datetime('now', '-7 days')")->fetchColumn();
    $this_month = $db->query("SELECT COUNT(*) FROM emails WHERE created_at > datetime('now', '-30 days')")->fetchColumn();
    
} catch (Exception $e) {
    die("Database error: " . $e->getMessage());
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Database Viewer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            background: #0d1117;
            color: #e6edf3;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: #1e90ff;
            margin-bottom: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .stat-box {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
            text-align: center;
        }
        .stat-box h3 {
            color: #8b949e;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .stat-box .number {
            color: #1e90ff;
            font-size: 32px;
            font-weight: bold;
        }
        .logout {
            float: right;
            margin-top: -50px;
        }
        .logout a {
            color: #8b949e;
            text-decoration: none;
            padding: 8px 16px;
            border: 1px solid #30363d;
            border-radius: 6px;
            background: #161b22;
        }
        .logout a:hover {
            background: #21262d;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            overflow: hidden;
        }
        thead {
            background: #0f141b;
        }
        th {
            text-align: left;
            padding: 12px;
            color: #8b949e;
            font-size: 12px;
            text-transform: uppercase;
            border-bottom: 1px solid #30363d;
        }
        td {
            padding: 12px;
            border-bottom: 1px solid #30363d;
        }
        tbody tr:hover {
            background: #1c2128;
        }
        tbody tr:last-child td {
            border-bottom: none;
        }
        .email-col {
            color: #1e90ff;
            font-family: monospace;
        }
        .date-col {
            color: #8b949e;
            font-size: 14px;
        }
        .export {
            margin: 20px 0;
        }
        .export a {
            display: inline-block;
            padding: 10px 20px;
            background: #238636;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }
        .export a:hover {
            background: #2ea043;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logout">
            <a href="?logout=1">Logout</a>
        </div>
        <h1>Email Database Viewer</h1>
        
        <div class="stats">
            <div class="stat-box">
                <h3>Total Emails</h3>
                <div class="number"><?php echo number_format($total_emails); ?></div>
            </div>
            <div class="stat-box">
                <h3>Today</h3>
                <div class="number"><?php echo number_format($today_count); ?></div>
            </div>
            <div class="stat-box">
                <h3>This Week</h3>
                <div class="number"><?php echo number_format($this_week); ?></div>
            </div>
            <div class="stat-box">
                <h3>This Month</h3>
                <div class="number"><?php echo number_format($this_month); ?></div>
            </div>
        </div>
        
        <div class="export">
            <a href="?export=csv">Export as CSV</a>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Email</th>
                    <th>IP Address</th>
                    <th>Date (Bogota)</th>
                </tr>
            </thead>
            <tbody>
                <?php if (empty($emails)): ?>
                    <tr>
                        <td colspan="4" style="text-align: center; color: #8b949e; padding: 40px;">
                            No emails in database yet.
                        </td>
                    </tr>
                <?php else: ?>
                    <?php foreach ($emails as $email): ?>
                        <tr>
                            <td><?php echo htmlspecialchars($email['id']); ?></td>
                            <td class="email-col"><?php echo htmlspecialchars($email['email']); ?></td>
                            <td><?php echo htmlspecialchars($email['ip_address'] ?? 'N/A'); ?></td>
                            <td class="date-col"><?php 
                                $date = new DateTime($email['created_at']);
                                $date->setTimezone(new DateTimeZone('America/Bogota'));
                                echo $date->format('Y-m-d H:i:s');
                            ?></td>
                        </tr>
                    <?php endforeach; ?>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</body>
</html>
<?php
// Handle CSV export
if (isset($_GET['export']) && $_GET['export'] === 'csv') {
    header('Content-Type: text/csv');
    header('Content-Disposition: attachment; filename="emails_' . date('Y-m-d') . '.csv"');
    
    $output = fopen('php://output', 'w');
    fputcsv($output, ['ID', 'Email', 'IP Address', 'Created At (Bogota)']);
    
    foreach ($emails as $email) {
        $date = new DateTime($email['created_at']);
        $date->setTimezone(new DateTimeZone('America/Bogota'));
        fputcsv($output, [
            $email['id'],
            $email['email'],
            $email['ip_address'] ?? 'N/A',
            $date->format('Y-m-d H:i:s')
        ]);
    }
    
    fclose($output);
    exit;
}
?>

