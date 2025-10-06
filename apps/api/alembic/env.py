from __future__ import annotations
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from alembic import context
from sqlalchemy import create_engine


config = context.config
if config.config_file_name is not None:
fileConfig(config.config_file_name)


target_metadata = None


def run_migrations_offline() -> None:
url = config.get_main_option("sqlalchemy.url")
context.configure(url=url, literal_binds=True, dialect_opts={"paramstyle": "named"})
with context.begin_transaction():
context.run_migrations()




def run_migrations_online() -> None:
connectable = create_engine(config.get_main_option("sqlalchemy.url"))
with connectable.connect() as connection:
context.configure(connection=connection, target_metadata=target_metadata)
with context.begin_transaction():
context.run_migrations()


if context.is_offline_mode():
run_migrations_offline()
else:
run_migrations_online()
