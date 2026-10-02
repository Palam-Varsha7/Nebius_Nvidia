from pydantic import BaseModel

class CodeResult(BaseModel):
    files: dict[str, str]  # filename -> code
    notes: str = ""

class Finding(BaseModel):
    agent: str      # "testing", "security" or "performance"
    severity: str   # "low", "medium" or "high"
    file: str
    line: int
    message: str

class TestResult(BaseModel):
    __test__ = False  # tells pytest this is not a test class
    passed: bool
    stdout: str = ""
    stderr: str = ""