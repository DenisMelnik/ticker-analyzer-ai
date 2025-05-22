from unittest.mock import ANY, MagicMock, patch

from src.controller import analyze_ticker, main


@patch('src.controller.validate_ticker_symbol')
@patch('src.controller.PriceAgent')
@patch('src.controller.NewsAgent')
@patch('src.controller.SentimentAgent')
@patch('src.controller.RecommendationAgent')
@patch('src.controller.Crew')
@patch('src.controller.Task')
def test_analyze_ticker_valid(
    mock_task_class,
    mock_crew_class, 
    mock_recommendation_agent_class,
    mock_sentiment_agent_class, 
    mock_news_agent_class,
    mock_price_agent_class,
    mock_validate_ticker_symbol
):
    """Test analyze_ticker function with a valid ticker."""
    # Setup mocks
    mock_validation_result = MagicMock()
    mock_validation_result.is_valid = True
    mock_validation_result.error_message = None
    mock_validate_ticker_symbol.return_value = mock_validation_result
    
    # Mock Task instances
    mock_price_task = MagicMock()
    mock_news_task = MagicMock()
    mock_sentiment_task = MagicMock()
    mock_recommendation_task = MagicMock()
    
    # Setup Task constructor to return the appropriate mock tasks
    mock_task_class.side_effect = [
        mock_price_task,
        mock_news_task,
        mock_sentiment_task, 
        mock_recommendation_task
    ]
    
    # Mock agents
    mock_price_agent = MagicMock()
    mock_news_agent = MagicMock()
    mock_sentiment_agent = MagicMock()
    mock_recommendation_agent = MagicMock()
    
    # Set up class returns
    mock_price_agent_class.return_value.agent = mock_price_agent
    mock_news_agent_class.return_value.agent = mock_news_agent
    mock_sentiment_agent_class.return_value.agent = mock_sentiment_agent
    mock_recommendation_agent_class.return_value.agent = mock_recommendation_agent
    
    # Mock crew
    mock_crew = MagicMock()
    mock_crew_class.return_value = mock_crew
    mock_crew.kickoff.return_value = "Test results"
    
    # Call the function
    success, error = analyze_ticker("AAPL")
    
    # Verify result
    assert success is True
    assert error is None
    
    # Verify all the expected functions were called
    mock_validate_ticker_symbol.assert_called_once_with("AAPL")
    mock_price_agent_class.assert_called_once()
    mock_news_agent_class.assert_called_once()
    mock_sentiment_agent_class.assert_called_once()
    mock_recommendation_agent_class.assert_called_once()
    
    # Verify Task creation
    assert mock_task_class.call_count == 4
    
    # Verify the crew was created with the correct tasks
    mock_crew_class.assert_called_once_with(
        agents=ANY,
        tasks=ANY,
        verbose=True,
        planning=True
    )
    
    # Verify the kickoff method was called
    mock_crew.kickoff.assert_called_once()


@patch('src.controller.validate_ticker_symbol')
def test_analyze_ticker_invalid(mock_validate_ticker_symbol):
    """Test analyze_ticker function with an invalid ticker."""
    # Setup mock validation result
    mock_validation_result = MagicMock()
    mock_validation_result.is_valid = False
    mock_validation_result.error_message = "Invalid ticker"
    mock_validate_ticker_symbol.return_value = mock_validation_result
    
    # Call the function
    success, error = analyze_ticker("INVALID")
    
    # Verify result
    assert success is False
    assert error == "Invalid ticker"
    
    # Verify validate_ticker_symbol was called
    mock_validate_ticker_symbol.assert_called_once_with("INVALID")


@patch('src.controller.input', side_effect=['AAPL', 'quit'])
@patch('src.controller.analyze_ticker')
def test_main_function(mock_analyze_ticker, mock_input):
    """Test main function with user input."""
    # Setup mock analyze_ticker
    mock_analyze_ticker.return_value = (True, None)
    
    # Call the main function
    main()
    
    # Verify analyze_ticker was called with the right ticker
    mock_analyze_ticker.assert_called_once_with('AAPL') 