# Simple AI Chatbot

A beginner-friendly chatbot built with Python, Streamlit, and the Groq API. It answers questions using information stored in `knowledge.json` and keeps conversation history in Streamlit session state.

## Features

- Streamlit chat interface using `st.chat_message()` and `st.chat_input()`
- Groq API with the `openai/gpt-oss-20b` model
- Knowledge loaded from `knowledge.json`
- Conversation history stored in `st.session_state`
- Button to clear the conversation
- Basic handling of missing API keys, invalid JSON, and API errors

## Requirements

- Python 3.9 or newer
- A Groq API key from <https://console.groq.com/keys>

> This project uses Groq, not Gemini. Set `GROQ_API_KEY` in the `.env` file.

## 1. Open the project folder

Download and extract the project ZIP, then open a terminal in the extracted folder. Make sure these files are in the same folder:

- `app.py`
- `knowledge.json`
- `.env`
- `.gitignore`
- `requirements.txt`
- `README.md`

## 2. Create a virtual environment (recommended)

Create the environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\\Scripts\\Activate.ps1
```

If you use Windows Command Prompt instead of PowerShell:

```bat
.venv\\Scripts\\activate.bat
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

## 3. Install dependencies

Run:

```bash
python -m pip install -r requirements.txt
```

## 4. Configure your Groq API key

Open `.env` in a text editor. Replace the placeholder with your real Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Get a key at <https://console.groq.com/keys>. Do not add quotation marks unless your key requires them, and never share or commit your real API key. The `.gitignore` file excludes `.env` from Git.

## 5. Customize the chatbot knowledge

Edit `knowledge.json` and save it as valid JSON. For example:

```json
{
  "about": "Example information about my project",
  "faq": [
    {
      "question": "What are your opening hours?",
      "answer": "Monday to Friday, 9:00 AM to 5:00 PM."
    }
  ]
}
```

The chatbot sends this content to the model as context. Do not put confidential or sensitive information in this file.

## 6. Run the app

With the virtual environment activated, run:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (usually <http://localhost:8501>).

## Troubleshooting

- **API key missing:** Check that `.env` is in the same folder as `app.py` and that the variable is named `GROQ_API_KEY`.
- **API request fails:** Confirm your key is valid, your internet connection works, and the selected model is available to your Groq account.
- **JSON error:** Check `knowledge.json` for valid JSON syntax. Property names and text values must use double quotes, and there must be no trailing commas.
- **Command not found:** Check that Python is installed and that your virtual environment is activated.

## Notes

- Conversation history is stored in `st.session_state`; it is not saved to a database and may reset when the session ends or restarts.
- The `.env` file included in the project contains only a placeholder. Add your own key before using the chatbot.
