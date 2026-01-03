<?php
/**
 * Root index file - INSTANT redirect
 * Uses browser language only for maximum speed (no API calls)
 */

// Prevent any output
ob_start();

// Instant browser language detection (no API calls, no delays)
$detected_lang = 'en'; // Default

if (isset($_SERVER['HTTP_ACCEPT_LANGUAGE'])) {
    $lang = strtolower(substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2));
    if ($lang === 'es' || $lang === 'de') {
        $detected_lang = $lang;
    }
}

// Clear output buffer
ob_end_clean();

// Instant redirect - no delays, no API calls
header("Location: /coming-soon/{$detected_lang}/", true, 301);
exit;
?>

