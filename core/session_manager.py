# core/session_manager.py
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import streamlit as st
import hashlib

class SessionManager:
    """Manage user sessions and analysis history"""
    
    def __init__(self):
        self.sessions_dir = Path("data/sessions")
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize session state
        if 'session_history' not in st.session_state:
            st.session_state.session_history = []
        if 'current_session' not in st.session_state:
            st.session_state.current_session = None
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = self._load_user_preferences()
    
    def save_session(self, session_data: Dict[str, Any]) -> str:
        """Save a session to persistent storage"""
        try:
            # Generate session ID
            session_id = self._generate_session_id(session_data)
            
            # Add session metadata
            session_data['session_id'] = session_id
            session_data['created_at'] = datetime.now().isoformat()
            session_data['last_accessed'] = datetime.now().isoformat()
            
            # Save to file
            session_file = self.sessions_dir / f"{session_id}.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            # Update session state
            st.session_state.current_session = session_data
            self._add_to_history(session_data)
            
            return session_id
            
        except Exception as e:
            st.error(f"Error saving session: {e}")
            return None
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session from persistent storage"""
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            
            if not session_file.exists():
                return None
            
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            # Update last accessed
            session_data['last_accessed'] = datetime.now().isoformat()
            self.save_session(session_data)
            
            return session_data
            
        except Exception as e:
            st.error(f"Error loading session: {e}")
            return None
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent sessions for the current user"""
        try:
            sessions = []
            
            # Get all session files
            session_files = list(self.sessions_dir.glob("*.json"))
            
            # Sort by modification time (most recent first)
            session_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Load session metadata
            for session_file in session_files[:limit]:
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                    
                    # Extract relevant metadata
                    session_info = {
                        'session_id': session_data.get('session_id'),
                        'title': session_data.get('video_info', {}).get('title', 'Unknown Video'),
                        'channel': session_data.get('video_info', {}).get('channel', 'Unknown Channel'),
                        'duration': session_data.get('video_info', {}).get('duration', 'Unknown'),
                        'created_at': session_data.get('created_at'),
                        'last_accessed': session_data.get('last_accessed'),
                        'summary_type': session_data.get('settings', {}).get('summary_type', 'Comprehensive'),
                        'url': session_data.get('url', '')
                    }
                    
                    sessions.append(session_info)
                    
                except Exception as e:
                    st.warning(f"Error loading session file {session_file}: {e}")
                    continue
            
            return sessions
            
        except Exception as e:
            st.error(f"Error getting recent sessions: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            
            if session_file.exists():
                session_file.unlink()
                return True
            
            return False
            
        except Exception as e:
            st.error(f"Error deleting session: {e}")
            return False
    
    def cleanup_old_sessions(self, days_old: int = 30) -> int:
        """Clean up sessions older than specified days"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            deleted_count = 0
            
            session_files = list(self.sessions_dir.glob("*.json"))
            
            for session_file in session_files:
                try:
                    # Check file modification time
                    if session_file.stat().st_mtime < cutoff_date.timestamp():
                        session_file.unlink()
                        deleted_count += 1
                        
                except Exception as e:
                    st.warning(f"Error cleaning up session file {session_file}: {e}")
                    continue
            
            return deleted_count
            
        except Exception as e:
            st.error(f"Error during cleanup: {e}")
            return 0
    
    def export_session_history(self) -> Dict[str, Any]:
        """Export all session history"""
        try:
            sessions = self.get_recent_sessions(limit=None)  # Get all sessions
            
            export_data = {
                'export_info': {
                    'type': 'session_history',
                    'generated_at': datetime.now().isoformat(),
                    'total_sessions': len(sessions)
                },
                'sessions': sessions
            }
            
            return export_data
            
        except Exception as e:
            st.error(f"Error exporting session history: {e}")
            return {}
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about user sessions"""
        try:
            sessions = self.get_recent_sessions(limit=None)
            
            if not sessions:
                return {
                    'total_sessions': 0,
                    'total_videos_analyzed': 0,
                    'favorite_summary_type': 'None',
                    'most_active_day': 'None',
                    'channels_analyzed': []
                }
            
            # Calculate statistics
            total_sessions = len(sessions)
            
            # Count summary types
            summary_types = {}
            channels = {}
            dates = {}
            
            for session in sessions:
                # Summary types
                summary_type = session.get('summary_type', 'Unknown')
                summary_types[summary_type] = summary_types.get(summary_type, 0) + 1
                
                # Channels
                channel = session.get('channel', 'Unknown')
                channels[channel] = channels.get(channel, 0) + 1
                
                # Dates
                created_at = session.get('created_at', '')
                if created_at:
                    try:
                        date = datetime.fromisoformat(created_at).date()
                        dates[date] = dates.get(date, 0) + 1
                    except:
                        pass
            
            # Find favorites
            favorite_summary_type = max(summary_types.keys(), key=summary_types.get) if summary_types else 'None'
            most_active_day = max(dates.keys(), key=dates.get) if dates else 'None'
            top_channels = sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                'total_sessions': total_sessions,
                'total_videos_analyzed': total_sessions,
                'favorite_summary_type': favorite_summary_type,
                'most_active_day': str(most_active_day),
                'channels_analyzed': [{'name': name, 'count': count} for name, count in top_channels],
                'summary_type_distribution': summary_types,
                'activity_by_date': {str(date): count for date, count in dates.items()}
            }
            
        except Exception as e:
            st.error(f"Error getting session stats: {e}")
            return {}
    
    def save_user_preferences(self, preferences: Dict[str, Any]) -> bool:
        """Save user preferences"""
        try:
            preferences_file = self.sessions_dir / "user_preferences.json"
            
            with open(preferences_file, 'w', encoding='utf-8') as f:
                json.dump(preferences, f, indent=2, ensure_ascii=False)
            
            st.session_state.user_preferences = preferences
            return True
            
        except Exception as e:
            st.error(f"Error saving preferences: {e}")
            return False
    
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        try:
            preferences_file = self.sessions_dir / "user_preferences.json"
            
            if not preferences_file.exists():
                return self._get_default_preferences()
            
            with open(preferences_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            st.warning(f"Error loading preferences: {e}")
            return self._get_default_preferences()
    
    def _get_default_preferences(self) -> Dict[str, Any]:
        """Get default user preferences"""
        return {
            'default_summary_type': 'Comprehensive',
            'default_language': 'English',
            'include_timestamps': True,
            'include_sentiment': True,
            'include_topics': True,
            'export_format': 'PDF',
            'auto_save_sessions': True,
            'max_session_history': 50,
            'theme': 'light'
        }
    
    def _generate_session_id(self, session_data: Dict[str, Any]) -> str:
        """Generate a unique session ID"""
        try:
            # Create hash from URL and timestamp
            url = session_data.get('url', '')
            timestamp = datetime.now().isoformat()
            
            hash_input = f"{url}{timestamp}".encode('utf-8')
            session_id = hashlib.md5(hash_input).hexdigest()[:16]
            
            return session_id
            
        except Exception as e:
            st.error(f"Error generating session ID: {e}")
            return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def _add_to_history(self, session_data: Dict[str, Any]) -> None:
        """Add session to in-memory history"""
        try:
            # Extract metadata for history
            history_item = {
                'session_id': session_data.get('session_id'),
                'title': session_data.get('video_info', {}).get('title', 'Unknown Video'),
                'timestamp': session_data.get('created_at'),
                'summary_type': session_data.get('settings', {}).get('summary_type', 'Comprehensive')
            }
            
            # Add to beginning of history
            st.session_state.session_history.insert(0, history_item)
            
            # Keep only recent items
            max_history = st.session_state.user_preferences.get('max_session_history', 50)
            st.session_state.session_history = st.session_state.session_history[:max_history]
            
        except Exception as e:
            st.warning(f"Error adding to history: {e}")
    
    def search_sessions(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search sessions by title, channel, or content"""
        try:
            sessions = self.get_recent_sessions(limit=None)
            matching_sessions = []
            
            query_lower = query.lower()
            
            for session in sessions:
                # Search in title
                if query_lower in session.get('title', '').lower():
                    matching_sessions.append(session)
                # Search in channel
                elif query_lower in session.get('channel', '').lower():
                    matching_sessions.append(session)
                # Could extend to search in summary content
            
            return matching_sessions[:limit]
            
        except Exception as e:
            st.error(f"Error searching sessions: {e}")
            return []
    
    def get_session_by_video_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Find existing session for a video URL"""
        try:
            sessions = self.get_recent_sessions(limit=None)
            
            for session in sessions:
                if session.get('url') == url:
                    return self.load_session(session['session_id'])
            
            return None
            
        except Exception as e:
            st.error(f"Error finding session by URL: {e}")
            return None