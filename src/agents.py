import re

class FAQAgent:
    def __init__(self):
        # Mock database of FAQs
        self.knowledge_base = {
            "return": "You can return items within 30 days of purchase.",
            "shipping": "Shipping usually takes 3-5 business days.",
            "hours": "We are open Mon-Fri from 9 AM to 5 PM.",
            "location": "We are located at 123 Tech Avenue."
        }

    def handle(self, query):
        # Simple keyword matching for the mock agent
        query_lower = query.lower()
        for key, answer in self.knowledge_base.items():
            if key in query_lower:
                return answer
        return "I'm sorry, I don't have information on that topic in my FAQ."


class OrderAgent:
    def __init__(self):
        # Mock database of Orders
        self.orders = {
            "101": "Shipped - Arriving Tomorrow",
            "102": "Processing - Packing in progress",
            "103": "Delivered - Left at front porch"
        }

    def handle(self, query):
        # Extract numbers from the query to find Order ID
        # "\b" -> word boundary, "\d{3}" -> exactly 3 digits
        match = re.search(r'\b\d{3}\b', query)
        
        if match:
            order_id = match.group()
            status = self.orders.get(order_id)
            if status:
                return f"Order #{order_id} status: {status}"
            else:
                return f"Order #{order_id} not found."
        
        return "Please provide a valid 3-digit order number (e.g., 101)."
