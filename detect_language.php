<?php
/**
 * IP-based Language Detection
 * Detects user's country from IP address and returns appropriate language code
 */

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

function detectCountryFromIP($ip) {
    // Skip localhost/private IPs
    if ($ip === '127.0.0.1' || $ip === '::1' || strpos($ip, '192.168.') === 0 || strpos($ip, '10.') === 0) {
        return null;
    }
    
    // Use free IP geolocation API (ip-api.com - free tier: 45 requests/minute)
    $url = "http://ip-api.com/json/{$ip}?fields=countryCode";
    
    $context = stream_context_create([
        'http' => [
            'timeout' => 2, // 2 second timeout
            'method' => 'GET'
        ]
    ]);
    
    $response = @file_get_contents($url, false, $context);
    
    if ($response === false) {
        return null;
    }
    
    $data = json_decode($response, true);
    
    if (isset($data['countryCode'])) {
        return strtoupper($data['countryCode']);
    }
    
    return null;
}

function getLanguageFromCountry($countryCode) {
    // Map country codes to languages
    $countryLanguageMap = [
        // Spanish-speaking countries
        'CO' => 'es', // Colombia
        'ES' => 'es', // Spain
        'MX' => 'es', // Mexico
        'AR' => 'es', // Argentina
        'CL' => 'es', // Chile
        'PE' => 'es', // Peru
        'VE' => 'es', // Venezuela
        'EC' => 'es', // Ecuador
        'GT' => 'es', // Guatemala
        'CU' => 'es', // Cuba
        'BO' => 'es', // Bolivia
        'DO' => 'es', // Dominican Republic
        'HN' => 'es', // Honduras
        'PY' => 'es', // Paraguay
        'SV' => 'es', // El Salvador
        'NI' => 'es', // Nicaragua
        'CR' => 'es', // Costa Rica
        'PA' => 'es', // Panama
        'UY' => 'es', // Uruguay
        'PR' => 'es', // Puerto Rico
        
        // German-speaking countries
        'DE' => 'de', // Germany
        'AT' => 'de', // Austria
        'CH' => 'de', // Switzerland
        'LI' => 'de', // Liechtenstein
        'LU' => 'de', // Luxembourg
        
        // English-speaking countries (default)
        'GB' => 'en', // United Kingdom
        'US' => 'en', // United States
        'CA' => 'en', // Canada
        'AU' => 'en', // Australia
        'NZ' => 'en', // New Zealand
        'IE' => 'en', // Ireland
        'ZA' => 'en', // South Africa
    ];
    
    if (isset($countryLanguageMap[$countryCode])) {
        return $countryLanguageMap[$countryCode];
    }
    
    // Default to English for unknown countries
    return 'en';
}

// Main function to detect language
function detectLanguage() {
    $ip = getClientIP();
    $countryCode = detectCountryFromIP($ip);
    
    if ($countryCode) {
        return getLanguageFromCountry($countryCode);
    }
    
    // Fallback to browser language if IP detection fails
    if (isset($_SERVER['HTTP_ACCEPT_LANGUAGE'])) {
        $lang = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'], 0, 2);
        if (in_array($lang, ['es', 'de', 'en'])) {
            return $lang;
        }
    }
    
    // Default to English
    return 'en';
}

// If called directly, return language code
if (php_sapi_name() !== 'cli' && basename($_SERVER['PHP_SELF']) === 'detect_language.php') {
    header('Content-Type: application/json');
    echo json_encode(['language' => detectLanguage()]);
}
?>

