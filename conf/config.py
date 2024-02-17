import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    HOST: str = os.getenv("HOST", None)
    PORT: str = os.getenv("PORT", "8765")
