# 🎥 YouTube Video Analyzer Pro

> **Next-Level AI-Powered YouTube Video Analysis and Summarization Platform**

Transform any YouTube video into comprehensive insights with advanced AI analysis, multiple summary styles, interactive chat, and professional export options.

## ✨ Features

### 🎯 Core Analysis Features
- **Multiple Summary Types**: Comprehensive, Brief, Bullet Points, Academic, Business, Creative
- **AI-Powered Insights**: Key takeaways, important quotes, action items, timeline analysis
- **Topic Extraction**: Automatic identification of main themes and subjects
- **Sentiment Analysis**: Emotional tone and sentiment scoring
- **Question & Answer Pairs**: Extracted Q&A from video content

### 🤖 Interactive Features
- **Chat with Content**: Ask questions about the video and get AI-powered answers
- **Smart Suggestions**: Contextual question recommendations
- **Real-time Analysis**: Live processing with progress indicators
- **Session Management**: Save and revisit previous analyses

### 📊 Export & Sharing
- **Multiple Formats**: PDF, Word Document, Text File, JSON
- **Professional Reports**: Comprehensive analysis reports with charts and metrics
- **Download Options**: Summary, full report, or transcript export
- **Session History**: Export and manage analysis history

### 🎨 User Experience
- **Modern UI**: Clean, responsive design with animations
- **Multi-language Support**: Analysis in multiple languages
- **Video Preview**: Thumbnail and metadata display
- **Progress Tracking**: Real-time analysis progress

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-analyzer-pro.git
cd youtube-analyzer-pro
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
Navigate to `http://localhost:8501`

## 📁 Project Structure

```
youtube-analyzer-pro/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
│
├── core/                           # Core application modules
│   ├── __init__.py
│   ├── youtube_handler.py          # YouTube API and transcript handling
│   ├── ai_processor.py            # AI analysis and processing
│   ├── export_handler.py          # Export functionality (PDF, Word, etc.)
│   └── session_manager.py         # Session and history management
│
├── components/                     # UI components
│   ├── __init__.py
│   └── chat_interface.py          # Interactive chat functionality
│
├── config/                         # Configuration files
│   ├── __init__.py
│   └── settings.py                # Application settings and config
│
├── prompts/                        # AI prompt templates
│   ├── __init__.py
│   └── templates.py               # Specialized prompts for different analysis types
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── validators.py              # Input validation and sanitization
│
├── data/                          # Data storage (created automatically)
│   ├── sessions/                  # User session data
│   ├── exports/                   # Generated export files
│   └── logs/                      # Application logs
│
├── tests/                         # Unit tests (optional)
│   ├── __init__.py
│   ├── test_youtube_handler.py
│   ├── test_ai_processor.py
│   └── test_validators.py
│
└── docs/                          # Additional documentation
    ├── api.md                     # API documentation
    ├── deployment.md              # Deployment guide
    └── contributing.md            # Contribution guidelines
```

## 🔧 Configuration

### Environment Variables

Key environment variables you need to set:

