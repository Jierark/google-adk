# Central agent which coordinates responses
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Import agents to use
from morning_agent.news_agent import news_agent
from morning_agent.trivia_agent import trivia_agent

# Model to use
MODEL_OPENAI = "openai/gpt-4.1-2025-04-14"

# Coordinator structure. Note the use of subagents
root_agent = Agent(
    name="root_agent",
    model=LiteLlm(model=MODEL_OPENAI),
    description="Agent which coordinates getting the news and giving random trivia facts.",
    sub_agents=[news_agent,trivia_agent],
)