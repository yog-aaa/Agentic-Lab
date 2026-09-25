from main import create_provider
from parsers import (AgentOutputValidationError, parse_qa_result)

provider = create_provider(name="openrouter")

prompt = """
anda adalah QA agent

Hasil Pengujian:
- 7 test berhasil
- 1 test gagal
- Rest yang gagal: test_devide_zero

kembalikan hasil hanya sebagai json valid dengan struktur:

{
    "status": "FAIL atau PASS",
    "tests_passed": integer,
    "tests_failed": integer,
    "failures": ["nama test yang gagal"]
}

jangan gunakan markdown.
jangan gunakan ```json.
jangan tambahkan penjelasan sebelum atau sesudah json.
"""

raw_response= provider.generate(prompt)


print("=== RAW RESPONSE ===")
print(raw_response)


try:
    result = parse_qa_result(raw_response)
except AgentOutputValidationError as e:
    print("=== VALIDATION ERROR ===")
    print(e)
else:
    print("=== VALIDATED RESULT ===")
    print(result)
    print(f"Status: {result.status}")
    print("Test passed:", result.tests_passed)
    print("Test failed:", result.tests_failed)
    print("Failures:", result.failures)
    
    if result.status == "PASS":
        print("Keputusan workflow: Selesai!")
    else:
        print("Keputusan workflow: Kirim ke Bug Fix Agent")