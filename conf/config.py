import os
from dotenv import load_dotenv

load_dotenv()

class Environment:
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: str = os.getenv("PORT", "8765")
