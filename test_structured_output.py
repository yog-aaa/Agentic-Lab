from parsers import parse_qa_result

raw_response = """
{
    "status": "FAIL",
    "tests_passed": 7,
    "tests_failed": 1,
    "failures": ["test_devide_zero"]
}
"""


result = parse_qa_result(raw_response)

print(result)
print(f"Status: {result.status}")
print(f"Jumlah Gagal: {result.tests_failed}")
print(f"Failure Pertama: {result.failures[0]}")

if result.status == "PASS":
    print("Workflow Selesai!")
else:
    print("kirim ke Bug Fix Agent")