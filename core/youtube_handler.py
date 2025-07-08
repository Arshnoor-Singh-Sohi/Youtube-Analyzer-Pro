# core/youtube_handler.py
import re
import json
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from datetime import datetime
import streamlit as st

class YouTubeHandler:
    def __init__(self):
        self.youtube_api_key = st.secrets.get("YOUTUBE_API_KEY", "")
        
    def extract_video_id(self, youtube_url):
        """Extract video ID from various YouTube URL formats"""
        try:
            youtube_url = youtube_url.strip()
            
            # Pattern for youtu.be short URLs
            if 'youtu.be' in youtube_url:
                video_id = youtube_url.split('youtu.be/')[-1].split('?')[0].split('&')[0]
                return video_id
            
            # Pattern for youtube.com URLs
            if 'youtube.com' in youtube_url:
                parsed_url = urlparse(youtube_url)
                query_params = parse_qs(parsed_url.query)
                
                if 'v' in query_params:
                    video_id = query_params['v'][0]
                    return video_id
            
            # Regex fallback
            video_id_pattern = r'(?:v=|/)([a-zA-Z0-9_-]{11})'
            match = re.search(video_id_pattern, youtube_url)
            if match:
                return match.group(1)
            
            return None
            
        except Exception as e:
            st.error(f"Error extracting video ID: {e}")
            return None
    
    def get_video_info(self, youtube_url):
        """Get comprehensive video information"""
        video_id = self.extract_video_id(youtube_url)
        if not video_id:
            return None
            
        try:
            # Basic info that we can get without API
            video_info = {
                'video_id': video_id,
                'url': youtube_url,
                'thumbnail': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                'title': 'Loading...',
                'duration': 'Unknown',
                'channel': 'Unknown',
                'views': 0,
                'description': '',
                'published_date': None
            }
            
            # If YouTube API key is available, get detailed info
            if self.youtube_api_key:
                detailed_info = self._get_video_details_from_api(video_id)
                if detailed_info:
                    video_info.update(detailed_info)
            else:
                # Try to get basic info from page scraping (fallback)
                basic_info = self._get_basic_video_info(video_id)
                if basic_info:
                    video_info.update(basic_info)
            
            return video_info
            
        except Exception as e:
            st.error(f"Error getting video info: {e}")
            return None
    
    def _get_video_details_from_api(self, video_id):
        """Get detailed video information using YouTube API"""
        try:
            url = f"https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': video_id,
                'key': self.youtube_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                video = data['items'][0]
                snippet = video['snippet']
                statistics = video['statistics']
                content_details = video['contentDetails']
                
                return {
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channel': snippet['channelTitle'],
                    'published_date': snippet['publishedAt'],
                    'views': int(statistics.get('viewCount', 0)),
                    'likes': int(statistics.get('likeCount', 0)),
                    'comments': int(statistics.get('commentCount', 0)),
                    'duration': self._parse_duration(content_details['duration']),
                    'tags': snippet.get('tags', []),
                    'category_id': snippet.get('categoryId', ''),
                    'language': snippet.get('defaultLanguage', 'en')
                }
            
            return None
            
        except Exception as e:
            st.warning(f"Could not fetch detailed video info: {e}")
            return None
    
    def _get_basic_video_info(self, video_id):
        """Get basic video info without API (fallback method)"""
        try:
            # This is a simplified version - in production, you might want to use
            # web scraping libraries like BeautifulSoup to extract more info
            return {
                'title': f'Video {video_id}',
                'duration': 'Unknown',
                'channel': 'Unknown Channel',
                'views': 0,
                'description': 'Description not available'
            }
        except:
            return None
    
    def _parse_duration(self, duration_str):
        """Parse YouTube API duration format (PT4M13S) to readable format"""
        try:
            duration_pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
            match = re.match(duration_pattern, duration_str)
            
            if match:
                hours = int(match.group(1) or 0)
                minutes = int(match.group(2) or 0)
                seconds = int(match.group(3) or 0)
                
                if hours > 0:
                    return f"{hours}:{minutes:02d}:{seconds:02d}"
                else:
                    return f"{minutes}:{seconds:02d}"
            
            return "Unknown"
        except:
            return "Unknown"
    
    def extract_transcript(self, youtube_url):
        """Extract transcript with enhanced features"""
        video_id = self.extract_video_id(youtube_url)
        if not video_id:
            return None
            
        try:
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Process transcript
            full_text = ""
            timestamped_segments = []
            
            for entry in transcript_list:
                timestamp = self._format_timestamp(entry['start'])
                text = entry['text'].strip()
                
                # Add to full text
                full_text += " " + text
                
                # Add timestamped segment
                timestamped_segments.append({
                    'timestamp': timestamp,
                    'start_time': entry['start'],
                    'duration': entry['duration'],
                    'text': text
                })
            
            # Language detection
            try:
                available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                language_codes = [t.language_code for t in available_transcripts]
            except:
                language_codes = ['en']
            
            return {
                'text': full_text.strip(),
                'segments': timestamped_segments,
                'language_codes': language_codes,
                'total_segments': len(timestamped_segments),
                'total_duration': timestamped_segments[-1]['start_time'] + timestamped_segments[-1]['duration'] if timestamped_segments else 0
            }
            
        except Exception as e:
            error_msg = str(e)
            if "No transcripts found" in error_msg:
                st.error("❌ This video doesn't have captions/subtitles available")
            elif "private" in error_msg.lower():
                st.error("❌ This video is private or restricted")
            elif "not available" in error_msg.lower():
                st.error("❌ Transcript not available for this video")
            else:
                st.error(f"❌ Error extracting transcript: {error_msg}")
            return None
    
    def _format_timestamp(self, seconds):
        """Format seconds to MM:SS or HH:MM:SS format"""
        try:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
        except:
            return "00:00"
    
    def get_video_chapters(self, transcript_data):
        """Extract potential chapter information from transcript"""
        try:
            segments = transcript_data['segments']
            chapters = []
            
            # Look for chapter indicators in transcript
            chapter_keywords = ['chapter', 'section', 'part', 'introduction', 'conclusion', 'overview']
            
            for i, segment in enumerate(segments):
                text_lower = segment['text'].lower()
                
                # Check if this segment might be a chapter title
                if any(keyword in text_lower for keyword in chapter_keywords):
                    chapters.append({
                        'timestamp': segment['timestamp'],
                        'title': segment['text'],
                        'start_time': segment['start_time']
                    })
            
            return chapters
            
        except Exception as e:
            st.warning(f"Could not extract chapters: {e}")
            return []
    
    def search_transcript(self, transcript_data, query):
        """Search for specific terms in transcript"""
        try:
            results = []
            query_lower = query.lower()
            
            for segment in transcript_data['segments']:
                if query_lower in segment['text'].lower():
                    results.append({
                        'timestamp': segment['timestamp'],
                        'text': segment['text'],
                        'start_time': segment['start_time']
                    })
            
            return results
            
        except Exception as e:
            st.error(f"Error searching transcript: {e}")
            return []