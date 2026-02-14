import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def is_safe_query(user_query):
    """
    Uses OpenAI's Moderation endpoint to validate user input.
    Returns (True, None) if safe, (False, error_message) if flagged.
    """
    try:
        # Call the moderation API
        mod_response = client.moderations.create(input=user_query)
        
        # Access the first result safely
        mod_data = mod_response.results[0]

        if mod_data.flagged:
            # Extract categories that were flagged as True
            # Convert the Pydantic model to a dictionary for safe iteration
            flags = mod_data.categories.model_dump()
            violated_names = [name for name, val in flags.items() if val]
            
            return False, f"Content flagged by safety policies: {', '.join(violated_names)}"
        
        # If not flagged, return success
        return True, None
        
    except Exception as e:
        # In case of technical failure, block by precaution
        return False, f"Safety technical error: {str(e)}"