import logging

from crewai import Agent

logger = logging.getLogger(__name__)

class SentimentAgent:
    """
    CrewAI agent for analyzing sentiment of news articles.
    Uses the LLM's inherent capabilities for sentiment analysis.
    """
    def __init__(self, role: str = "Sentiment Analyst", goal: str = "Analyze sentiment of news articles.", llm=None):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory="""
                You are an expert in sentiment analysis for financial news and market data.
                You understand context, nuance, sarcasm, and implicit sentiment in financial reporting.
                You can identify subtle indicators of market sentiment in text that might not use obvious sentiment words.
                
                When analyzing sentiment:
                1. Consider the overall tone (positive, negative, or neutral)
                2. Identify key phrases that signal sentiment
                3. Recognize financial context and industry-specific language
                4. Assess the implied sentiment beyond just the words used
                5. Quantify sentiment on a scale from -1.0 (very negative) to 1.0 (very positive)
                
                Always provide reasoning for your sentiment assessments and highlight specific phrases that influenced your analysis.
            """,
            llm=llm,
            verbose=True,
        ) 