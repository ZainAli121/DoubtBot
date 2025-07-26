from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

app = Flask(__name__)

# In-memory chat history (you can persist this per user/session)
chat_history: list[ChatCompletionMessageParam] = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    chat_history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're DoubtBot, an AI that second-guesses itself, overthinks, hesitates, and sometimes apologizes for being too unsure or too confident."},
                *chat_history
            ],
            temperature=0.8
        )
        bot_reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"Oops, something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
