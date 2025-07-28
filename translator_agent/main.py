# ✅ Install required packages using:
# pip install openai-agents
# pip install python-dotenv

# Importing necessary classes and methods from openai-agents and dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv  # For loading environment variables from .env file
import os  # For operating system-related functions like reading environment variables

# Load variables from the .env file
load_dotenv()

# Read the GEMINI_API_KEY from the environment
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Print the key to confirm it was loaded (for debugging)
print(gemini_api_key)

# Raise an error if the key is not set
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Create an external OpenAI-compatible client for Gemini API
# ✅ Gemini API doc: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",  # Gemini API base URL
)

# Create a model using Gemini through OpenAI-style chat completion interface
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",         # Gemini model name
    openai_client=external_client     # Provide the external Gemini client
)

# Define model configuration settings
config = RunConfig(
    model=model,
    model_provider=external_client,  # Gemini API client as model provider
    tracing_disabled=True            # Disable tracing (optional setting)
)

# Define a Translator Agent with instructions
translator = Agent(
    name='Translator Agent',  # Name of the agent
    instructions="""You are a translator agent that translates text from 
    one Language to another."""  # Agent's job is to translate text
)

# Use the agent to translate an Urdu sentence into English
response = Runner.run_sync(
    translator,
    input="Translate 'میں آج بہت خوش ہوں۔' to English.",  # Input sentence to be translated
    run_config=config  # Pass the model configuration
)

# Print the final translated output
print(response.final_output)
