from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "storage" / "aid.db"
LOG_DIR = BASE_DIR / "logs"
LOG_CONFIG = BASE_DIR / "core" / "logging_config.json"
CLANG_PATH = "C:\\Program Files\\LLVM\\bin\\libclang.dll"

CF_KEY = "472617f3caaf831c7c98f30a50a7b3e10cd218e0"
CF_SECRET = "364629748a398f731dfea991b74fbd9e019c796f"

#Now sapported languages is: python as "py", c++ compiler with clang as "c++"
INCLUDING_LANGUAGE = ('py') 
