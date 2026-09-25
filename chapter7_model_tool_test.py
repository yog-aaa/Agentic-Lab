import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools import READ_FILE_SCHEMA, read_file

load_dotenv()

tool = types.Tool(
    function_declarations=[READ_FILE_SCHEMA],  # Daftar deklarasi fungsi alat
)

config = types.GenerateContentConfig(
    tools=[tool],  # Daftar alat yang tersedia
    automatic_function_calling=(types.AutomaticFunctionCallingConfig(disable=True)),
)

with genai.Client(
    api_key=os.environ["GEMINI_API_KEY"],
) as client:
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemma-3-26b-a4b-it"),
        contents=(
            "Gunakan tool yang tersedia untuk membaca",
            "file sample.txt jangan menebak isi file.",
        ),
        config=config,
    )

print("=== MODEL RESPONSE ===")

if not response.function_calls:
    print("Model tidak meminta tool.")
    print("Text: ", response.text)
else:
    for function_call in response.function_calls:
        print("Tool name:", function_call.name)
        print("Arguments:", function_call.args)

        if function_call.name != "read_file":
            raise ValueError(f"Tool tidak dikenal: {function_call.name}")

        arguments = dict(function_call.args or {})
        path = arguments.get("path")

        if not isinstance(path, str):
            raise TypeError("Argumen 'path' harus berupa string.")

        print("=== EXECUTING TOOL ===")
        tool_result = read_file(path)
        print(tool_result)
