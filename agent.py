from dataclasses import dataclass

from google import genai
from google.genai import types

from tools import READ_FILE_SCHEMA, read_file


@dataclass
class Agent:
    name: str
    instructions: str
    client: genai.Client
    model: str
    max_steps: int = 4

    def run(self, task: str) -> str:
        tool = types.Tool(function_declarations=[READ_FILE_SCHEMA])

        config = types.GenerateContentConfig(
            system_instruction=self.instructions,
            tools=[tool],
            automatic_function_calling=(
                types.AutomaticFunctionCallingConfig(disable=True)
            ),
        )

        messages = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=task)],
            )
        ]

        for step in range(1, self.max_steps + 1):
            print(f"[{self.name}] Step {step}/{self.max_steps}")

            response = self.client.models.generate_content(
                model=self.model,
                contents=messages,
                config=config,
            )

            if not response.function_calls:
                if not response.text:
                    raise RuntimeError("Model tidak memberikan jawaban.")

                return response.text

            model_content = response.candidates[0].content
            messages.append(model_content)

            for function_call in response.function_calls:
                print(f"[{self.name}] Meminta tool: {function_call.name}")
                print(f"[{self.name}] Arguments: {function_call.args}")

                tool_result = self.execute_tool(
                    name=function_call.name,
                    arguments=dict(function_call.args or {}),
                )

                print(f"[{self.name}] Tool selesai.")

                tool_response = types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": tool_result},
                )

                messages.append(
                    types.Content(
                        role="tool",
                        parts=[tool_response],
                    )
                )

        raise RuntimeError(f"Agent melewati batas {self.max_steps} steps.")

    def execute_tool(
        self,
        name: str,
        arguments: dict,
    ) -> str:
        if name != "read_file":
            raise ValueError(f"Tool tidak dikenal: {name}")

        path = arguments.get("path")

        if not isinstance(path, str):
            raise TypeError("Argument path harus berupa string.")

        return read_file(path)
