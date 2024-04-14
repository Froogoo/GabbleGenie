#!pip install -U -q google-generativeai
import google.generativeai as genai
import json
from pathlib import Path
import textwrap

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def save_conversation_as_text(data, output_filename):
    with open(output_filename, 'w') as file:
        if data.get("users"):
            for user in data["users"]:
                file.write(f"{user['name']}: {user['bio']}\n")
        file.write("\nGoal: " + data.get("conversation_goals", ["No goal specified"])[0] + "\n")
        file.write("Environment: " + data.get("environment", "No environment specified") + "\n\n")
        for conversation in data.get("conversations", []):
            if conversation['text']:
                file.write(f"{conversation['date']}，{conversation['speaker']}: {conversation['text']}\n")

def analyze_conversation_with_gemini(text_data, model):
    # prompt = "Give me detailed strcture decision tree and labeled nodes to forcast the conversation flow with numbered probability align with the goal, and numeric Awkwardness Level and Goal Achievement Likelihood, in a json like format for further nodes visualization"
    # response = model.generate_content([prompt, text_data])
    response = model.generate_content(textwrap.dedent("""\
    Generate a detailed decision tree that forecasts conversation flow. Each node should be structured and numbered as follows:

    {
      "nodeNumber": int,
      "text": str,
      "user":str,
      "type": str,
      "awkwardnessLevel": int,
      "goalAchievementLikelihood": float,
      "children": [
        {
          "nodeNumber": int,
          "text": str,
          "user":str,
          "type": str,
          "awkwardnessLevel": int,
          "goalAchievementLikelihood": float
          // additional children nodes can be nested here, with each having a unique node number
        }
      ]
    }

    The detailed strcture tree and labeled nodes should include:
    - consider carefully on users
    - consider major transition points for the whole conversation
    - don't use gemini, try to use predicted user
    - forcast all the conversation flow with numbered probability align with the goal
    - Small talk variations based on the conversation and users and environment I provided
    - Transition to main conversation goals, consider users bio and environment
    - Each node should specify the 'awkwardnessLevel' and 'goalAchievementLikelihood', represented as a number and a percentage respectively.
    - Node numbers should be sequential and indicate the path of the conversation flow.

    Please return a JSON-like structure for visualization of this conversation decision tree.
    """)+text_data)
    return response.text

def main():
    data = load_data('conversation_data.json')
    save_conversation_as_text(data, 'conversations.txt')
    GOOGLE_API_KEY = 'APIKEY'
    genai.configure(api_key=GOOGLE_API_KEY)
    with open('conversations.txt', 'r') as file:
        text_data = file.read()
    model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
    analysis_result = analyze_conversation_with_gemini(text_data, model)
    with open('analysis_results.txt', 'w') as f:
        f.write(analysis_result)
if __name__ == '__main__':
    main()