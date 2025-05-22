from crewai import Agent


class RecommendationAgent:
    """
    CrewAI agent for generating a final Buy/Sell/Hold recommendation using an LLM.
    The LLM should output a JSON object with fields: 'ticker', 'action' (Buy/Sell/Hold), 'explanation', and 'references' (list of sources).
    """
    def __init__(self, role: str = "Recommendation Specialist", goal: str = "Analyze price and sentiment data to provide a Buy/Sell/Hold recommendation with a short explanation in JSON format.", llm=None):
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=(
                "A senior analyst who synthesizes all data to make actionable investment recommendations. "
                "Always output a JSON object with fields: 'ticker', 'action' (Buy/Sell/Hold), 'explanation', and 'references' (list of sources)."
            ),
            tools=[],  # No custom tools, rely on LLM
            llm=llm,
            verbose=True,
        ) 