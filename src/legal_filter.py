import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load variables to ensure GROQ_API_KEY is available
load_dotenv()

def apply_legal_filter(query):
    """
    Evaluates if the query has legal merit using Groq (Llama 3).
    Saves costs by filtering trivial cases before calling OpenAI.
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    filter_prompt = """
    You are a Legal Triage Assistant. Your job is to decide if a situation 
    needs a lawyer or if it is a trivial, common-sense matter.
    
    Criteria:
    - LEGAL: Labor issues, health insurance denials, accidents, contracts.
    - TRIVIAL: Lost pets (no theft involved), minor neighbor arguments with no damage, etiquette.

    Respond ALWAYS in JSON format:
    {
        "is_legal_matter": true/false,
        "reasoning": "Brief explanation in Spanish",
        "suggestion": "Practical advice in Spanish if not a legal matter"
    }
    """
    
    try:
        # Using Llama-3.3-70b for fast and free classification
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            messages=[
                {"role": "system", "content": filter_prompt},
                {"role": "user", "content": query}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        # Fallback to True to avoid blocking potentially important cases on error
        return {"is_legal_matter": True, "reasoning": str(e), "suggestion": "N/A"}