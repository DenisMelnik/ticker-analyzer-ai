from crewai import Agent
from crewai_tools import BraveSearchTool


class NewsAgent:
    """
    CrewAI agent for searching and summarizing news using the Brave Search API.
    """
    def __init__(self, role: str = "News Researcher", goal: str = "Find and summarize the latest news about a stock ticker.", llm=None):
        self.brave_search_tool = BraveSearchTool()
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory="An expert in financial news research, skilled at finding and summarizing relevant news articles for stock analysis.",
            tools=[self.brave_search_tool],
            llm=llm,
            verbose=True,
        ) 