# core/ai_processor.py
import google.generativeai as genai
import json
import re
from datetime import datetime
from typing import Dict, List, Any
import streamlit as st
from prompts.templates import PromptTemplates

class AIProcessor:
    def __init__(self):
        # Configure Gemini
        api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Google API key not found. Please add GOOGLE_API_KEY or GEMINI_API_KEY to your secrets.")
            return
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.prompt_templates = PromptTemplates()
    
    def comprehensive_analysis(self, transcript_text: str, **kwargs) -> Dict[str, Any]:
        """Perform comprehensive analysis of the video transcript"""
        
        # Extract parameters
        summary_type = kwargs.get('summary_type', 'Comprehensive')
        language = kwargs.get('language', 'English')
        include_timestamps = kwargs.get('include_timestamps', True)
        include_sentiment = kwargs.get('include_sentiment', True)
        include_topics = kwargs.get('include_topics', True)
        video_info = kwargs.get('video_info', {})
        
        results = {}
        
        try:
            # 1. Generate main summary
            results['main_summary'] = self._generate_summary(
                transcript_text, summary_type, language, video_info
            )
            
            # 2. Extract key takeaways
            results['key_takeaways'] = self._extract_key_takeaways(
                transcript_text, summary_type
            )
            
            # 3. Identify important quotes
            results['important_quotes'] = self._extract_important_quotes(
                transcript_text
            )
            
            # 4. Generate action items
            results['action_items'] = self._generate_action_items(
                transcript_text
            )
            
            # 5. Topic analysis
            if include_topics:
                results['topics'] = self._extract_topics(transcript_text)
            
            # 6. Sentiment analysis
            if include_sentiment:
                results['sentiment_analysis'] = self._analyze_sentiment(transcript_text)
                results['sentiment_score'] = results['sentiment_analysis'].get('overall_score', 0)
            
            # 7. Generate timeline/structure
            results['timeline'] = self._generate_timeline(transcript_text)
            
            # 8. Extract questions and answers
            results['questions_and_answers'] = self._extract_qa_pairs(transcript_text)
            
            # 9. Generate study notes (if academic)
            if summary_type == 'Academic':
                results['study_notes'] = self._generate_study_notes(transcript_text)
            
            # 10. Business insights (if business)
            if summary_type == 'Business':
                results['business_insights'] = self._generate_business_insights(transcript_text)
            
            return results
            
        except Exception as e:
            st.error(f"Error in AI analysis: {e}")
            return {'error': str(e)}
    
    def _generate_summary(self, transcript_text: str, summary_type: str, language: str, video_info: Dict) -> str:
        """Generate the main summary based on type"""
        try:
            prompt = self.prompt_templates.get_summary_prompt(
                summary_type, language, video_info
            )
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            return response.text
            
        except Exception as e:
            st.error(f"Error generating summary: {e}")
            return "Summary generation failed."
    
    def _extract_key_takeaways(self, transcript_text: str, summary_type: str) -> List[str]:
        """Extract key takeaways from the transcript"""
        try:
            prompt = self.prompt_templates.get_takeaways_prompt(summary_type)
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse the response into a list
            takeaways = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                    takeaways.append(line[1:].strip())
                elif line and any(line.startswith(str(i)) for i in range(1, 20)):
                    takeaways.append(re.sub(r'^\d+\.?\s*', '', line))
            
            return takeaways[:10]  # Limit to top 10 takeaways
            
        except Exception as e:
            st.error(f"Error extracting takeaways: {e}")
            return []
    
    def _extract_important_quotes(self, transcript_text: str) -> List[str]:
        """Extract the most important and impactful quotes"""
        try:
            prompt = self.prompt_templates.get_quotes_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Extract quotes from response
            quotes = []
            lines = response.text.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and ('"' in line or "'" in line):
                    # Clean up the quote
                    quote = re.sub(r'^[\d\-\•\*\s]+', '', line)
                    quote = quote.strip('"\'')
                    if len(quote) > 10:  # Minimum length for meaningful quotes
                        quotes.append(quote)
            
            return quotes[:5]  # Limit to top 5 quotes
            
        except Exception as e:
            st.error(f"Error extracting quotes: {e}")
            return []
    
    def _generate_action_items(self, transcript_text: str) -> List[str]:
        """Generate actionable items from the content"""
        try:
            prompt = self.prompt_templates.get_action_items_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse action items
            action_items = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                    action_items.append(line[1:].strip())
                elif line and any(line.startswith(str(i)) for i in range(1, 20)):
                    action_items.append(re.sub(r'^\d+\.?\s*', '', line))
            
            return action_items[:8]  # Limit to top 8 action items
            
        except Exception as e:
            st.error(f"Error generating action items: {e}")
            return []
    
    def _extract_topics(self, transcript_text: str) -> List[str]:
        """Extract main topics and themes"""
        try:
            prompt = self.prompt_templates.get_topics_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse topics
            topics = []
            for line in response.text.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    # Clean up topic
                    topic = re.sub(r'^[\d\-\•\*\s]+', '', line)
                    topic = topic.strip('.,;:')
                    if len(topic) > 2:
                        topics.append(topic)
            
            return topics[:12]  # Limit to top 12 topics
            
        except Exception as e:
            st.error(f"Error extracting topics: {e}")
            return []
    
    def _analyze_sentiment(self, transcript_text: str) -> Dict[str, float]:
        """Analyze sentiment of the transcript"""
        try:
            prompt = self.prompt_templates.get_sentiment_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse sentiment response
            sentiment_data = {
                'positive': 0.0,
                'neutral': 0.0,
                'negative': 0.0,
                'overall_score': 0.0
            }
            
            # Extract percentages from response
            lines = response.text.lower()
            
            # Look for percentage patterns
            positive_match = re.search(r'positive[:\s]*(\d+(?:\.\d+)?)', lines)
            neutral_match = re.search(r'neutral[:\s]*(\d+(?:\.\d+)?)', lines)
            negative_match = re.search(r'negative[:\s]*(\d+(?:\.\d+)?)', lines)
            overall_match = re.search(r'overall[:\s]*(-?\d+(?:\.\d+)?)', lines)
            
            if positive_match:
                sentiment_data['positive'] = float(positive_match.group(1)) / 100
            if neutral_match:
                sentiment_data['neutral'] = float(neutral_match.group(1)) / 100
            if negative_match:
                sentiment_data['negative'] = float(negative_match.group(1)) / 100
            if overall_match:
                sentiment_data['overall_score'] = float(overall_match.group(1))
            
            return sentiment_data
            
        except Exception as e:
            st.error(f"Error analyzing sentiment: {e}")
            return {'positive': 0.33, 'neutral': 0.33, 'negative': 0.33, 'overall_score': 0.0}
    
    def _generate_timeline(self, transcript_text: str) -> List[Dict[str, str]]:
        """Generate a timeline of key events/topics"""
        try:
            prompt = self.prompt_templates.get_timeline_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse timeline
            timeline = []
            lines = response.text.split('\n')
            
            for line in lines:
                line = line.strip()
                if line and ':' in line:
                    # Try to extract timestamp and description
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        timestamp = parts[0].strip()
                        description = parts[1].strip()
                        
                        # Clean up timestamp
                        timestamp = re.sub(r'^[\d\-\•\*\s]+', '', timestamp)
                        
                        if timestamp and description:
                            timeline.append({
                                'timestamp': timestamp,
                                'description': description
                            })
            
            return timeline[:10]  # Limit to top 10 events
            
        except Exception as e:
            st.error(f"Error generating timeline: {e}")
            return []
    
    def _extract_qa_pairs(self, transcript_text: str) -> List[Dict[str, str]]:
        """Extract question-answer pairs from the transcript"""
        try:
            prompt = self.prompt_templates.get_qa_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse Q&A pairs
            qa_pairs = []
            lines = response.text.split('\n')
            
            current_question = None
            current_answer = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('Q:') or line.startswith('Question:'):
                    if current_question and current_answer:
                        qa_pairs.append({
                            'question': current_question,
                            'answer': current_answer
                        })
                    current_question = line[2:].strip() if line.startswith('Q:') else line[9:].strip()
                    current_answer = None
                elif line.startswith('A:') or line.startswith('Answer:'):
                    current_answer = line[2:].strip() if line.startswith('A:') else line[7:].strip()
            
            # Add the last pair
            if current_question and current_answer:
                qa_pairs.append({
                    'question': current_question,
                    'answer': current_answer
                })
            
            return qa_pairs[:5]  # Limit to top 5 Q&A pairs
            
        except Exception as e:
            st.error(f"Error extracting Q&A pairs: {e}")
            return []
    
    def _generate_study_notes(self, transcript_text: str) -> Dict[str, Any]:
        """Generate academic study notes"""
        try:
            prompt = self.prompt_templates.get_study_notes_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse study notes into structured format
            study_notes = {
                'main_concepts': [],
                'definitions': [],
                'examples': [],
                'formulas': []
            }
            
            lines = response.text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if 'concept' in line.lower():
                    current_section = 'main_concepts'
                elif 'definition' in line.lower():
                    current_section = 'definitions'
                elif 'example' in line.lower():
                    current_section = 'examples'
                elif 'formula' in line.lower():
                    current_section = 'formulas'
                elif line and current_section:
                    study_notes[current_section].append(line)
            
            return study_notes
            
        except Exception as e:
            st.error(f"Error generating study notes: {e}")
            return {}
    
    def _generate_business_insights(self, transcript_text: str) -> Dict[str, Any]:
        """Generate business-focused insights"""
        try:
            prompt = self.prompt_templates.get_business_insights_prompt()
            
            response = self.model.generate_content(
                prompt + "\n\nTranscript:\n" + transcript_text
            )
            
            # Parse business insights
            business_insights = {
                'key_strategies': [],
                'market_insights': [],
                'opportunities': [],
                'challenges': []
            }
            
            lines = response.text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if 'strateg' in line.lower():
                    current_section = 'key_strategies'
                elif 'market' in line.lower():
                    current_section = 'market_insights'
                elif 'opportunit' in line.lower():
                    current_section = 'opportunities'
                elif 'challenge' in line.lower():
                    current_section = 'challenges'
                elif line and current_section:
                    business_insights[current_section].append(line)
            
            return business_insights
            
        except Exception as e:
            st.error(f"Error generating business insights: {e}")
            return {}
    
    def chat_with_content(self, transcript_text: str, user_question: str) -> str:
        """Allow users to chat with the video content"""
        try:
            prompt = f"""
            You are an AI assistant that can answer questions about the following video transcript.
            Be helpful, accurate, and cite specific parts of the transcript when relevant.
            
            Transcript: {transcript_text}
            
            User Question: {user_question}
            
            Please provide a comprehensive answer based on the transcript content:
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            st.error(f"Error in chat: {e}")
            return "I'm sorry, I couldn't process your question. Please try again."