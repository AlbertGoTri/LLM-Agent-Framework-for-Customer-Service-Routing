import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
load_dotenv(project_root / "environment.env")

# Add project root to path for imports
sys.path.insert(0, str(project_root))

from src.agents import FAQAgent, OrderAgent
from src.router import route_query, initialize_client, get_current_model

# Supported providers and their required API keys
PROVIDERS = {
    "google": "GOOGLE_API_KEY",
    "groq": "GROQ_API_KEY"
}

def Usage():
    print("Usage: python src/main.py <provider>")
    print("  Providers: google, groq")
    print("\nExamples:")
    print("  python src/main.py google  # Google Gemini 2.5 Flash")
    print("  python src/main.py groq    # Groq Llama 3.1 8B")

def run_chat_system():
    faq_agent = FAQAgent()
    order_agent = OrderAgent()
    
    print("--- Customer Service Bot Initialized ---")
    print("Type 'exit' or 'quit' to quit.\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ['exit', 'quit']:
            break

        # Step 1: Route the query using LLM
        intent = route_query(user_query)
        print(f"[DEBUG] Router identified intent: {intent}")

        # Step 2: Dispatch to the correct agent
        response = ""
        
        if intent == "FAQ":
            response = faq_agent.handle(user_query)
        elif intent == "ORDER":
            response = order_agent.handle(user_query)
        else:
            response = "I'm having trouble understanding your request. Please try again."

        # Step 3: Return the agent's response
        print(f"Bot: {response}\n")

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) < 2:
        print("Error: No provider specified.\n")
        Usage()
        sys.exit(1)
    
    provider = sys.argv[1].lower()
    
    # Validate provider
    if provider not in PROVIDERS:
        print(f"Error: Unknown provider '{provider}'.\n")
        Usage()
        sys.exit(1)
    
    # Check API key exists
    api_key_name = PROVIDERS[provider]
    if not os.getenv(api_key_name):
        print(f"Error: {api_key_name} not found in environment.env file.")
        sys.exit(1)
    
    # Initialize the AI client
    try:
        initialize_client(provider)
        model = get_current_model()
        print(f"[INFO] Using {provider.upper()} as AI provider (model: {model})\n")
        run_chat_system()
    except Exception as e:
        print(f"Error initializing client: {e}")
        sys.exit(1)
