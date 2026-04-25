import time
import os
from llm_agent import EdithAgent
from browser_ops import BrowserManager

def test_edith():
    # Only test if API key is set
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not set. Cannot test LLM.")
        return

    agent = EdithAgent()
    browser = BrowserManager()

    print("\n--- Test 1: Action Classification (Open URL) ---")
    query = "EDITH, please open google.com"
    print(f"Query: {query}")
    decision = agent.process_query(query)
    print(f"Decision: {decision}")
    
    if decision.get("action_type") == "open_url":
        url = decision.get("action_args", {}).get("url", "https://google.com")
        print(f"Executing: open_url({url})")
        browser.open_url(url)
        time.sleep(2)
        print("Browser opened URL successfully.")
    else:
        print("FAILED to classify open_url")

    print("\n--- Test 2: Chat Mode (General Knowledge) ---")
    query = "What is the capital of France?"
    print(f"Query: {query}")
    decision = agent.process_query(query)
    print(f"Decision: {decision}")
    if decision.get("mode") == "chat":
        print("Chat mode successful.")
    else:
        print("FAILED to classify chat mode")

    print("\nClosing browser...")
    browser.close()
    print("Testing complete.")

if __name__ == "__main__":
    test_edith()
