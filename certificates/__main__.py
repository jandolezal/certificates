import click

from certificates.iscc import scrape_iscc
from certificates.kzr import scrape_kzr


@click.command()
@click.option(
    '--scheme',
    default='all',
    type=click.Choice(['all', 'iscc', 'kzr'], case_sensitive=False),
    help='Choose voluntary scheme to scrape (default: all)',
)
def main(scheme):
    """Scrape bioenergy sustainability certificates."""
    if scheme == 'all':
        scrape_iscc()
        scrape_kzr()
    elif scheme == 'iscc':
        scrape_iscc()
    elif scheme == 'kzr':
        scrape_kzr()


main()
