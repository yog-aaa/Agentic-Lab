from typing import Literal

from pydantic import BaseModel, Field


class QAResult(BaseModel):
    status: Literal['PASS', "FAIL"]
    tests_passed: int = Field(ge=0, description="Jumlah tes yang berhasil")
    tests_failed: int = Field(ge=0, description="Jumlah tes yang gagal")
    failures: list[str] = Field(default_factory=list, description="Daftar kegagalan tes")