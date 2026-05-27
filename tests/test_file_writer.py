import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.tools.file_writer import write_code_file

def test_write_file():
    code = '''def hello():
    print("Hello from AI!")
'''
    success = write_code_file("test_output/hello.py", code, overwrite=True)
    
    if success:
        print("✅ File written!")
        # Verify content
        content = Path("test_output/hello.py").read_text()
        assert "hello()" in content
        print("✅ Content verified!")
    else:
        print("❌ Failed to write file")

if __name__ == "__main__":
    test_write_file()