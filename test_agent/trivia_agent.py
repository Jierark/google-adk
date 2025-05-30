from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Model to use
MODEL_OPENAI = "openai/gpt-4.1-2025-04-14"

trivia_agent = Agent(
    name = "trivia_agent",
    model = LiteLlm(model=MODEL_OPENAI),
    description="An agent who gives out trivia facts.",
    instruction="You are a trivia guru. You answer queries that ask for random trivia facts and respond accordingly.'"
)