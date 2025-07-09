import streamlit as st
import os
import time
from datetime import datetime
import json
from pathlib import Path

# Import custom modules
from core.youtube_handler import YouTubeHandler
from core.ai_processor import AIProcessor
from core.export_handler import ExportHandler
from core.session_manager import SessionManager
from components.chat_interface import ChatInterface
from utils.validators import validate_youtube_url
from config.settings import APP_CONFIG

# Page configuration
st.set_page_config(
    page_title="YouTube Video Analyzer Pro",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4ecdc4;
        margin: 1rem 0;
    }
    .summary-container {
        background: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .metric-box {
        text-align: center;
        padding: 1rem;
        background: #f1f3f4;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    ai_processor = AIProcessor()
    return {
        'youtube_handler': YouTubeHandler(),
        'ai_processor': ai_processor,
        'export_handler': ExportHandler(),
        'session_manager': SessionManager(),
        'chat_interface': ChatInterface(ai_processor)
    }

def main():
    components = initialize_components()
    
    # Check if we have existing analysis data to display
    if (st.session_state.get('analysis_complete', False) and 
        'analysis_results' in st.session_state and 
        'transcript_data' in st.session_state and 
        'video_info' in st.session_state):
        
        # Display existing results immediately
        st.markdown("""
        <div class="main-header">
            <h1>🎥 YouTube Video Analyzer Pro</h1>
            <p>Transform any YouTube video into comprehensive insights with AI-powered analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show current video info
        video_info = st.session_state.video_info
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(
                video_info['thumbnail'],
                caption="Current Analysis",
                use_container_width=True
            )
        with col2:
            st.markdown(f"**Title:** {video_info['title']}")
            st.markdown(f"**Channel:** {video_info['channel']}")
            st.markdown(f"**Duration:** {video_info['duration']}")
            
            if st.button("🔄 Analyze New Video", type="secondary"):
                # Clear session state for new analysis
                for key in ['analysis_complete', 'analysis_results', 'transcript_data', 'video_info']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        # Display the results
        display_analysis_results(
            st.session_state.analysis_results,
            st.session_state.transcript_data,
            st.session_state.video_info,
            components
        )
        return
    
    # Sidebar
    with st.sidebar:
        st.title("🎮 Control Panel")
        
        # Session Management
        st.subheader("📊 Session History")
        sessions = components['session_manager'].get_recent_sessions()
        
        if sessions:
            selected_session = st.selectbox(
                "Load Previous Analysis:",
                options=["New Analysis"] + [f"{s['title'][:30]}..." for s in sessions],
                key="session_selector"
            )
            
            if selected_session != "New Analysis":
                session_idx = sessions[st.session_state.session_selector.split("...")[0]]
                # Load session data
                pass
        
        st.divider()
        
        # API Usage Info
        with st.expander("ℹ️ API Usage Info"):
            st.markdown("""
            **Google Gemini API Limits:**
            - Free tier: Limited requests per minute
            - If you see rate limit errors, wait a few minutes
            - For heavy usage, consider upgrading your API plan
            
            **Tips to avoid rate limits:**
            - Analyze shorter videos first
            - Wait between analyses
            - Use session history to revisit previous analyses
            """)
        
        # Settings
        st.subheader("⚙️ Settings")
        
        # API Status indicator
        api_status = st.empty()
        if st.session_state.get('api_error', False):
            api_status.error("🚫 API Rate Limited - Please wait before analyzing")
        else:
            api_status.success("✅ API Ready")
        
        summary_type = st.selectbox(
            "Summary Style:",
            ["Comprehensive", "Brief", "Bullet Points", "Academic", "Business", "Creative"]
        )
        
        language = st.selectbox(
            "Output Language:",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese"]
        )
        
        include_timestamps = st.checkbox("Include Timestamps", value=True)
        include_sentiment = st.checkbox("Sentiment Analysis", value=True)
        include_topics = st.checkbox("Topic Extraction", value=True)
        
        st.divider()
        
        # Export Options
        st.subheader("📥 Export Options")
        export_format = st.selectbox(
            "Export Format:",
            ["PDF", "Word Document", "Text File", "JSON"]
        )

    # Main content
    st.markdown("""
    <div class="main-header">
        <h1>🎥 YouTube Video Analyzer Pro</h1>
        <p>Transform any YouTube video into comprehensive insights with AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        youtube_url = st.text_input(
            "🔗 Enter YouTube Video URL:",
            placeholder="https://www.youtube.com/watch?v=VIDEO_ID",
            help="Supports all YouTube URL formats including youtu.be links"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button(
            "🔍 Analyze Video",
            type="primary",
            use_container_width=True
        )

    # URL validation and preview
    if youtube_url:
        if validate_youtube_url(youtube_url):
            video_info = components['youtube_handler'].get_video_info(youtube_url)
            
            if video_info:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(
                        video_info['thumbnail'],
                        caption="Video Thumbnail",
                        use_container_width=True
                    )
                
                with col2:
                    st.markdown(f"**Title:** {video_info['title']}")
                    st.markdown(f"**Duration:** {video_info['duration']}")
                    st.markdown(f"**Channel:** {video_info['channel']}")
                    st.markdown(f"**Views:** {video_info['views']:,}")
                    
                    if video_info['description']:
                        with st.expander("📝 Description"):
                            st.write(video_info['description'][:500] + "..." if len(video_info['description']) > 500 else video_info['description'])
        else:
            st.error("❌ Please enter a valid YouTube URL")

    # Analysis processing
    if analyze_button and youtube_url:
        if validate_youtube_url(youtube_url):
            with st.spinner("🔄 Processing video... This may take a moment"):
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Step 1: Extract transcript
                    status_text.text("📥 Extracting transcript...")
                    progress_bar.progress(20)
                    
                    transcript_data = components['youtube_handler'].extract_transcript(youtube_url)
                    
                    if not transcript_data:
                        st.error("❌ Failed to extract transcript. Video may not have captions.")
                        return
                    
                    # Step 2: Process with AI
                    status_text.text("🤖 Analyzing content with AI...")
                    progress_bar.progress(50)
                    
                    analysis_results = components['ai_processor'].comprehensive_analysis(
                        transcript_data['text'],
                        summary_type=summary_type,
                        language=language,
                        include_timestamps=include_timestamps,
                        include_sentiment=include_sentiment,
                        include_topics=include_topics,
                        video_info=video_info
                    )
                    
                    # Step 3: Save session
                    status_text.text("💾 Saving analysis...")
                    progress_bar.progress(80)
                    
                    session_data = {
                        'url': youtube_url,
                        'video_info': video_info,
                        'transcript': transcript_data,
                        'analysis': analysis_results,
                        'settings': {
                            'summary_type': summary_type,
                            'language': language,
                            'include_timestamps': include_timestamps,
                            'include_sentiment': include_sentiment,
                            'include_topics': include_topics
                        },
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    components['session_manager'].save_session(session_data)
                    
                    # Step 4: Display results
                    status_text.text("✅ Analysis complete!")
                    progress_bar.progress(100)
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display results
                    display_analysis_results(analysis_results, transcript_data, video_info, components)
                    
                except Exception as e:
                    error_msg = str(e)
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Handle different types of errors
                    if "429" in error_msg or "rate limit" in error_msg.lower():
                        st.error("🚫 **API Rate Limit Exceeded**")
                        st.info("""
                        **What happened:** You've exceeded the Google Gemini API quota limit.
                        
                        **Solutions:**
                        1. ⏰ **Wait 1-2 minutes** and try again
                        2. 🔄 Try analyzing a **shorter video**
                        3. 📚 Use **session history** to view previous analyses
                        4. 💰 Consider upgrading your Google API plan for higher limits
                        
                        **Current status:** API temporarily blocked - please wait before retrying.
                        """)
                        st.session_state.api_error = True
                    elif "quota" in error_msg.lower():
                        st.error("📊 **API Quota Exceeded**")
                        st.info("""
                        **Daily/Monthly quota reached.** 
                        
                        **Solutions:**
                        1. ⏰ Wait until quota resets (usually next day/month)
                        2. 💰 Upgrade your Google API plan
                        3. 📚 Review previous analyses in session history
                        """)
                    else:
                        st.error(f"❌ **Analysis Error:** {error_msg}")
                        st.info("""
                        **Troubleshooting steps:**
                        1. 🔄 Try again with a different video
                        2. ✅ Ensure the video has captions/subtitles
                        3. 🔗 Verify the YouTube URL is correct
                        4. ⏰ Wait a moment and retry
                        """)
        else:
            st.error("❌ Please enter a valid YouTube URL")

def display_analysis_results(analysis_results, transcript_data, video_info, components):
    """Display the comprehensive analysis results"""
    
    # Store in session state for persistence
    st.session_state.analysis_results = analysis_results
    st.session_state.transcript_data = transcript_data
    st.session_state.video_info = video_info
    st.session_state.analysis_complete = True
    
    st.markdown("---")
    st.header("📊 Analysis Results")
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Word Count",
            f"{len(transcript_data['text'].split()):,}",
            help="Total words in transcript"
        )
    
    with col2:
        st.metric(
            "Duration",
            video_info.get('duration', 'N/A'),
            help="Video duration"
        )
    
    with col3:
        st.metric(
            "Sentiment Score",
            f"{analysis_results.get('sentiment_score', 0):.2f}",
            help="Overall sentiment (-1 to 1)"
        )
    
    with col4:
        st.metric(
            "Reading Time",
            f"{len(analysis_results['main_summary'].split()) // 200 + 1} min",
            help="Estimated reading time"
        )
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Summary", "🔍 Key Insights", "📈 Topics & Sentiment", "⏰ Timeline", "🤖 Chat", "📄 Full Transcript"
    ])
    
    with tab1:
        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
        st.subheader("📝 Main Summary")
        st.write(analysis_results['main_summary'])
        
        if 'key_takeaways' in analysis_results:
            st.subheader("🎯 Key Takeaways")
            for i, takeaway in enumerate(analysis_results['key_takeaways'], 1):
                st.write(f"{i}. {takeaway}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            if 'important_quotes' in analysis_results:
                st.subheader("💬 Important Quotes")
                for quote in analysis_results['important_quotes']:
                    st.info(f'"{quote}"')
        
        with col2:
            if 'action_items' in analysis_results:
                st.subheader("✅ Action Items")
                for item in analysis_results['action_items']:
                    st.write(f"- {item}")
    
    with tab3:
        if 'topics' in analysis_results:
            st.subheader("🏷️ Main Topics")
            
            # Display topics as badges
            topics_html = ""
            for topic in analysis_results['topics']:
                topics_html += f'<span style="background-color: #2E3440; color: #FFFFFF; padding: 0.4rem 0.8rem; border-radius: 1.2rem; margin: 0.3rem; display: inline-block; font-size: 0.9rem; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{topic}</span>'
            
            st.markdown(topics_html, unsafe_allow_html=True)
        
        if 'sentiment_analysis' in analysis_results:
            st.subheader("😊 Sentiment Analysis")
            sentiment = analysis_results['sentiment_analysis']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positive", f"{sentiment.get('positive', 0):.1%}")
            with col2:
                st.metric("Neutral", f"{sentiment.get('neutral', 0):.1%}")
            with col3:
                st.metric("Negative", f"{sentiment.get('negative', 0):.1%}")
    
    with tab4:
        if 'timeline' in analysis_results:
            st.subheader("⏰ Video Timeline")
            for event in analysis_results['timeline']:
                st.write(f"**{event['timestamp']}** - {event['description']}")
    
    with tab5:
        # Interactive Chat Interface
        chat_interface = components['chat_interface']
        chat_interface.render_chat_interface(transcript_data, analysis_results, video_info)
    
    with tab6:
        st.subheader("📄 Full Transcript")
        st.text_area(
            "Complete Transcript:",
            transcript_data['text'],
            height=400,
            help="Full video transcript with timestamps"
        )
    
    # Export section
    st.markdown("---")
    st.subheader("📥 Export Analysis")
    
    # Get export format from sidebar
    export_format = st.session_state.get('export_format', 'PDF')
    export_handler = components['export_handler']
    
    # Create unique keys for download buttons to prevent conflicts
    video_id = video_info.get('video_id', 'unknown')
    timestamp = int(time.time())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📄 Summary Export**")
        try:
            file_data = export_handler.export_summary(analysis_results, export_format)
            st.download_button(
                label=f"📥 Download {export_format} Summary",
                data=file_data,
                file_name=f"summary_{video_id}_{timestamp}.{export_format.lower().replace(' ', '_')}",
                mime=export_handler.get_mime_type(export_format),
                key=f"download_summary_{timestamp}",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Export error: {e}")
    
    with col2:
        st.markdown("**📊 Full Report Export**")
        try:
            file_data = export_handler.export_full_report(analysis_results, transcript_data, video_info, export_format)
            st.download_button(
                label=f"📥 Download Full Report",
                data=file_data,
                file_name=f"full_report_{video_id}_{timestamp}.{export_format.lower().replace(' ', '_')}",
                mime=export_handler.get_mime_type(export_format),
                key=f"download_report_{timestamp}",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Export error: {e}")
    
    with col3:
        st.markdown("**📋 Transcript Export**")
        st.download_button(
            label="📥 Download Transcript",
            data=transcript_data['text'],
            file_name=f"transcript_{video_id}_{timestamp}.txt",
            mime="text/plain",
            key=f"download_transcript_{timestamp}",
            use_container_width=True
        )

if __name__ == "__main__":
    main()