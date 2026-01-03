<?php
/**
 * Coming Soon Directory Index
 * Redirects to language-specific page based on IP address
 */

// Include language detection
require_once __DIR__ . '/detect_language.php';

// Detect language from IP
$detected_lang = detectLanguage();

// Redirect to appropriate language page (301 permanent redirect for better caching)
header("Location: /coming-soon/{$detected_lang}/", true, 301);
exit;
?>

