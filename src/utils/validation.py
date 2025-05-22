import logging
from collections import namedtuple

import yfinance as yf

# Simple named tuple instead of Pydantic model
TickerValidationResult = namedtuple('TickerValidationResult', 
                                   ['ticker', 'is_valid', 'company_name', 'error_message'])

logger = logging.getLogger(__name__)

def validate_ticker_symbol(ticker: str) -> TickerValidationResult:
    """
    Validate a stock ticker symbol using Yahoo Finance.
    Returns a TickerValidationResult named tuple.
    """
    # Basic input validation
    if not ticker or not isinstance(ticker, str):
        return TickerValidationResult(
            ticker=str(ticker),
            is_valid=False,
            company_name=None,
            error_message="Ticker symbol must be a non-empty string."
        )
    
    logger.info(f"Validating ticker symbol: {ticker}")
    
    try:
        # Try to get ticker info - this will fail with 404 for invalid tickers
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        # If we got here, check if we have a company name
        company_name = info.get("shortName")
        if company_name:
            return TickerValidationResult(
                ticker=ticker,
                is_valid=True,
                company_name=company_name,
                error_message=None
            )
        else:
            # Valid ticker but no company name, use ticker as fallback
            return TickerValidationResult(
                ticker=ticker,
                is_valid=True,
                company_name=ticker,
                error_message=None
            )
            
    except Exception as e:
        # Most errors will be 404 for invalid tickers
        if "404" in str(e):
            # Log technical details at debug level, let controller handle user-facing error
            logger.debug(f"HTTP 404 error for ticker {ticker}: {e}")
            return TickerValidationResult(
                ticker=ticker,
                is_valid=False,
                company_name=None,
                error_message=f"Ticker symbol '{ticker}' does not exist."
            )
        
        # Handle any other errors generically
        logger.debug(f"Error validating ticker {ticker}: {e}", exc_info=True)
        return TickerValidationResult(
            ticker=ticker,
            is_valid=False,
            company_name=None,
            error_message=f"Error validating ticker '{ticker}'. Please try again."
        ) 