from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect

BACKEND = Path(__file__).resolve().parents[1]
TABLES = {"users", "contact_methods", "complaints", "audit_events"}


def _config(url: str) -> Config:
    cfg = Config(str(BACKEND / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND / "migrations"))
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def test_migration_applies_and_rolls_back(tmp_path):
    url = f"sqlite:///{tmp_path / 'm.db'}"
    cfg = _config(url)

    command.upgrade(cfg, "head")
    assert TABLES <= set(inspect(create_engine(url)).get_table_names())

    command.downgrade(cfg, "base")
    assert not TABLES & set(inspect(create_engine(url)).get_table_names())
