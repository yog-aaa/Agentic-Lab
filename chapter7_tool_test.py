from tools import READ_FILE_SCHEMA, read_file

print("=== TOOL SCHEMA ===")
print(READ_FILE_SCHEMA)

print("=== TOOL RESULT ===")
result = read_file("sample.txt")
print(result)