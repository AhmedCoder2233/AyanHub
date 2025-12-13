import os
import textwrap
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up AsyncOpenAI provider using Gemini API
provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

# Load model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", openai_client=provider
)

# Agent for human-style replies
agent = Agent(
    name="Friendly File Agent",
    instructions="""
You are a friendly assistant. When user asks to create folders/files or projects:
- Just give a friendly response like:
  ✅ Folder created!
  📁 File saved!
  🚀 Todo app code written!
- Do NOT return any code or explanation.
- User will not see the actual Python code.
""",
    model=model,
)

# Agent to generate raw Python code
code_agent = Agent(
    name="Code Generator",
    instructions="""
You are a code executor. When the user requests to:
- create folder,
- make a file,
- write some code in a file,

you will respond with only raw, valid Python code using 'os', 'open', etc.
Do NOT return triple backticks, no explanation, no markdown.
Just raw Python code only.
""",
    model=model,
)

# Main loop
while True:
    user_input = input("\n🧑 User: ")

    if user_input.lower() in ["exit", "quit"]:
        print("👋 Exiting...")
        break

    # Get friendly user response
    friendly_response = Runner.run_sync(agent, user_input)
    print("🤖:", friendly_response.final_output.strip())

    # Get raw Python code from code agent
    result = Runner.run_sync(code_agent, user_input)
    python_code = result.final_output.strip()

    # Clean any formatting (just in case)
    python_code = python_code.replace("```python", "").replace("```", "").strip()
    python_code = textwrap.dedent(python_code)

    # Debug: Uncomment this line if you want to see generated code
    # print("\n[DEBUG Python Code]\n", python_code)

    # Execute code
    try:
        exec(python_code)
        print("✅ Code executed successfully!")
    except Exception as e:
        print("❌ Error during execution:", e)
