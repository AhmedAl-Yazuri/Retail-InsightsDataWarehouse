import json
import os
from pathlib import Path

from sqlalchemy import create_engine, text


def get_db_uri() -> str:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        if db_url.startswith("postgresql://"):
            return db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return db_url

    config_path = Path("config/db_config.json")
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        return (
            f"postgresql+psycopg2://{config['user']}:{config['password']}"
            f"@{config['host']}:{config['port']}/{config['dbname']}"
        )

    raise RuntimeError("No DATABASE_URL env var or config/db_config.json found.")


def main() -> None:
    sql_path = Path("sql/build_dw_from_public.sql")
    sql_text = sql_path.read_text(encoding="utf-8")

    engine = create_engine(get_db_uri())
    with engine.begin() as conn:
        for statement in sql_text.split(";"):
            statement = statement.strip()
            if statement:
                conn.execute(text(statement))

    print("dw schema rebuilt from public tables successfully.")


if __name__ == "__main__":
    main()
