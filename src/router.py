import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
load_dotenv(project_root / "environment.env")

# Global variables
_client = None
_provider = None

# Default models for each provider
DEFAULT_MODELS = {
    "google": "gemini-2.5-flash",
    "groq": "llama-3.1-8b-instant"
}

def initialize_client(provider: str, model: str = None):
    """
    Initialize the AI client based on the provider name.
    Provider can be: 'google' or 'groq'
    """
    global _client, _provider
    _provider = provider.lower()
    
    if _provider == "google":
        from google import genai
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        _client = genai.Client(api_key=api_key)
        
    elif _provider == "groq":
        from openai import OpenAI
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        # Groq uses OpenAI-compatible API
        _client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        
    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'google' or 'groq'")

    return DEFAULT_MODELS.get(_provider) if model is None else model


def get_current_model():
    """Returns the default model for the current provider."""
    return DEFAULT_MODELS.get(_provider)


def route_query(query, model=None):
    """
    Decides whether a query is for the FAQ Agent or Order Status Agent.
    """
    if _client is None:
        raise RuntimeError("Client not initialized. Call initialize_client() first.")
    
    # Use default model if not specified
    if model is None:
        model = DEFAULT_MODELS.get(_provider)
    
    system_prompt = """You are an intelligent router for a customer service bot. 
Classify the user's query into exactly one of these two intents:
1. FAQ_INTENT (General questions about returns, shipping, hours, location)
2. ORDER_INTENT (Specific questions asking about an order status, where is my package, etc.)

Output ONLY the label 'FAQ' or 'ORDER'. Do not add punctuation or explanation."""

    try:
        if _provider == "groq":
            response = _client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0
            )
            intent = response.choices[0].message.content.strip().upper()
            
        elif _provider == "google":
            full_prompt = f"{system_prompt}\n\nUser query: {query}"
            response = _client.models.generate_content(
                model=model,
                contents=full_prompt
            )
            intent = response.text.strip().upper()
        
        return intent

    except Exception as e:
        print(f"Error during routing: {e}")
        return "ERROR"
