<?php
/**
 * Root index file with IP-based language detection
 * This replaces index.html for better server-side IP detection
 */

// Include language detection (adjust path based on where this file is located)
// If index.php is in /public_html/, use this path:
require_once __DIR__ . '/coming-soon/detect_language.php';

// If index.php is in /public_html/coming-soon/, use:
// require_once __DIR__ . '/detect_language.php';

// Detect language from IP
$detected_lang = detectLanguage();

// Redirect to appropriate language
$redirect_url = "/coming-soon/{$detected_lang}/";
header("Location: {$redirect_url}", true, 302);
exit;
?>

