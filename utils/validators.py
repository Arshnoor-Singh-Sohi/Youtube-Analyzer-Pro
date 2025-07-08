# utils/validators.py
import re
from urllib.parse import urlparse
from typing import Optional, Dict, Any

def validate_youtube_url(url: str) -> bool:
    """Validate if the URL is a valid YouTube URL"""
    if not url or not isinstance(url, str):
        return False
    
    # Remove any whitespace
    url = url.strip()
    
    # Check for YouTube domains
    youtube_domains = [
        'youtube.com',
        'www.youtube.com',
        'm.youtube.com',
        'youtu.be',
        'music.youtube.com'
    ]
    
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Check if domain is in YouTube domains
        if any(domain == yt_domain or domain.endswith('.' + yt_domain) for yt_domain in youtube_domains):
            return True
        
        # Additional check for YouTube URLs
        if 'youtube' in domain or 'youtu.be' in domain:
            return True
            
        return False
        
    except Exception:
        return False

def validate_video_id(video_id: str) -> bool:
    """Validate if the video ID is in correct format"""
    if not video_id or not isinstance(video_id, str):
        return False
    
    # YouTube video IDs are typically 11 characters long
    # and contain alphanumeric characters, hyphens, and underscores
    pattern = r'^[a-zA-Z0-9_-]{11}$'
    
    return bool(re.match(pattern, video_id))

