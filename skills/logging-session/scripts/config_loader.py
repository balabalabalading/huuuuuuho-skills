"""Load configuration from config.json located in the skill root directory."""
import json
import os

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = {
    "db_path": os.path.join(
        os.path.expanduser("~"),
        "Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life/dev_knowledge.db"
    ),
    "obsidian_vault_path": os.path.join(
        os.path.expanduser("~"),
        "Library/Mobile Documents/iCloud~md~obsidian/Documents/vault4life"
    ),
}


def load_config(config_path=None):
    if config_path is None:
        config_path = os.path.join(SKILL_ROOT, "config.json")

    if not os.path.exists(config_path):
        return dict(DEFAULT_CONFIG)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["db_path"] = os.path.expanduser(config.get("db_path", DEFAULT_CONFIG["db_path"]))
    config["obsidian_vault_path"] = os.path.expanduser(
        config.get("obsidian_vault_path", DEFAULT_CONFIG["obsidian_vault_path"])
    )
    return config
