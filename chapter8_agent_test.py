import os

from dotenv import load_dotenv
from google import genai

from agent import Agent

load_dotenv()

with genai.Client(api_key=os.environ["GEMINI_API_KEY"]) as client:
    agent = Agent(
        name="reader",
        instructions=(
            "Anda adalah agent pembaca file. "
            "Gunakan read_file jika informasi "
            "yang dibutuhkan berada dalam file. "
            "Jawab berdasarkan hasil tool, "
            "bukan berdasarkan tebakan."
        ),
        client=client,
        model=os.getenv(
            "GEMINI_MODEL",
            "gemma-4-26b-a4b-it",
        ),
        max_steps=4,
    )

    answer = agent.run("Baca sample.txt dan jelaskan apa target pembelajaran saat ini.")

print("\n=== FINAL ANSWER ===")
print(answer)
