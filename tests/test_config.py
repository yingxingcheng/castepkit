from pathlib import Path
from castepkit.config import get_exec_path

def test_get_exec_path_uses_dummy():
    path = Path(get_exec_path("shg"))
    assert path.is_file()
    assert path.name == "shg.py"
