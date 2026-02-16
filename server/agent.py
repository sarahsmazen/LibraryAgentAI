import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# Handling imports for different execution environments
try:
    from langchain.agents import AgentExecutor, create_openai_functions_agent
except ImportError:
   
    from langchain.agents.agent import AgentExecutor
    from langchain.agents.openai_functions_agent.base import create_openai_functions_agent

# Import custom database tools
try:
    from server.tools import (
        find_books, 
        create_order, 
        restock_book, 
        update_price, 
        order_status, 
        inventory_summary
    )
except ImportError:
    from tools import (
        find_books, 
        create_order, 
        restock_book, 
        update_price, 
        order_status, 
        inventory_summary
    )

# Load Environment Variables
load_dotenv()

def initialize_agent():
    """
    Initializes the AI Library Agent with professional configurations.
    This function links the LLM with the database tools.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")
    
    # Using GPT-4o as the core brain for high accuracy in tool selection
    llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=api_key)

    # Authorized tools for database interaction
    tools = [
        find_books, 
        create_order, 
        restock_book, 
        update_price, 
        order_status, 
        inventory_summary
    ]

    # System Instructions for the Agent
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompt.txt")
    with open(prompt_path, "r") as f:
      system_instructions = f.read()
    prompt = ChatPromptTemplate.from_messages([
       ("system", system_instructions),
        
       # Maintains conversation context
        MessagesPlaceholder(variable_name="chat_history"),
        
        ("user", "{input}"),
        
        # Agent's internal reasoning space
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Constructing the agent with the specified model and tools
    agent = create_openai_functions_agent(llm, tools, prompt)

    # Returning the executor with verbose enabled for transparent reasoning
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )

# Global agent instance
library_agent = initialize_agent()