```bash
# Required
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional but recommended
YOUTUBE_API_KEY=your_youtube_api_key_here
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Analysis Settings

Customize analysis behavior in `.env`:

```bash
MAX_TRANSCRIPT_LENGTH=500000
MAX_SUMMARY_WORDS=1000
DEFAULT_LANGUAGE=English
ENABLE_CHAT=true
ENABLE_ANALYTICS=true
```

## 📚 Usage Guide

### Basic Analysis

1. **Enter YouTube URL**: Paste any YouTube video URL
2. **Choose Settings**: Select summary type, language, and features
3. **Click Analyze**: Wait for AI processing to complete
4. **View Results**: Explore summary, insights, topics, and timeline

### Interactive Chat

1. **Access Chat Tab**: Click on the chat interface after analysis
2. **Ask Questions**: Type questions about the video content
3. **Get AI Answers**: Receive contextual, intelligent responses
4. **Follow Suggestions**: Use suggested questions for deeper exploration

### Export Options

1. **Choose Format**: Select PDF, Word, Text, or JSON
2. **Select Content**: Summary only or comprehensive report
3. **Download**: Get professionally formatted documents

### Session Management

- **Auto-Save**: Sessions are automatically saved
- **History Access**: View and reload previous analyses
- **Search Sessions**: Find sessions by video title or content
- **Export History**: Download complete session history

## 🎨 Customization

### Adding New Summary Types

1. **Update Templates**: Add new prompt in `prompts/templates.py`
2. **Modify UI**: Update dropdown options in `app.py`
3. **Test Analysis**: Verify new summary type works correctly

### Custom Export Formats

1. **Extend ExportHandler**: Add new format method in `core/export_handler.py`
2. **Update UI**: Add format option to interface
3. **Handle MIME Types**: Ensure proper file handling

### UI Themes

Customize the appearance in `config/settings.py`:

```python
UI_CONFIG = {
    'theme': {
        'primary_color': '#4ecdc4',
        'secondary_color': '#ff6b6b',
        'background_color': '#ffffff'
    }
}
```

## 🔒 Security & Privacy

- **No Data Storage**: Video content is processed in memory only
- **Session Encryption**: Local session data is securely stored
- **API Key Protection**: Environment variables for sensitive data
- **Content Filtering**: Optional content safety checks

## 📈 Performance

### Optimization Tips

1. **API Limits**: Monitor Gemini API usage and quotas
2. **Memory Management**: Large videos may require more memory
3. **Caching**: Enable caching for repeated analyses
4. **Concurrent Limits**: Adjust based on server capacity

### Monitoring

Enable monitoring in production:

```bash
MONITORING_ENABLED=true
ERROR_TRACKING=true
PERF_MONITORING=true
```

## 🚀 Deployment

### Streamlit Cloud

1. **Fork Repository**: Create your own fork
2. **Connect to Streamlit**: Link GitHub repository
3. **Add Secrets**: Configure environment variables
4. **Deploy**: Automatic deployment from main branch

### Docker Deployment

```bash
# Build image
docker build -t youtube-analyzer-pro .

# Run container
docker run -p 8501:8501 --env-file .env youtube-analyzer-pro
```

### Local Production

```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment
export ENVIRONMENT=production

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=core tests/
```

### Manual Testing

1. **Test Different URLs**: Try various YouTube video formats
2. **Validate Exports**: Check all export formats work correctly
3. **Chat Functionality**: Test interactive chat features
4. **Error Handling**: Test with invalid URLs and edge cases

## 📋 API Reference

### Core Classes

#### YouTubeHandler
- `extract_video_id(url)`: Extract video ID from URL
- `get_video_info(url)`: Get video metadata
- `extract_transcript(url)`: Get video transcript

#### AIProcessor
- `comprehensive_analysis(transcript, **kwargs)`: Full AI analysis
- `chat_with_content(transcript, question)`: Interactive chat

#### ExportHandler
- `export_summary(results, format)`: Export summary
- `export_full_report(results, transcript, video_info, format)`: Export complete report

#### SessionManager
- `save_session(data)`: Save analysis session
- `load_session(session_id)`: Load previous session
- `get_recent_sessions(limit)`: Get session history

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

### Development Setup

1. **Fork and Clone**: Create your development environment
2. **Install Dependencies**: Including development packages
3. **Create Branch**: Feature or bug fix branch
4. **Make Changes**: Follow coding standards
5. **Test**: Ensure all tests pass
6. **Submit PR**: Detailed pull request description

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini**: For powerful AI analysis capabilities
- **Streamlit**: For the amazing web framework
- **YouTube Transcript API**: For transcript extraction
- **ReportLab & python-docx**: For document generation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/youtube-analyzer-pro/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/youtube-analyzer-pro/discussions)
- **Email**: sohi21@uwindsor.ca

## 🗺️ Roadmap

### Version 2.1
- [ ] Batch video processing
- [ ] Advanced analytics dashboard
- [ ] User account system
- [ ] API access

### Version 2.2
- [ ] Video comparison features
- [ ] Playlist analysis
- [ ] Integration with note-taking apps
- [ ] Mobile optimization

### Version 3.0
- [ ] Real-time video analysis
- [ ] Multi-language interface
- [ ] Advanced AI models
- [ ] Enterprise features

---

**Made with ❤️ by Arshnoor Singh Sohi**

*Transform any YouTube video into actionable insights with the power of AI!*