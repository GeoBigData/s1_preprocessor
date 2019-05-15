import os
import sh
import click
from s1_preprocessor import utils


@click.command()
@click.argument('image_id')
@click.argument('out_path')
def main(image_id, out_path):
    """Download data from AWS open data S3 and convert into SAFE format compatible with SNAP and PyroSAR"""

    print("Downloading files from S3")
    archive = utils.download_s1_image(image_id, out_path, dry_run=False)

    # rename the files
    print("Renaming files")
    utils.rename_files(image_id, dir=os.path.join(archive, 'measurement'), ext='tiff',
                       prefix=None)
    utils.rename_files(image_id, dir=os.path.join(archive, 'annotation'), ext='xml',
                       prefix=None)
    utils.rename_files(image_id, dir=os.path.join(archive, 'annotation', 'calibration'), ext='xml',
                       prefix='noise-')
    utils.rename_files(image_id, dir=os.path.join(archive, 'annotation', 'calibration'), ext='xml',
                       prefix='calibration-')

    # zip it all up
    print("Zipping up SAFE archive")
    # use sh to do this because the shutil.make_archive() function doesn't seem to work with SNAP
    sh.zip('-r', archive.replace('.SAFE', '.zip'), os.path.basename(archive), '-4', _cwd=os.path.dirname(archive))

    print("Process completed successfully.")

if __name__ == '__main__':
    main()
