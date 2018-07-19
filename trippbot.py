from trippbot import ingester, bot
import click


@click.command()
@click.option("--ingest", is_flag=True)
@click.option("--interval", default=4, help="The script is invoked once an hour, so only tweet "
              "if the current hour (UTC) divides exactly by this number.",
              type=click.IntRange(1, 24))
@click.option("--force", is_flag=True)
def cli(ingest, interval, force):
    if ingest:
        ingester.run()
    else:
        bot.run(interval, force)


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