def validate_analysis_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize analysis settings"""
    
    # Default settings
    default_settings = {
        'summary_type': 'Comprehensive',
        'language': 'English',
        'include_timestamps': True,
        'include_sentiment': True,
        'include_topics': True,
        'export_format': 'PDF'
    }
    
    # Validate settings
    validated_settings = {}
    
    # Summary type validation
    valid_summary_types = ['Comprehensive', 'Brief', 'Bullet Points', 'Academic', 'Business', 'Creative']
    summary_type = settings.get('summary_type', default_settings['summary_type'])
    validated_settings['summary_type'] = summary_type if summary_type in valid_summary_types else default_settings['summary_type']
    
    # Language validation
    valid_languages = ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Portuguese', 'Italian', 'Russian', 'Arabic']
    language = settings.get('language', default_settings['language'])
    validated_settings['language'] = language if language in valid_languages else default_settings['language']
    
    # Boolean settings validation
    boolean_settings = ['include_timestamps', 'include_sentiment', 'include_topics']
    for setting in boolean_settings:
        value = settings.get(setting, default_settings[setting])
        validated_settings[setting] = bool(value) if isinstance(value, (bool, int, str)) else default_settings[setting]
    
    # Export format validation
    valid_export_formats = ['PDF', 'Word Document', 'Text File', 'JSON']
    export_format = settings.get('export_format', default_settings['export_format'])
    validated_settings['export_format'] = export_format if export_format in valid_export_formats else default_settings['export_format']
    
    return validated_settings

def validate_transcript_data(transcript_data: Dict[str, Any]) -> bool:
    """Validate transcript data structure"""
    if not transcript_data or not isinstance(transcript_data, dict):
        return False
    
    # Required fields
    required_fields = ['text', 'segments']
    
    for field in required_fields:
        if field not in transcript_data:
            return False
    
    # Validate text
    if not isinstance(transcript_data['text'], str) or not transcript_data['text'].strip():
        return False
    
    # Validate segments
    segments = transcript_data.get('segments', [])
    if not isinstance(segments, list):
        return False
    
    # Check segment structure
    for segment in segments:
        if not isinstance(segment, dict):
            return False
        
        required_segment_fields = ['timestamp', 'text', 'start_time']
        for field in required_segment_fields:
            if field not in segment:
                return False
    
    return True

def validate_session_data(session_data: Dict[str, Any]) -> bool:
    """Validate session data structure"""
    if not session_data or not isinstance(session_data, dict):
        return False
    
    # Required fields
    required_fields = ['url', 'video_info', 'analysis', 'settings']
    
    for field in required_fields:
        if field not in session_data:
            return False
    
    # Validate URL
    if not validate_youtube_url(session_data['url']):
        return False
    
    # Validate video info
    video_info = session_data.get('video_info', {})
    if not isinstance(video_info, dict):
        return False
    
    # Validate analysis results
    analysis = session_data.get('analysis', {})
    if not isinstance(analysis, dict):
        return False
    
    # Validate settings
    settings = session_data.get('settings', {})
    if not isinstance(settings, dict):
        return False
    
    return True

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    if not filename or not isinstance(filename, str):
        return "unknown_file"
    
    # Remove or replace invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(' .')
    
    # Limit length
    max_length = 100
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "unknown_file"
    
    return sanitized

def validate_export_format(format_type: str) -> str:
    """Validate and normalize export format"""
    if not format_type or not isinstance(format_type, str):
        return "Text File"
    
    format_type = format_type.strip().title()
    
    valid_formats = ["PDF", "Word Document", "Text File", "JSON"]
    
    # Direct match
    if format_type in valid_formats:
        return format_type
    
    # Fuzzy matching
    format_lower = format_type.lower()
    
    if 'pdf' in format_lower:
        return "PDF"
    elif 'word' in format_lower or 'docx' in format_lower or 'doc' in format_lower:
        return "Word Document"
    elif 'json' in format_lower:
        return "JSON"
    else:
        return "Text File"

def validate_text_input(text: str, min_length: int = 1, max_length: int = 10000) -> bool:
    """Validate text input"""
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    
    if len(text) < min_length or len(text) > max_length:
        return False
    
    return True

def validate_query_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
    """Validate query parameters"""
    validated_params = {}
    
    # Validate limit parameter
    limit = params.get('limit', 10)
    try:
        limit = int(limit)
        if limit < 1:
            limit = 1
        elif limit > 100:
            limit = 100
    except (ValueError, TypeError):
        limit = 10
    
    validated_params['limit'] = limit
    
    # Validate search query
    query = params.get('query', '')
    if isinstance(query, str):
        validated_params['query'] = query.strip()[:200]  # Limit query length
    else:
        validated_params['query'] = ''
    
    # Validate sort parameter
    sort = params.get('sort', 'created_at')
    valid_sorts = ['created_at', 'title', 'channel', 'duration']
    validated_params['sort'] = sort if sort in valid_sorts else 'created_at'
    
    # Validate order parameter
    order = params.get('order', 'desc')
    valid_orders = ['asc', 'desc']
    validated_params['order'] = order if order in valid_orders else 'desc'
    
    return validated_params

def validate_user_preferences(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Validate user preferences"""
    if not preferences or not isinstance(preferences, dict):
        return {}
    
    validated_prefs = {}
    
    # Summary type
    summary_type = preferences.get('default_summary_type', 'Comprehensive')
    valid_summary_types = ['Comprehensive', 'Brief', 'Bullet Points', 'Academic', 'Business', 'Creative']
    validated_prefs['default_summary_type'] = summary_type if summary_type in valid_summary_types else 'Comprehensive'
    
    # Language
    language = preferences.get('default_language', 'English')
    valid_languages = ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese']
    validated_prefs['default_language'] = language if language in valid_languages else 'English'
    
    # Boolean preferences
    boolean_prefs = ['include_timestamps', 'include_sentiment', 'include_topics', 'auto_save_sessions']
    for pref in boolean_prefs:
        value = preferences.get(pref, True)
        validated_prefs[pref] = bool(value)
    
    # Export format
    export_format = preferences.get('export_format', 'PDF')
    validated_prefs['export_format'] = validate_export_format(export_format)
    
    # Max session history
    max_history = preferences.get('max_session_history', 50)
    try:
        max_history = int(max_history)
        if max_history < 1:
            max_history = 1
        elif max_history > 500:
            max_history = 500
    except (ValueError, TypeError):
        max_history = 50
    
    validated_prefs['max_session_history'] = max_history
    
    # Theme
    theme = preferences.get('theme', 'light')
    valid_themes = ['light', 'dark']
    validated_prefs['theme'] = theme if theme in valid_themes else 'light'
    
    return validated_prefs

def is_safe_content(text: str) -> bool:
    """Basic content safety check"""
    if not text or not isinstance(text, str):
        return False
    
    # Check for extremely long content that might cause issues
    if len(text) > 1000000:  # 1MB limit
        return False
    
    # Check for suspicious patterns (basic implementation)
    suspicious_patterns = [
        r'<script[^>]*>',  # Script tags
        r'javascript:',    # JavaScript URLs
        r'data:text/html', # Data URLs
        r'vbscript:',     # VBScript URLs
    ]
    
    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, text_lower):
            return False
    
    return True