# Configuration settings for XRay Proxy Validator
# Customize these values according to your needs

import os

# ============================================================
# PERFORMANCE SETTINGS
# ============================================================

# Maximum latency threshold in milliseconds
MAX_LATENCY = 2000

# TCP connection timeout in seconds
TCP_TIMEOUT = 3

# HTTP request timeout in seconds
HTTP_TIMEOUT = 5

# XRay startup timeout
XRAY_STARTUP_TIMEOUT = 0.8

# Number of concurrent workers for proxy testing
MAX_WORKERS = 25

# ============================================================
# VALIDATION STAGES (Enable/Disable)
# ============================================================

ENABLE_STAGE3_IP_REPUTATION = True
ENABLE_STAGE4_SPEED_TEST = True
ENABLE_STAGE5_STABILITY = True
ENABLE_STAGE6_ROUTE_QUALITY = True
ENABLE_STAGE7_TLS_VALIDATION = True

# ============================================================
# SPEED TEST SETTINGS
# ============================================================

# Minimum required speed in Mbps
MIN_SPEED_MBPS = 1.0

# ============================================================
# STABILITY TEST SETTINGS
# ============================================================

# Number of stability checks per proxy
STABILITY_CHECKS = 3

# Required success rate (0.0 - 1.0)
STABILITY_SUCCESS_RATE = 0.7

# ============================================================
# ROUTE QUALITY SETTINGS
# ============================================================

ROUTE_QUALITY_HOSTS = [
    ('http://www.gstatic.com/generate_204', 'Google'),
    ('http://cp.cloudflare.com/generate_204', 'Cloudflare'),
    ('http://connectivitycheck.android.com/generate_204', 'Android'),
]

# ============================================================
# IP REPUTATION SETTINGS
# ============================================================

IP_REPUTATION_TIMEOUT = 5
BLACKLIST_CACHE_TIME = 3600  # Cache results for 1 hour

# ============================================================
# PROXY SOURCES
# ============================================================
# IMPORTANT: Replace these example URLs with your actual proxy sources
# Format: { 'source_name': ['url1', 'url2', ...] }

KEY_SOURCES = {
    'example_premium': [
        'https://example.com/premium.txt',
        'https://example.com/elite.txt',
    ],
    'example_free': [
        'https://example.com/free.txt',
    ],
}

# GitHub token for API rate limiting (optional)
# Set via environment variable: GITHUB_TOKEN
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', None)

# Your Telegram channel for publishing results
MY_CHANNEL = '@vlesstrojan'  # Update with your channel name

# ============================================================
# LOGGING
# ============================================================

LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_TO_FILE = True
LOG_FILE = 'validator.log'

# ============================================================
# DIRECTORIES
# ============================================================

WORKDIR = os.path.dirname(os.path.abspath(__file__))
XRAY_FOLDER = os.path.join(WORKDIR, 'xray')
RESULTS_FOLDER = os.path.join(WORKDIR, 'results')
CACHE_FOLDER = os.path.join(WORKDIR, 'cache')

# Create directories if they don't exist
os.makedirs(XRAY_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(CACHE_FOLDER, exist_ok=True)
