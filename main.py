import os

from dotenv import load_dotenv

from providers import (
    GeminiProvider,
    GroqProvider,
    ModelProvider,
    OpenRouterProvider,
)

load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} belum diisi.")

    return value


def create_provider(name) -> ModelProvider:
    provider_name = name.lower()

    if provider_name == "gemini":
        return GeminiProvider(
            api_key=get_required_env("GEMINI_API_KEY"),
            model=os.getenv("GEMINI_MODEL", "gemma-4-26b-a4b-it"),
        )

    if provider_name == "groq":
        return GroqProvider(
            api_key=get_required_env("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        )

    if provider_name == "openrouter":
        return OpenRouterProvider(
            api_key=get_required_env("OPENROUTER_API_KEY"),
            model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        )

    raise ValueError(
        "MODEL_PROVIDER harus berisi gemini, groq, atau openrouter."
    )


def main() -> None:
    provider = create_provider(name="openrouter")
    answer = provider.generate("Apa itu AI?")
    print(answer)


if __name__ == "__main__":
    main()
