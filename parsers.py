import json

from pydantic import ValidationError

from schemas import QAResult


class AgentOutputValidationError(Exception):
    pass


def parse_qa_result(raw: str) -> QAResult:
    try:
        data = json.loads(raw)
        return QAResult.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as error:
        raise AgentOutputValidationError(f"Validasi QAResult gagal: {error}") from error
