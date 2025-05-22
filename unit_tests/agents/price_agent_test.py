from unittest.mock import ANY, MagicMock, patch

from src.agents.price_agent import PriceAgent

# Since we cannot call the decorated fetch_price_data_tool directly,
# we'll test the internal function by patching the decorator

class MockTool:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

@patch('src.agents.price_agent.tool', side_effect=lambda name: lambda f: MockTool(f))
@patch('src.agents.price_agent.yf.Ticker')
def test_fetch_price_data_tool_success(mock_yf_ticker, mock_tool, mock_ticker):
    """Test fetch_price_data_tool with successful data retrieval."""
    # Import here after mocking the decorator
    from src.agents.price_agent import fetch_price_data_tool
    
    mock_yf_ticker.return_value = mock_ticker
    
    result = fetch_price_data_tool.func("AAPL", days=10)
    
    assert isinstance(result, dict)
    assert result["ticker"] == "AAPL"
    assert isinstance(result["data"], list)
    assert "moving_average" in result
    assert "volatility" in result


@patch('src.agents.price_agent.tool', side_effect=lambda name: lambda f: MockTool(f))
@patch('src.agents.price_agent.yf.Ticker')
def test_fetch_price_data_tool_empty_data(mock_yf_ticker, mock_tool):
    """Test fetch_price_data_tool with empty data."""
    # Import here after mocking the decorator
    from src.agents.price_agent import fetch_price_data_tool
    
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = MagicMock()
    mock_ticker.history.return_value.empty = True
    mock_yf_ticker.return_value = mock_ticker
    
    result = fetch_price_data_tool.func("AAPL", days=10)
    
    assert result is None


@patch('src.agents.price_agent.tool', side_effect=lambda name: lambda f: MockTool(f))
@patch('src.agents.price_agent.yf.Ticker')
def test_fetch_price_data_tool_exception(mock_yf_ticker, mock_tool):
    """Test fetch_price_data_tool with exception."""
    # Import here after mocking the decorator
    from src.agents.price_agent import fetch_price_data_tool
    
    mock_yf_ticker.side_effect = Exception("Test exception")
    
    result = fetch_price_data_tool.func("AAPL", days=10)
    
    assert result is None


def test_price_agent_initialization():
    """Test PriceAgent initialization."""
    agent = PriceAgent()
    
    assert agent.agent is not None
    assert agent.agent.role == "Price Analyst"
    assert "Analyze price trends" in agent.agent.goal
    assert len(agent.agent.tools) == 1  # Check that we have one tool


@patch('src.agents.price_agent.Agent')
def test_price_agent_custom_initialization(mock_agent_class):
    """Test PriceAgent initialization with custom parameters."""
    # Setup mock Agent class
    mock_agent_instance = MagicMock()
    mock_agent_class.return_value = mock_agent_instance
    
    custom_role = "Custom Analyst"
    custom_goal = "Custom goal"
    custom_llm = MagicMock()
    
    PriceAgent(role=custom_role, goal=custom_goal, llm=custom_llm)
    
    # Verify Agent was created with correct parameters
    mock_agent_class.assert_called_once_with(
        role=custom_role,
        goal=custom_goal,
        backstory=ANY,
        tools=ANY,
        llm=custom_llm,
        verbose=True
    ) 