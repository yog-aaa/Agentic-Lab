from abc import ABC, abstractmethod

import httpx
from google import genai
from groq import Groq


class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        # Mengirim prompt dan mengembalikan teks
        raise NotImplementedError


class GeminiProvider(ModelProvider):
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text


class GroqProvider(ModelProvider):
    def __init__(self, api_key: str, model: str):
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        content = response.choices[0].message.content
        if content is None:
            raise RuntimeError("Groq tidak mengembalikan respons teks.")

        return content


class OpenRouterProvider(ModelProvider):
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, prompt: str) -> str:
        response = httpx.post(
            self.API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-OpenRouter-Title": "Agentic Dev Lab",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            },
            timeout=60.0,
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise TypeError("OpenRouter tidak mengembalikan respons teks.")

        return content
