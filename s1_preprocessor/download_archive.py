import os
import click
from sentinelsat import SentinelAPI

@click.command()
@click.argument('image_id')
@click.argument('out_path')
@click.option('--username', '-U', required=True, type=str, default=None,
              help="Copernicus SciHub username to use for authenticating download.")
@click.option('--password', '-P', required=True, type=str, default=None,
              help="Copernicus SciHub password to use for authenticating download.")
def main(image_id, out_path, username, password):
    """Download data from Copernicus Scihub"""

    # check that the output path exists
    if os.path.exists(out_path) is False:
        raise FileExistsError("out_path {} does not exist".format(out_path))

    # connect to the api
    api = SentinelAPI(username, password)

    print("Identifying UUID of image ID {}".format(image_id))
    products = api.query(filename='{}.SAFE'.format(image_id))
    if len(products) == 0:
        raise ValueError("Could not identify product with the input image ID.")
    elif len(products) > 1:
        raise ValueError("Unexpected result: identified multiple products with the input image ID.")
    product_id = list(products.keys())[0]

    print("Downloading archive from Scihub")
    api.download_all([product_id],
                     directory_path=out_path)

    print("Process completed successfully.")


if __name__ == '__main__':
    main()
