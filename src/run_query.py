import os
import time
import json
import argparse
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from safety import is_safe_query
from legal_filter import apply_legal_filter


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
    """Processes the user query using a multi-agent approach with Groq and OpenAI."""
    
    # 1. Safety Layer (AI Moderation)
    is_safe, safety_feedback = is_safe_query(user_question)

    # 2. Legal Merit Filter (Using Groq/Llama)
    start_filter = time.time()
    filter_result = apply_legal_filter(user_question)
    filter_latency = int((time.time() - start_filter) * 1000)
    
    if not filter_result["is_legal_matter"]:
        # We define the variable EXACTLY here
        filtered_result = {
            "timestamp": datetime.now().isoformat(),
            "query": user_question,
            "status": "filtered",
            "reasoning": filter_result["reasoning"],
            "suggestion": filter_result["suggestion"],
            "safety_audit": {
                "is_flagged": not is_safe,
                "analysis": safety_feedback if not is_safe else "Clear"
            },
            "metrics": {
                "llm_used": "Llama-3.3-70b (Groq)",
                "latency_ms": filter_latency,
                "estimated_cost_usd": 0.00 
            }
        }
        
        save_metrics(filtered_result)
        return filtered_result

    # 3. Specialist Legal Agent (OpenAI)
    system_prompt = load_prompt("prompts/main_prompt.txt")
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            timeout=15.0
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        output_dict = json.loads(response.choices[0].message.content)
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
                "llm_used": "GPT-4o-mini (OpenAI)",
                "latency_ms": latency_ms,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "estimated_cost_usd": estimated_cost
            }
        }

        save_metrics(final_result)
        return final_result
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # 1. Create the parser object
    parser = argparse.ArgumentParser(description="Legal Assistant CLI")
    
    # 2. Add the 'query' argument. 
    # '-q' is the short version, '--query' the long one.
    parser.add_argument(
        '-q', '--query', 
        type=str, 
        required=True, 
        help='The legal situation to analyze'
    )

    # 3. Capture the arguments
    args = parser.parse_args()
    
    # 4. Use the captured argument in your existing function
    result = run_legal_query(args.query)
    
    # 5. Show the final result
    print(json.dumps(result, indent=2, ensure_ascii=False))