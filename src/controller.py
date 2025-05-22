import logging

from crewai import Crew, Task
from dotenv import load_dotenv

from src.agents.news_agent import NewsAgent
from src.agents.price_agent import PriceAgent
from src.agents.recommendation_agent import RecommendationAgent
from src.agents.sentiment_agent import SentimentAgent
from src.utils.validation import validate_ticker_symbol

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_ticker(ticker: str) -> tuple[bool, str | None]:
    """Analyze a stock ticker using the CrewAI agents.
    
    Args:
        ticker: The stock ticker symbol to analyze
        
    Returns:
        Tuple containing:
        - success (bool): Whether the analysis was successful
        - error_message (Optional[str]): Error message if analysis failed, None otherwise
    """
    logger.info(f"Starting analysis for ticker: {ticker}")

    # Validate ticker before proceeding
    validation_result = validate_ticker_symbol(ticker)
    if not validation_result.is_valid:
        logger.debug(f"Ticker validation failed: {ticker}")
        # Only print user-facing message
        print(f"Error: {validation_result.error_message}")
        return False, validation_result.error_message

    try:
        # Initialize agents (default LLM: OpenAI GPT-3.5-turbo if OPENAI_API_KEY is set)
        price_agent = PriceAgent().agent
        news_agent = NewsAgent().agent
        sentiment_agent = SentimentAgent().agent
        recommendation_agent = RecommendationAgent().agent

        # Define tasks
        price_task = Task(
            description=f"Fetch recent price data for {ticker}.",
            expected_output="A summary of price data.",
            agent=price_agent
        )
        news_task = Task(
            description=f"Find and summarize the latest news about {ticker}.",
            expected_output="A summary of the top 3 news articles with links.",
            agent=news_agent,
            context=[price_task]
        )
        sentiment_task = Task(
            description="Analyze the sentiment of the summarized news articles.",
            expected_output="A sentiment score and summary.",
            agent=sentiment_agent,
            context=[news_task]
        )
        recommendation_task = Task(
            description=(
                "Given the price summary and sentiment score, provide a final investment recommendation. "
                "Output a JSON object with: 'ticker', 'action' (Buy/Sell/Hold), 'explanation', and 'references'. "
                "Be concise and base your answer on the provided analysis."
            ),
            expected_output="A JSON object with the recommendation and explanation.",
            agent=recommendation_agent,
            context=[price_task, sentiment_task]
        )

        # Create the Crew
        crew = Crew(
            agents=[price_agent, news_agent, sentiment_agent, recommendation_agent],
            tasks=[price_task, news_task, sentiment_task, recommendation_task],
            verbose=True,
            planning=True
        )

        # Run the Crew
        results = crew.kickoff()
        logger.info(f"Analysis completed successfully for {ticker}")
        print("Final Results:", results)
        return True, None
        
    except Exception as e:
        error_msg = f"Error analyzing ticker {ticker}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

def main():
    """Main function to run the stock ticker analysis with the ability to analyze multiple tickers."""
    print("Welcome to Ticker Analysis Assistant!")
    print("This tool analyzes stock tickers and provides investment recommendations.")
    
    while True:
        ticker = input("\nEnter a stock ticker symbol (e.g., AAPL) or 'quit' to exit: ").strip().upper()
        
        if ticker.lower() in ('quit', 'exit', 'q'):
            print("Thank you for using Ticker Analysis Assistant. Goodbye!")
            break
        
        if not ticker:
            print("Please enter a valid ticker symbol.")
            continue
        
        success, error = analyze_ticker(ticker)
        
        if success:
            print("\n" + "-" * 80)
            print(f"Analysis for {ticker} completed.")
            print("-" * 80)
        else:
            print("\n" + "-" * 80)
            print(f"Analysis for {ticker} failed: {error}")
            print("-" * 80)

if __name__ == "__main__":
    main() 