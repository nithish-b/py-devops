import logging
import click
from .checker import check_urls

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


@click.command
@click.argument("urls", nargs=-1)
@click.option("--timeout", default=5, help="Timeout in seconds")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbosity")
def main(urls, timeout, verbose):
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    logger.debug(f"Recievd urls: {urls}")
    logger.debug(f"Recievd urls: {timeout}")
    logger.debug(f"Recievd urls: {verbose}")
    if not urls:
        logging.warning("No URLs provided to check")
        click.echo("Usage: check-urls <URL1> <URL2>")
    logger.info(f"Starting check for {len(urls)} URLs")

    results = check_urls(urls, timeout)
    click.echo("\n---- Results ---")
    for url, status in results.items():
        if "OK" in status:
            fg_color = "green"
        else:
            fg_color = "red"
        click.secho(f"{url:<40} -> {status}", fg=fg_color)
