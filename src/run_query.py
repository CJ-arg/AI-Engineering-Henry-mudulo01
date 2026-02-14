import os
import time
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from safety import is_safe_query

# 1. We load the variables from the .env file
load_dotenv()

# 2. Configure the OpenAI client
# It will automatically search for the OPENAI_API_KEY variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PRICE_PROMPT_1M = 0.15
PRICE_COMPLETION_1M = 0.60

def calculate_cost(prompt_tokens, completion_tokens):
    cost = ((prompt_tokens / 1_000_000) * PRICE_PROMPT_1M) + \
           ((completion_tokens / 1_000_000) * PRICE_COMPLETION_1M)
    return round(cost, 6)

def save_metrics(metrics_data):
    filepath = "metrics/metrics.json"
    
    # If the file already exists, we read the above
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []
    else:
        history = []
    
    history.append(metrics_data)
    
    # We saved the updated list
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def load_prompt(filepath):
    """Read the prompt file from the prompts/ folder"""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
    
def run_legal_query(user_question):
    """Processes the user query after passing a safety check."""
    
    # 1. Safety Layer (AI Moderation) - Audit mode (non-blocking)
    is_safe, safety_feedback = is_safe_query(user_question)

    # Send the query to OpenAI and measure basic metrics
    system_prompt = load_prompt("prompts/main_prompt.txt")

    # We recorded the start time for the latency metric
    start_time = time.time()

    # API call (The gpt-4o-mini model is cheap and fast)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            response_format={"type": "json_object"}, # We forced JSON output
            timeout=15.0 # Set timeout to prevent terminal hanging
        )
        # We calculate latency in milliseconds
        latency_ms = int((time.time() - start_time) * 1000)

        # We extract the text response and convert it to a Python object (dict)
        output_dict = json.loads(response.choices[0].message.content)

        # We extract token metrics
        usage = response.usage
        estimated_cost = calculate_cost(usage.prompt_tokens, usage.completion_tokens)

        final_result = {
            "timestamp": datetime.now().isoformat(),
            "query": user_question,
            "data": output_dict,
            "safety_audit": {
                "is_flagged": not is_safe,
                "analysis": safety_feedback if not is_safe else "Clear"
            },
            "metrics": {
                "latency_ms": latency_ms,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "estimated_cost_usd": estimated_cost # money cost
            }
        }

        save_metrics(final_result)

        return final_result
        
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    # Quick test to see if it works
    question = "se me escapo el canario"
    result = run_legal_query(question)
    print(json.dumps(result, indent=2, ensure_ascii=False))