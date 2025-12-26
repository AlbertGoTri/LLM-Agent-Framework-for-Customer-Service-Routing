"""
Test dataset for evaluating LLM routing accuracy.
Each test case contains a query and the expected intent (FAQ or ORDER).
"""

TEST_CASES = [
    # FAQ queries - Returns
    {"query": "What is your return policy?", "expected": "FAQ"},
    {"query": "Can I return an item after 30 days?", "expected": "FAQ"},
    {"query": "How do I return something?", "expected": "FAQ"},
    {"query": "Do you accept returns on sale items?", "expected": "FAQ"},
    
    # FAQ queries - Shipping
    {"query": "How long does shipping take?", "expected": "FAQ"},
    {"query": "What are your shipping options?", "expected": "FAQ"},
    {"query": "Do you offer free shipping?", "expected": "FAQ"},
    {"query": "How much does delivery cost?", "expected": "FAQ"},
    
    # FAQ queries - Hours
    {"query": "What are your store hours?", "expected": "FAQ"},
    {"query": "When do you open?", "expected": "FAQ"},
    {"query": "Are you open on weekends?", "expected": "FAQ"},
    {"query": "What time do you close?", "expected": "FAQ"},
    
    # FAQ queries - Location
    {"query": "Where is your store located?", "expected": "FAQ"},
    {"query": "What's your address?", "expected": "FAQ"},
    {"query": "Do you have a physical store?", "expected": "FAQ"},
    
    # ORDER queries - Direct order status
    {"query": "Where is my order 101?", "expected": "ORDER"},
    {"query": "What's the status of order 102?", "expected": "ORDER"},
    {"query": "Track my order 103", "expected": "ORDER"},
    {"query": "Has order 101 shipped yet?", "expected": "ORDER"},
    
    # ORDER queries - Package tracking
    {"query": "Where is my package?", "expected": "ORDER"},
    {"query": "When will my order arrive?", "expected": "ORDER"},
    {"query": "My order hasn't arrived yet", "expected": "ORDER"},
    {"query": "I want to track my delivery", "expected": "ORDER"},
    
    # ORDER queries - Delivery status
    {"query": "Has my order been delivered?", "expected": "ORDER"},
    {"query": "Is my package out for delivery?", "expected": "ORDER"},
    {"query": "When was my order shipped?", "expected": "ORDER"},
    
    # Edge cases / Ambiguous queries
    {"query": "I have a question about my order 101", "expected": "ORDER"},
    {"query": "Can I return order 102?", "expected": "ORDER"},  # Order-specific, not general FAQ
    {"query": "How do returns work?", "expected": "FAQ"},
    {"query": "What happens if my package is lost?", "expected": "FAQ"},
]

def get_test_cases():
    """Returns all test cases."""
    return TEST_CASES

def get_faq_cases():
    """Returns only FAQ test cases."""
    return [tc for tc in TEST_CASES if tc["expected"] == "FAQ"]

def get_order_cases():
    """Returns only ORDER test cases."""
    return [tc for tc in TEST_CASES if tc["expected"] == "ORDER"]
