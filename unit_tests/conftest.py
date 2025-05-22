from unittest.mock import MagicMock

import pandas as pd
import pytest


@pytest.fixture
def mock_ticker():
    """Mock yfinance Ticker object for testing"""
    mock = MagicMock()
    
    # Create mock historical price data
    dates = pd.date_range(start='2023-01-01', periods=10)
    mock_data = pd.DataFrame({
        'Open': [150.0, 151.0, 152.0, 153.0, 154.0, 155.0, 156.0, 157.0, 158.0, 159.0],
        'High': [155.0, 156.0, 157.0, 158.0, 159.0, 160.0, 161.0, 162.0, 163.0, 164.0],
        'Low': [148.0, 149.0, 150.0, 151.0, 152.0, 153.0, 154.0, 155.0, 156.0, 157.0],
        'Close': [152.0, 153.0, 154.0, 155.0, 156.0, 157.0, 158.0, 159.0, 160.0, 161.0],
        'Volume': [1000000, 1100000, 1200000, 1300000, 1400000, 
                  1500000, 1600000, 1700000, 1800000, 1900000]
    }, index=dates)
    
    mock.history.return_value = mock_data
    
    # Mock ticker info
    mock.info = {
        'shortName': 'Test Company',
        'longName': 'Test Company Inc.',
        'sector': 'Technology',
        'industry': 'Software'
    }
    
    return mock 