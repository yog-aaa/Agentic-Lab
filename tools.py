from pathlib import Path

WORKSPACE_ROOT = (Path(__file__).parent / "workspace").resolve()


def read_file(path: str) -> str:
    target = (WORKSPACE_ROOT / path).resolve()

    if not target.is_relative_to(WORKSPACE_ROOT):
        raise PermissionError("File berada di luar direktori workspace.")
    if not target.is_file():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    return target.read_text(encoding="utf-8")


READ_FILE_SCHEMA = {
    "name": "read_file",
    "description": "Membaca file teks UTF-8 di dalam workspace.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path file relatif dari direktori workspace.",
            }
        },
        "required": ["path"],
    },
}
