import json
from pathlib import Path

import click

from .config import DatabaseConfig
from .engine import EngineManager
from .inspect import inspect_sql_layer
from .migrations import init_migrations


@click.group()
def main():
    pass


@main.command("doctor")
@click.option("--url", required=True)
def doctor(url: str):
    config = DatabaseConfig(url=url)
    manager = EngineManager(config)
    click.echo(json.dumps(inspect_sql_layer(manager), ensure_ascii=False))


@main.command("inspect")
@click.option("--url", required=True)
def inspect_cmd(url: str):
    config = DatabaseConfig(url=url)
    manager = EngineManager(config)
    click.echo(json.dumps(inspect_sql_layer(manager), ensure_ascii=False))


@main.group("migrate")
def migrate():
    pass


@migrate.command("init")
@click.option("--dir", "target_dir", default="migrations")
def migrate_init(target_dir: str):
    root = init_migrations(target_dir=target_dir)
    click.echo(str(root))


@main.group("generate")
def generate():
    pass


@generate.command("resource")
@click.argument("name")
@click.option("--sql", is_flag=True, default=False)
def generate_resource(name: str, sql: bool):
    root = Path("generated")
    root.mkdir(exist_ok=True)
    target = root / f"{name}.py"
    content = f"class {name.title().replace('_', '')}Resource:\n    sql_enabled = {sql}\n"
    target.write_text(content, encoding="utf-8")
    click.echo(str(target))
