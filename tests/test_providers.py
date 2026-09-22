from types import SimpleNamespace

import providers
from providers import GroqProvider, OpenRouterProvider


def test_groq_provider_returns_message_content(monkeypatch):
    provider = GroqProvider(api_key="test-key", model="test-model")

    def fake_create(**kwargs):
        assert kwargs["model"] == "test-model"
        assert kwargs["messages"] == [
            {"role": "user", "content": "Halo"}
        ]
        message = SimpleNamespace(content="Jawaban Groq")
        return SimpleNamespace(
            choices=[SimpleNamespace(message=message)]
        )

    monkeypatch.setattr(
        provider.client.chat.completions,
        "create",
        fake_create,
    )

    assert provider.generate("Halo") == "Jawaban Groq"


def test_openrouter_provider_returns_message_content(monkeypatch):
    provider = OpenRouterProvider(
        api_key="test-key",
        model="test-model",
    )

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "choices": [
                    {"message": {"content": "Jawaban OpenRouter"}}
                ]
            }

    def fake_post(url, **kwargs):
        assert url == OpenRouterProvider.API_URL
        assert kwargs["json"]["model"] == "test-model"
        assert kwargs["json"]["messages"] == [
            {"role": "user", "content": "Halo"}
        ]
        assert kwargs["headers"]["Authorization"] == "Bearer test-key"
        return FakeResponse()

    monkeypatch.setattr(providers.httpx, "post", fake_post)

    assert provider.generate("Halo") == "Jawaban OpenRouter"
