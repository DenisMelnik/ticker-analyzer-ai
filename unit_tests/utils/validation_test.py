from unittest.mock import MagicMock, patch

from src.utils.validation import TickerValidationResult, validate_ticker_symbol


@patch('src.utils.validation.yf.Ticker')
def test_validate_ticker_symbol_valid(mock_yf_ticker, mock_ticker):
    """Test ticker validation with a valid ticker symbol."""
    mock_yf_ticker.return_value = mock_ticker
    
    result = validate_ticker_symbol("AAPL")
    
    assert isinstance(result, TickerValidationResult)
    assert result.ticker == "AAPL"
    assert result.is_valid is True
    assert result.company_name == "Test Company"
    assert result.error_message is None


@patch('src.utils.validation.yf.Ticker')
def test_validate_ticker_symbol_valid_no_company_name(mock_yf_ticker):
    """Test ticker validation with valid ticker but no company name."""
    mock_ticker = MagicMock()
    mock_ticker.info = {}  # Empty info dict, no shortName
    mock_yf_ticker.return_value = mock_ticker
    
    result = validate_ticker_symbol("XYZ")
    
    assert isinstance(result, TickerValidationResult)
    assert result.ticker == "XYZ"
    assert result.is_valid is True
    assert result.company_name == "XYZ"  # Fallback to ticker
    assert result.error_message is None


@patch('src.utils.validation.yf.Ticker')
def test_validate_ticker_symbol_invalid_404(mock_yf_ticker):
    """Test ticker validation with an invalid ticker (404 error)."""
    mock_yf_ticker.side_effect = Exception("404 Client Error")
    
    result = validate_ticker_symbol("INVALID")
    
    assert isinstance(result, TickerValidationResult)
    assert result.ticker == "INVALID"
    assert result.is_valid is False
    assert result.company_name is None
    assert "does not exist" in result.error_message


def test_validate_ticker_symbol_empty():
    """Test ticker validation with an empty ticker."""
    result = validate_ticker_symbol("")
    
    assert isinstance(result, TickerValidationResult)
    assert result.ticker == ""
    assert result.is_valid is False
    assert result.company_name is None
    assert "non-empty string" in result.error_message


def test_validate_ticker_symbol_none():
    """Test ticker validation with None ticker."""
    result = validate_ticker_symbol(None)
    
    assert isinstance(result, TickerValidationResult)
    assert result.ticker == "None"
    assert result.is_valid is False
    assert result.company_name is None
    assert "non-empty string" in result.error_message 