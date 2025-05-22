import logging
from typing import Any

import yfinance as yf
from crewai import Agent
from crewai.tools import tool

logger = logging.getLogger(__name__)

@tool("Fetch Price Data Tool")
def fetch_price_data_tool(ticker: str, days: int = 30) -> dict[str, Any] | None:
    """Fetch historical price data for a given ticker using Yahoo Finance."""
    logger.info(f"Fetching price data for ticker: {ticker}, days: {days}")
    
    try:
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(period=f"{days}d")
        if hist.empty:
            logger.error(f"No price data found for ticker: {ticker}")
            return None
        
        data = []
        for idx, row in hist.iterrows():
            data_point = {
                "date": str(idx.date()),
                "open": row["Open"],
                "close": row["Close"],
                "high": row["High"],
                "low": row["Low"],
                "volume": int(row["Volume"])
            }
            data.append(data_point)
            
        moving_average = hist["Close"].mean()
        volatility = hist["Close"].std()
        
        return {
            "ticker": ticker,
            "data": data,
            "moving_average": moving_average,
            "volatility": volatility
        }
    except Exception as e:
        logger.error(f"Error fetching price data for {ticker}: {e}")
        return None

class PriceAgent:
    """
    CrewAI agent for analyzing price data and trends.
    """
    def __init__(self, role: str = "Price Analyst", goal: str = "Analyze price trends for a valid ticker.", llm=None):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory="A financial analyst skilled in analyzing stock price data.",
            tools=[fetch_price_data_tool],
            llm=llm,
            verbose=True,
        ) 