import os
import json
import google.generativeai as genai
from typing import Dict, Any, List

class EdithAgent:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyCEPT8wg1u626du1yhsJ1QCUCym5oaPUwc")
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY environment variable not set. LLM functionality will not work.")
        else:
            genai.configure(api_key=self.api_key)
            
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
            "response_mime_type": "application/json",
        }
        
        # We use a system prompt to instruct the model on its persona and output format
        self.system_instruction = """You are EDITH (Even Dead, I'm The Hero), a highly intelligent and efficient AI assistant.
Your responsibilities:
1. Voice Command Execution: Convert user commands into executable actions.
2. Dual Mode System: Decide if a command is an Action or just a Chat.
3. Strict Directness: If the user asks a question or for a list, output ONLY the direct answer or the list items. NEVER use introductory or concluding phrases (like "Here is the list", "Sure", "These are..."). Just output the raw list.

You MUST respond strictly in the following JSON format:
{
  "mode": "action" | "chat",
  "action_type": "click_link" | "scroll_up" | "scroll_down" | "go_back" | "open_url" | "search_google" | "open_app" | "close_app" | "type_text" | "volume_up" | "volume_down" | "mute" | "stop" | "none",
  "action_args": {},
  "response": "Your natural spoken response here."
}

Action Type Arguments Mapping (for action_args):
- open_url: {"url": "https://..."}
- click_link: {"text": "the text of the link to click"}
- search_google: {"query": "search query"}
- open_app: {"app_name": "name of application"}
- close_app: {"app_name": "name of application"}
- type_text: {"text": "text to type"}
- all other actions: {}

If the user gives an unclear command, set mode to "chat", action_type to "none", and response to a clarifying question.
"""
        
        if self.api_key:
            self.model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                generation_config=self.generation_config,
                system_instruction=self.system_instruction
            )
            self.chat_session = self.model.start_chat(history=[])
        else:
            self.model = None
            self.chat_session = None

    def process_query(self, query: str) -> Dict[str, Any]:
        if not self.model:
            return {
                "mode": "chat",
                "action_type": "none",
                "action_args": {},
                "response": "I cannot process that request because my API key is not configured."
            }
            
        try:
            response = self.chat_session.send_message(query)
            # The response should be pure JSON based on our configuration
            json_str = response.text.strip()
            # Handle potential markdown fencing
            if json_str.startswith("```json"):
                json_str = json_str[7:-3].strip()
            elif json_str.startswith("```"):
                json_str = json_str[3:-3].strip()
                
            return json.loads(json_str)
        except Exception as e:
            print(f"Error in LLM processing: {e}")
            return {
                "mode": "chat",
                "action_type": "none",
                "action_args": {},
                "response": "I encountered an error while trying to process your command. Let me try another way."
            }

    def notify_error(self, error_msg: str):
        """Used to feed an error back into the context so EDITH knows an action failed."""
        if self.chat_session:
            try:
                self.chat_session.send_message(f"SYSTEM: The previous action failed with error: {error_msg}")
            except:
                pass
