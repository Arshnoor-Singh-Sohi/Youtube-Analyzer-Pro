# components/chat_interface.py
import streamlit as st
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from core.ai_processor import AIProcessor

class ChatInterface:
    """Interactive chat interface for discussing video content"""
    
    def __init__(self, ai_processor: AIProcessor):
        self.ai_processor = ai_processor
        
        # Initialize chat state
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'chat_context' not in st.session_state:
            st.session_state.chat_context = None
        if 'chat_suggestions' not in st.session_state:
            st.session_state.chat_suggestions = []
    
    def render_chat_interface(self, transcript_data: Dict[str, Any], analysis_results: Dict[str, Any], video_info: Dict[str, Any]):
        """Render the complete chat interface"""
        
        # Set context if not already set
        if st.session_state.chat_context is None:
            st.session_state.chat_context = {
                'transcript': transcript_data,
                'analysis': analysis_results,
                'video_info': video_info
            }
        
        st.subheader("🤖 Chat with Video Content")
        st.markdown("Ask questions about the video content and get AI-powered answers!")
        
        # Chat container
        chat_container = st.container()
        
        # Display chat history
        self._display_chat_history(chat_container)
        
        # Suggested questions
        self._display_suggestions()
        
        # Chat input
        self._render_chat_input()
        
        # Chat controls
        self._render_chat_controls()
    
    def _display_chat_history(self, container):
        """Display the chat history"""
        
        with container:
            if not st.session_state.chat_history:
                st.info("💡 Start by asking a question about the video content!")
                return
            
            # Display each message
            for i, message in enumerate(st.session_state.chat_history):
                self._render_message(message, i)
    
    def _render_message(self, message: Dict[str, Any], index: int):
        """Render a single chat message"""
        
        timestamp = message.get('timestamp', datetime.now().strftime('%H:%M'))
        
        if message['role'] == 'user':
            # User message
            with st.chat_message("user"):
                st.write(message['content'])
                st.caption(f"Asked at {timestamp}")
        
        else:
            # AI message
            with st.chat_message("assistant"):
                st.write(message['content'])
                
                # Add helpful actions
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("👍", key=f"like_{index}", help="Helpful answer"):
                        self._rate_message(index, 'like')
                
                with col2:
                    if st.button("👎", key=f"dislike_{index}", help="Not helpful"):
                        self._rate_message(index, 'dislike')
                
                with col3:
                    if st.button("🔄", key=f"regenerate_{index}", help="Regenerate answer"):
                        self._regenerate_answer(index)
                
                st.caption(f"Answered at {timestamp}")
    
    def _display_suggestions(self):
        """Display suggested questions"""
        
        if not st.session_state.chat_suggestions:
            # Generate initial suggestions
            suggestions = self._generate_suggestions()
            st.session_state.chat_suggestions = suggestions
        
        if st.session_state.chat_suggestions:
            st.write("**💡 Suggested Questions:**")
            
            # Display suggestions as clickable buttons
            cols = st.columns(2)
            for i, suggestion in enumerate(st.session_state.chat_suggestions[:4]):
                col = cols[i % 2]
                with col:
                    if st.button(
                        suggestion,
                        key=f"suggestion_{i}",
                        help="Click to ask this question",
                        use_container_width=True
                    ):
                        self._ask_question(suggestion)
    
    def _render_chat_input(self):
        """Render the chat input field"""
        
        # Chat input form
        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Ask a question:",
                    placeholder="What is the main topic discussed in this video?",
                    label_visibility="collapsed"
                )
            
            with col2:
                submitted = st.form_submit_button("Send", use_container_width=True)
            
            if submitted and user_input.strip():
                self._ask_question(user_input.strip())
    
    def _render_chat_controls(self):
        """Render chat control buttons"""
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🗑️ Clear Chat", help="Clear all chat history"):
                self._clear_chat()
        
        with col2:
            if st.button("📋 Summary", help="Get a summary of the conversation"):
                self._generate_chat_summary()
        
        with col3:
            if st.button("💾 Export Chat", help="Export chat history"):
                self._export_chat()
        
        with col4:
            if st.button("🔄 New Suggestions", help="Generate new question suggestions"):
                self._refresh_suggestions()
    
    def _ask_question(self, question: str):
        """Process a user question"""
        
        if not question.strip():
            return
        
        # Add user message to history
        user_message = {
            'role': 'user',
            'content': question,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        st.session_state.chat_history.append(user_message)
        
        # Generate AI response
        with st.spinner("🤔 Thinking..."):
            try:
                context = st.session_state.chat_context
                transcript_text = context['transcript']['text']
                
                # Get AI response
                response = self.ai_processor.chat_with_content(
                    transcript_text, 
                    question
                )
                
                # Add AI message to history
                ai_message = {
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'rating': None
                }
                st.session_state.chat_history.append(ai_message)
                
                # Generate new suggestions based on the conversation
                self._update_suggestions()
                
            except Exception as e:
                st.error(f"Sorry, I couldn't process your question: {e}")
        
        # Rerun to update the interface
        st.rerun()
    
    def _generate_suggestions(self) -> List[str]:
        """Generate contextual question suggestions"""
        
        try:
            context = st.session_state.chat_context
            if not context:
                return self._get_default_suggestions()
            
            # Generate suggestions based on video content
            analysis = context.get('analysis', {})
            video_info = context.get('video_info', {})
            
            suggestions = []
            
            # Based on video title/topic
            if video_info.get('title'):
                suggestions.append(f"What is the main message of this video?")
            
            # Based on key takeaways
            if analysis.get('key_takeaways'):
                suggestions.append("What are the most important points to remember?")
            
            # Based on topics
            if analysis.get('topics'):
                topics = analysis['topics'][:3]
                if topics:
                    suggestions.append(f"Can you explain more about {topics[0]}?")
            
            # Based on timeline
            if analysis.get('timeline'):
                suggestions.append("What happens at the beginning vs the end?")
            
            # General suggestions
            suggestions.extend([
                "What actionable steps can I take from this video?",
                "Are there any important quotes or key phrases?",
                "What questions does this video answer?",
                "How does this relate to current trends?"
            ])
            
            return suggestions[:6]
            
        except Exception as e:
            st.warning(f"Error generating suggestions: {e}")
            return self._get_default_suggestions()
    
    def _get_default_suggestions(self) -> List[str]:
        """Get default question suggestions"""
        return [
            "What is the main topic of this video?",
            "What are the key takeaways?",
            "Can you summarize the important points?",
            "What actionable advice is given?",
            "Are there any important examples mentioned?",
            "What questions does this video answer?"
        ]
    
    def _update_suggestions(self):
        """Update suggestions based on conversation history"""
        
        try:
            # Analyze recent questions to suggest follow-ups
            recent_messages = st.session_state.chat_history[-6:]  # Last 3 exchanges
            
            new_suggestions = []
            
            # Add follow-up suggestions based on recent topics
            for message in recent_messages:
                if message['role'] == 'user':
                    content = message['content'].lower()
                    
                    if 'takeaway' in content or 'key point' in content:
                        new_suggestions.append("Can you elaborate on any of these points?")
                    elif 'example' in content:
                        new_suggestions.append("Are there other examples mentioned?")
                    elif 'action' in content or 'implement' in content:
                        new_suggestions.append("What are the first steps to get started?")
                    elif 'quote' in content:
                        new_suggestions.append("What's the context behind these quotes?")
            
            # Mix with general suggestions
            general_suggestions = [
                "What are the potential challenges mentioned?",
                "How does this apply to beginners?",
                "What tools or resources are recommended?",
                "Are there any contradictions or debates discussed?"
            ]
            
            new_suggestions.extend(general_suggestions)
            
            # Update suggestions (avoid duplicates)
            current_suggestions = st.session_state.chat_suggestions
            updated_suggestions = []
            
            for suggestion in new_suggestions:
                if suggestion not in current_suggestions and len(updated_suggestions) < 6:
                    updated_suggestions.append(suggestion)
            
            # Fill with remaining current suggestions if needed
            for suggestion in current_suggestions:
                if suggestion not in updated_suggestions and len(updated_suggestions) < 6:
                    updated_suggestions.append(suggestion)
            
            st.session_state.chat_suggestions = updated_suggestions
            
        except Exception as e:
            st.warning(f"Error updating suggestions: {e}")
    
    def _rate_message(self, message_index: int, rating: str):
        """Rate an AI message"""
        
        if message_index < len(st.session_state.chat_history):
            st.session_state.chat_history[message_index]['rating'] = rating
            
            if rating == 'like':
                st.success("Thanks for the feedback! 👍")
            else:
                st.info("Thanks for the feedback. I'll try to do better! 👎")
    
    def _regenerate_answer(self, message_index: int):
        """Regenerate an AI answer"""
        
        if message_index > 0 and message_index < len(st.session_state.chat_history):
            # Get the original question
            question_message = st.session_state.chat_history[message_index - 1]
            
            if question_message['role'] == 'user':
                question = question_message['content']
                
                with st.spinner("🔄 Regenerating answer..."):
                    try:
                        context = st.session_state.chat_context
                        transcript_text = context['transcript']['text']
                        
                        # Generate new response
                        response = self.ai_processor.chat_with_content(
                            transcript_text, 
                            question + " (Please provide a different perspective or more details)"
                        )
                        
                        # Update the message
                        st.session_state.chat_history[message_index]['content'] = response
                        st.session_state.chat_history[message_index]['timestamp'] = datetime.now().strftime('%H:%M:%S')
                        st.session_state.chat_history[message_index]['rating'] = None
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error regenerating answer: {e}")
    
    def _clear_chat(self):
        """Clear chat history"""
        st.session_state.chat_history = []
        st.session_state.chat_suggestions = self._generate_suggestions()
        st.success("Chat history cleared!")
        st.rerun()
    
    def _generate_chat_summary(self):
        """Generate a summary of the chat conversation"""
        
        if not st.session_state.chat_history:
            st.info("No chat history to summarize.")
            return
        
        try:
            # Extract questions and topics discussed
            questions = []
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    questions.append(message['content'])
            
            summary = f"""
            **Chat Summary:**
            
            **Total Messages:** {len(st.session_state.chat_history)}
            
            **Questions Asked:**
            """
            
            for i, question in enumerate(questions, 1):
                summary += f"\n{i}. {question}"
            
            summary += f"""
            
            **Key Topics Discussed:** {', '.join(set([q.split()[:3] for q in questions])) if questions else 'None'}
            
            **Duration:** Started {len(st.session_state.chat_history)} messages ago
            """
            
            st.info(summary)
            
        except Exception as e:
            st.error(f"Error generating summary: {e}")
    
    def _export_chat(self):
        """Export chat history"""
        
        if not st.session_state.chat_history:
            st.info("No chat history to export.")
            return
        
        try:
            # Create export data
            export_data = {
                'export_info': {
                    'type': 'chat_history',
                    'generated_at': datetime.now().isoformat(),
                    'total_messages': len(st.session_state.chat_history)
                },
                'video_info': st.session_state.chat_context.get('video_info', {}),
                'chat_history': st.session_state.chat_history
            }
            
            # Convert to JSON
            export_json = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            # Offer download
            st.download_button(
                label="📥 Download Chat History",
                data=export_json.encode('utf-8'),
                file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error exporting chat: {e}")
    
    def _refresh_suggestions(self):
        """Generate new question suggestions"""
        st.session_state.chat_suggestions = self._generate_suggestions()
        st.success("New suggestions generated!")
        st.rerun()
    
    def get_chat_insights(self) -> Dict[str, Any]:
        """Get insights about the chat conversation"""
        
        if not st.session_state.chat_history:
            return {}
        
        try:
            total_messages = len(st.session_state.chat_history)
            user_messages = [m for m in st.session_state.chat_history if m['role'] == 'user']
            ai_messages = [m for m in st.session_state.chat_history if m['role'] == 'assistant']
            
            # Calculate engagement metrics
            insights = {
                'total_messages': total_messages,
                'user_questions': len(user_messages),
                'ai_responses': len(ai_messages),
                'average_question_length': sum(len(m['content'].split()) for m in user_messages) / len(user_messages) if user_messages else 0,
                'topics_explored': len(set(' '.join(m['content'].lower().split()[:3]) for m in user_messages)),
                'conversation_duration': total_messages,
                'engagement_level': 'High' if total_messages > 10 else 'Medium' if total_messages > 5 else 'Low'
            }
            
            return insights
            
        except Exception as e:
            st.error(f"Error generating chat insights: {e}")
            return {}