# prompts/templates.py
class PromptTemplates:
    """Collection of specialized prompts for different analysis types"""
    
    def get_summary_prompt(self, summary_type: str, language: str, video_info: dict) -> str:
        """Get summary prompt based on type and language"""
        
        base_context = f"""
        You are an expert content analyzer specializing in video transcript analysis.
        
        Video Information:
        - Title: {video_info.get('title', 'Unknown')}
        - Channel: {video_info.get('channel', 'Unknown')}
        - Duration: {video_info.get('duration', 'Unknown')}
        
        Language: Generate the summary in {language}.
        """
        
        if summary_type == "Comprehensive":
            return base_context + """
            Create a comprehensive summary that covers all major points discussed in the video.
            Include the main thesis, supporting arguments, examples, and conclusions.
            Structure it with clear sections and provide detailed explanations.
            Aim for 400-600 words.
            """
            
        elif summary_type == "Brief":
            return base_context + """
            Create a concise summary focusing on the core message and key points.
            Highlight only the most important information and main takeaways.
            Keep it clear and to the point.
            Aim for 150-250 words.
            """
            
        elif summary_type == "Bullet Points":
            return base_context + """
            Create a structured bullet-point summary that breaks down the content into:
            • Main Topic/Theme
            • Key Points (5-8 bullets)
            • Important Details (3-5 bullets)
            • Conclusion/Takeaway
            
            Use clear, actionable bullet points.
            """
            
        elif summary_type == "Academic":
            return base_context + """
            Create an academic-style summary suitable for students and researchers.
            Include:
            - Abstract/Overview
            - Main concepts and theories discussed
            - Supporting evidence and examples
            - Methodology (if applicable)
            - Conclusions and implications
            - Key terms and definitions
            
            Use formal academic language and structure.
            """
            
        elif summary_type == "Business":
            return base_context + """
            Create a business-focused summary emphasizing:
            - Executive summary
            - Strategic insights and recommendations
            - Market implications
            - Actionable business intelligence
            - Key metrics and data points
            - Implementation considerations
            
            Use professional business language and focus on practical applications.
            """
            
        elif summary_type == "Creative":
            return base_context + """
            Create an engaging, creative summary that captures the essence of the content
            while being informative and entertaining. Use:
            - Compelling narrative structure
            - Vivid descriptions and analogies
            - Engaging transitions
            - Memorable quotes and examples
            - Creative formatting and structure
            
            Make it both informative and enjoyable to read.
            """
            
        else:
            return base_context + """
            Create a balanced summary that covers the main points clearly and concisely.
            Include the key messages, supporting details, and conclusions.
            Aim for 250-400 words.
            """
    
    def get_takeaways_prompt(self, summary_type: str) -> str:
        """Get prompt for extracting key takeaways"""
        
        base_prompt = """
        Analyze the following transcript and extract the most important takeaways.
        Focus on actionable insights, key learnings, and memorable points.
        """
        
        if summary_type == "Academic":
            return base_prompt + """
            Focus on:
            - Core concepts and theories
            - Key findings and conclusions
            - Important methodologies
            - Significant insights for further study
            
            Format as clear, educational bullet points.
            """
            
        elif summary_type == "Business":
            return base_prompt + """
            Focus on:
            - Strategic insights
            - Business opportunities
            - Market intelligence
            - Actionable recommendations
            - Performance metrics
            
            Format as executive-level takeaways.
            """
            
        else:
            return base_prompt + """
            Extract 5-10 key takeaways that viewers should remember.
            Focus on practical, actionable insights.
            Format as clear, concise bullet points.
            """
    
    def get_quotes_prompt(self) -> str:
        """Get prompt for extracting important quotes"""
        return """
        Extract the most impactful, memorable, and important quotes from the transcript.
        Focus on:
        - Profound insights and wisdom
        - Memorable statements
        - Key definitions or explanations
        - Inspiring or motivational quotes
        - Controversial or thought-provoking statements
        
        Select 3-5 quotes that best represent the core message.
        Provide only the quotes without additional commentary.
        Format each quote on a new line.
        """
    
    def get_action_items_prompt(self) -> str:
        """Get prompt for generating action items"""
        return """
        Based on the transcript content, generate specific, actionable items that
        viewers can implement or follow up on.
        
        Focus on:
        - Specific steps to take
        - Recommended actions
        - Things to research further
        - Practical implementations
        - Follow-up activities
        
        Format as clear, actionable bullet points.
        Start each item with an action verb.
        Provide 5-8 concrete action items.
        """
    
    def get_topics_prompt(self) -> str:
        """Get prompt for extracting main topics"""
        return """
        Identify and extract the main topics, themes, and subjects discussed in the transcript.
        
        Focus on:
        - Primary topics and themes
        - Subtopics and categories
        - Key concepts mentioned
        - Subject areas covered
        - Important keywords and phrases
        
        Provide 8-12 topics as single words or short phrases.
        Format as a simple list, one topic per line.
        """
    
    def get_sentiment_prompt(self) -> str:
        """Get prompt for sentiment analysis"""
        return """
        Analyze the overall sentiment and emotional tone of the transcript.
        
        Provide:
        1. Overall sentiment percentages:
           - Positive: X%
           - Neutral: X%
           - Negative: X%
        
        2. Overall sentiment score: [number between -1 and 1]
           (-1 = very negative, 0 = neutral, 1 = very positive)
        
        3. Brief explanation of the emotional tone and mood throughout the content.
        
        Base your analysis on:
        - Word choice and language used
        - Emotional expressions
        - Overall message tone
        - Speaker's attitude and delivery style
        """
    
    def get_timeline_prompt(self) -> str:
        """Get prompt for generating timeline"""
        return """
        Create a timeline of key events, topics, or sections discussed in the video.
        
        Analyze the flow of content and identify:
        - Major topic transitions
        - Key events or milestones mentioned
        - Important segments or chapters
        - Significant moments or turning points
        
        Format as:
        [Time/Section]: [Brief description of what happens]
        
        Example:
        00:00: Introduction and overview
        05:30: First main topic discussion
        12:15: Important example or case study
        
        Provide 8-10 timeline entries covering the major flow of content.
        """
    
    def get_qa_prompt(self) -> str:
        """Get prompt for extracting Q&A pairs"""
        return """
        Extract or generate relevant question-answer pairs from the transcript.
        
        Focus on:
        - Actual questions asked and answered in the content
        - Implicit questions that are addressed
        - Important concepts explained
        - Key topics that viewers might want to understand
        
        Format as:
        Q: [Question]
        A: [Answer]
        
        Provide 3-5 meaningful Q&A pairs that capture the most important information.
        """
    
    def get_study_notes_prompt(self) -> str:
        """Get prompt for generating academic study notes"""
        return """
        Create comprehensive study notes from the transcript suitable for academic learning.
        
        Organize into sections:
        
        MAIN CONCEPTS:
        - List the primary concepts and theories discussed
        
        DEFINITIONS:
        - Key terms and their explanations
        
        EXAMPLES:
        - Important examples and case studies mentioned
        
        FORMULAS/METHODS:
        - Any formulas, methodologies, or processes explained
        
        Use clear, academic language and structure the notes for easy studying and review.
        """
    
    def get_business_insights_prompt(self) -> str:
        """Get prompt for generating business insights"""
        return """
        Extract business-focused insights and intelligence from the transcript.
        
        Organize into sections:
        
        KEY STRATEGIES:
        - Strategic approaches and methodologies discussed
        
        MARKET INSIGHTS:
        - Market analysis, trends, and intelligence
        
        OPPORTUNITIES:
        - Business opportunities and potential areas for growth
        
        CHALLENGES:
        - Challenges, obstacles, and potential risks mentioned
        
        Focus on actionable business intelligence that can inform decision-making.
        """
    
    def get_chat_prompt(self, transcript_text: str, chat_history: list) -> str:
        """Get prompt for chat functionality"""
        
        history_context = ""
        if chat_history:
            history_context = "\n\nPrevious conversation:\n"
            for entry in chat_history[-5:]:  # Last 5 exchanges
                history_context += f"Human: {entry['question']}\nAI: {entry['answer']}\n\n"
        
        return f"""
        You are an AI assistant that can answer questions about the following video transcript.
        Be helpful, accurate, and cite specific parts of the transcript when relevant.
        
        Guidelines:
        - Answer based on the transcript content
        - If information isn't in the transcript, say so clearly
        - Provide specific quotes or references when possible
        - Be conversational but informative
        - If asked about timestamps, note that you don't have access to exact timing
        
        Transcript: {transcript_text}
        
        {history_context}
        
        Please provide a comprehensive answer based on the transcript content.
        """