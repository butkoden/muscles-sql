import json
from pathlib import Path

import click

from .config import DatabaseConfig
from .providers import SqlGenerationRequest, SqlResourceGeneratorProvider


@click.group()
def main():
    pass


@main.command("doctor")
@click.option("--url", required=True)
def doctor(url: str):
    from .engine import EngineManager
    from .inspect import inspect_sql_layer

    config = DatabaseConfig(url=url)
    manager = EngineManager(config)
    click.echo(json.dumps(inspect_sql_layer(manager), ensure_ascii=False))


@main.command("inspect")
@click.option("--url", required=True)
def inspect_cmd(url: str):
    from .engine import EngineManager
    from .inspect import inspect_sql_layer

    config = DatabaseConfig(url=url)
    manager = EngineManager(config)
    click.echo(json.dumps(inspect_sql_layer(manager), ensure_ascii=False))


@main.group("migrate")
def migrate():
    pass


@migrate.command("init")
@click.option("--dir", "target_dir", default="migrations")
def migrate_init(target_dir: str):
    from .migrations import init_migrations

    root = init_migrations(target_dir=target_dir)
    click.echo(str(root))


@migrate.command("revision")
@click.option("--dir", "target_dir", default="migrations")
@click.option("--message", default="revision")
@click.option("--autogenerate", is_flag=True, default=False)
@click.option("--url", default=None)
def migrate_revision(target_dir: str, message: str, autogenerate: bool, url: str | None):
    from .migrations import revision

    revision(message=message, target_dir=target_dir, autogenerate=autogenerate, url=url)
    click.echo("ok")


@migrate.command("upgrade")
@click.option("--dir", "target_dir", default="migrations")
@click.option("--rev", default="head")
@click.option("--url", default=None)
def migrate_upgrade(target_dir: str, rev: str, url: str | None):
    from .migrations import upgrade

    upgrade(rev=rev, target_dir=target_dir, url=url)
    click.echo("ok")


@migrate.command("downgrade")
@click.option("--dir", "target_dir", default="migrations")
@click.option("--rev", default="-1")
@click.option("--url", default=None)
def migrate_downgrade(target_dir: str, rev: str, url: str | None):
    from .migrations import downgrade

    downgrade(rev=rev, target_dir=target_dir, url=url)
    click.echo("ok")


@migrate.command("history")
@click.option("--dir", "target_dir", default="migrations")
@click.option("--url", default=None)
def migrate_history(target_dir: str, url: str | None):
    from .migrations import history

    history(target_dir=target_dir, url=url)
    click.echo("ok")


@migrate.command("current")
@click.option("--dir", "target_dir", default="migrations")
@click.option("--url", default=None)
def migrate_current(target_dir: str, url: str | None):
    from .migrations import current

    current(target_dir=target_dir, url=url)
    click.echo("ok")


@main.group("generate")
def generate():
    pass


@generate.command("resource")
@click.argument("name")
@click.option("--sql", is_flag=True, default=False)
def generate_resource(name: str, sql: bool):
    if sql:
        provider = SqlResourceGeneratorProvider()
        generated = provider.generate(
            project_root=Path.cwd(),
            request=SqlGenerationRequest(
                generator_type="sql-resource",
                name=name,
                force=False,
                with_tests=False,
            ),
        )
        click.echo(generated[0])
        return

    root = Path("generated")
    root.mkdir(exist_ok=True)
    target = root / f"{name}.py"
    content = f"class {name.title().replace('_', '')}Resource:\n    sql_enabled = {sql}\n"
    target.write_text(content, encoding="utf-8")
    click.echo(str(target))


if __name__ == "__main__":
    main()
