# config/settings.py
import os
from pathlib import Path
from typing import Dict, Any

# Application Configuration
APP_CONFIG = {
    'name': 'YouTube Video Analyzer Pro',
    'version': '2.0.0',
    'description': 'AI-Powered YouTube Video Analysis and Summarization',
    'author': 'Your Name',
    'contact': 'your.email@example.com'
}

# Directory Configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
SESSIONS_DIR = DATA_DIR / 'sessions'
EXPORTS_DIR = DATA_DIR / 'exports'
LOGS_DIR = DATA_DIR / 'logs'

# Create directories if they don't exist
for directory in [DATA_DIR, SESSIONS_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Configuration
API_CONFIG = {
    'google_api_key': os.getenv('GOOGLE_API_KEY', ''),
    'youtube_api_key': os.getenv('YOUTUBE_API_KEY', ''),
    'gemini_model': os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp'),
    'max_retries': int(os.getenv('MAX_API_RETRIES', '3')),
    'timeout': int(os.getenv('API_TIMEOUT', '30'))
}

# Analysis Configuration
ANALYSIS_CONFIG = {
    'max_transcript_length': int(os.getenv('MAX_TRANSCRIPT_LENGTH', '500000')),
    'max_summary_words': int(os.getenv('MAX_SUMMARY_WORDS', '1000')),
    'max_takeaways': int(os.getenv('MAX_TAKEAWAYS', '10')),
    'max_quotes': int(os.getenv('MAX_QUOTES', '5')),
    'max_action_items': int(os.getenv('MAX_ACTION_ITEMS', '8')),
    'max_topics': int(os.getenv('MAX_TOPICS', '12')),
    'default_language': os.getenv('DEFAULT_LANGUAGE', 'English'),
    'supported_languages': [
        'English', 'Spanish', 'French', 'German', 'Chinese', 
        'Japanese', 'Portuguese', 'Italian', 'Russian', 'Arabic'
    ]
}

# Export Configuration
EXPORT_CONFIG = {
    'max_file_size': int(os.getenv('MAX_EXPORT_SIZE', '50000000')),  # 50MB
    'supported_formats': ['PDF', 'Word Document', 'Text File', 'JSON'],
    'default_format': os.getenv('DEFAULT_EXPORT_FORMAT', 'PDF'),
    'include_branding': os.getenv('INCLUDE_BRANDING', 'true').lower() == 'true'
}

# Session Configuration
SESSION_CONFIG = {
    'max_sessions_per_user': int(os.getenv('MAX_SESSIONS_PER_USER', '100')),
    'session_timeout_days': int(os.getenv('SESSION_TIMEOUT_DAYS', '30')),
    'auto_cleanup': os.getenv('AUTO_CLEANUP', 'true').lower() == 'true',
    'backup_sessions': os.getenv('BACKUP_SESSIONS', 'true').lower() == 'true'
}

# UI Configuration
UI_CONFIG = {
    'page_title': 'YouTube Video Analyzer Pro',
    'page_icon': '🎥',
    'layout': 'wide',
    'sidebar_state': 'expanded',
    'theme': {
        'primary_color': '#4ecdc4',
        'secondary_color': '#ff6b6b',
        'background_color': '#ffffff',
        'text_color': '#333333'
    },
    'animations': os.getenv('ENABLE_ANIMATIONS', 'true').lower() == 'true',
    'auto_refresh': int(os.getenv('AUTO_REFRESH_SECONDS', '0'))  # 0 = disabled
}

# Security Configuration
SECURITY_CONFIG = {
    'max_url_length': int(os.getenv('MAX_URL_LENGTH', '2048')),
    'allowed_domains': [
        'youtube.com', 'www.youtube.com', 'm.youtube.com', 
        'youtu.be', 'music.youtube.com'
    ],
    'rate_limit_requests': int(os.getenv('RATE_LIMIT_REQUESTS', '100')),
    'rate_limit_window': int(os.getenv('RATE_LIMIT_WINDOW', '3600')),  # 1 hour
    'content_filtering': os.getenv('CONTENT_FILTERING', 'true').lower() == 'true'
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    'cache_enabled': os.getenv('CACHE_ENABLED', 'true').lower() == 'true',
    'cache_ttl': int(os.getenv('CACHE_TTL', '3600')),  # 1 hour
    'max_concurrent_requests': int(os.getenv('MAX_CONCURRENT_REQUESTS', '5')),
    'chunk_size': int(os.getenv('CHUNK_SIZE', '8192')),
    'memory_limit': int(os.getenv('MEMORY_LIMIT', '512'))  # MB
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    'file_enabled': os.getenv('LOG_TO_FILE', 'true').lower() == 'true',
    'max_file_size': int(os.getenv('MAX_LOG_FILE_SIZE', '10000000')),  # 10MB
    'backup_count': int(os.getenv('LOG_BACKUP_COUNT', '5')),
    'console_enabled': os.getenv('LOG_TO_CONSOLE', 'true').lower() == 'true'
}

# Feature Flags
FEATURE_FLAGS = {
    'chat_with_content': os.getenv('ENABLE_CHAT', 'true').lower() == 'true',
    'advanced_analytics': os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true',
    'batch_processing': os.getenv('ENABLE_BATCH', 'false').lower() == 'true',
    'api_access': os.getenv('ENABLE_API', 'false').lower() == 'true',
    'user_accounts': os.getenv('ENABLE_ACCOUNTS', 'false').lower() == 'true',
    'premium_features': os.getenv('ENABLE_PREMIUM', 'false').lower() == 'true'
}

# Monitoring and Analytics
MONITORING_CONFIG = {
    'enabled': os.getenv('MONITORING_ENABLED', 'false').lower() == 'true',
    'analytics_id': os.getenv('ANALYTICS_ID', ''),
    'error_tracking': os.getenv('ERROR_TRACKING', 'false').lower() == 'true',
    'performance_monitoring': os.getenv('PERF_MONITORING', 'false').lower() == 'true'
}

# Development Configuration
DEV_CONFIG = {
    'debug_mode': os.getenv('DEBUG', 'false').lower() == 'true',
    'hot_reload': os.getenv('HOT_RELOAD', 'false').lower() == 'true',
    'mock_api': os.getenv('MOCK_API', 'false').lower() == 'true',
    'test_mode': os.getenv('TEST_MODE', 'false').lower() == 'true'
}

def get_config() -> Dict[str, Any]:
    """Get complete configuration dictionary"""
    return {
        'app': APP_CONFIG,
        'api': API_CONFIG,
        'analysis': ANALYSIS_CONFIG,
        'export': EXPORT_CONFIG,
        'session': SESSION_CONFIG,
        'ui': UI_CONFIG,
        'security': SECURITY_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'logging': LOGGING_CONFIG,
        'features': FEATURE_FLAGS,
        'monitoring': MONITORING_CONFIG,
        'development': DEV_CONFIG,
        'directories': {
            'base': str(BASE_DIR),
            'data': str(DATA_DIR),
            'sessions': str(SESSIONS_DIR),
            'exports': str(EXPORTS_DIR),
            'logs': str(LOGS_DIR)
        }
    }

def validate_config() -> Dict[str, Any]:
    """Validate configuration and return any issues"""
    issues = []
    
    # Check required API keys
    if not API_CONFIG['google_api_key']:
        issues.append("GOOGLE_API_KEY is not set")
    
    # Check directory permissions
    for name, directory in [
        ('data', DATA_DIR),
        ('sessions', SESSIONS_DIR),
        ('exports', EXPORTS_DIR),
        ('logs', LOGS_DIR)
    ]:
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                issues.append(f"Cannot create {name} directory: {e}")
        elif not os.access(directory, os.W_OK):
            issues.append(f"No write permission for {name} directory")
    
    # Check numeric configurations
    numeric_checks = [
        ('MAX_TRANSCRIPT_LENGTH', ANALYSIS_CONFIG['max_transcript_length'], 1000, 1000000),
        ('MAX_SESSIONS_PER_USER', SESSION_CONFIG['max_sessions_per_user'], 1, 1000),
        ('SESSION_TIMEOUT_DAYS', SESSION_CONFIG['session_timeout_days'], 1, 365)
    ]
    
    for name, value, min_val, max_val in numeric_checks:
        if not min_val <= value <= max_val:
            issues.append(f"{name} value {value} is not within valid range [{min_val}, {max_val}]")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': []
    }

def update_config(new_config: Dict[str, Any]) -> bool:
    """Update configuration values"""
    try:
        # This would typically update environment variables or config files
        # For now, we'll just validate the new configuration
        if isinstance(new_config, dict):
            # Merge with existing config
            current_config = get_config()
            # Update logic would go here
            return True
        return False
    except Exception:
        return False

# Environment-specific configurations
def get_environment() -> str:
    """Get current environment"""
    return os.getenv('ENVIRONMENT', 'development').lower()

def is_production() -> bool:
    """Check if running in production"""
    return get_environment() == 'production'

def is_development() -> bool:
    """Check if running in development"""
    return get_environment() == 'development'

def is_testing() -> bool:
    """Check if running in testing"""
    return get_environment() == 'testing'