import os
import sh
import click
from s1_preprocessor import utils


@click.command()
@click.argument('image_id')
@click.argument('out_path')
@click.option('--aws_access_key_id', '-K', required=False, type=str, default=None,
              help="If provided, AWS_ACCESS_KEY_ID environment variable will be set at runtime.")
@click.option('--aws_secret_access_key', '-S', required=False, type=str, default=None,
              help="If provided, AWS_SECRET_ACCESS_KEY environment variable will be set at runtime.")
@click.option('--aws_session_token', '-T', required=False, type=str, default=None,
              help="If provided, AWS_SESSION_TOKEN environment variable will be set at runtime.")
def main(image_id, out_path, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None):
    """Download data from AWS open data S3 and convert into SAFE format compatible with SNAP and PyroSAR"""


    print("Downloading files from S3")
    archive = utils.download_s1_image(image_id,
                                      out_path,
                                      dry_run=False,
                                      aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      aws_session_token=aws_session_token)

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
    sh.zip('-rm', archive.replace('.SAFE', '.zip'), os.path.basename(archive), '-4', _cwd=os.path.dirname(archive))

    print("Process completed successfully.")

if __name__ == '__main__':
    main()
