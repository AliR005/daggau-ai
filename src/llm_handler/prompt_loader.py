import yaml
from pathlib import Path


def load_system_prompt():
    path = Path(__file__).parent / "prompts" / "system.yaml"

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data["system_prompt"]
