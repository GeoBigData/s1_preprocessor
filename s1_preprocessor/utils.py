import os
import sh
import glob
import shutil
import sys


def image_info(image_id):
    """Parses image ID into various parts needed for formatting filenames"""

    info = {
        'image_id'         : image_id,
        'satellite': image_id.split('_')[0],
        'year'             : int(image_id.split('_')[4][0:4]),
        'month'            : int(image_id.split('_')[4][4:6]),
        'start_day'              : int(image_id.split('_')[4][6:8]),
        'end_day'                : int(image_id.split('_')[5][6:8]),
        'start_hour'             : int(image_id.split('_')[4].split('T')[1][0:2]),
        'start_minute'           : int(image_id.split('_')[4].split('T')[1][2:4]),
        'start_second'           : int(image_id.split('_')[4].split('T')[1][4:6]),
        'end_hour'               : int(image_id.split('_')[5].split('T')[1][0:2]),
        'end_minute'             : int(image_id.split('_')[5].split('T')[1][2:4]),
        'end_second'             : int(image_id.split('_')[5].split('T')[1][4:6]),
        'beam_mode'        : image_id.split('_')[1],
        'beam_mode_lower'  : image_id.split('_')[1].lower(),
        'polarization_mode': image_id.split('_')[3][2:4],
        'product_id6': image_id.split('_')[6],
        'product_id7': image_id.split('_')[7],
        'product_id9': image_id.split('_')[8]
    }

    return info


def format_s3_prefix(image_id):
    """Formats the path to the image on S3 based on the image ID"""

    path = 'GRD/{year}/{month}/{start_day}/{beam_mode}/{polarization_mode}/{image_id}'.format(**image_info(image_id))

    return path

def download_s1_image(image_id, out_folder, dry_run=False):
    """Downloads the image directory from AWS """

    src_bucket = 'sentinel-s1-l1c'
    src_prefix = format_s3_prefix(image_id)
    s3_path = os.path.join('s3://', src_bucket, src_prefix)
    out_path = os.path.join(out_folder, '{}.SAFE'.format(image_id))
    args = [s3_path,
            out_path,
            '--request-payer',
            'requester',
            '--recursive']
    if dry_run is True:
        args.append('--dryrun')

    # don't run the command if in debug mode -- it fails in pycharm for some reason
    if sys.gettrace() is None:
        sh.aws.s3.cp(*args)
    else:
        print("In debug mode. Skipping sh command.")

    return out_path


def format_filename(filename, image_id, extension, prefix=None):
    """Reformat filenames from the AWS S3 pattern to the format required for SAFE"""

    info = image_info(image_id)
    info['polarization'] = os.path.splitext(filename)[0].split('-')[-1]
    info['extension'] = extension
    if info['polarization'] in ['hh', 'vh']:
        # TODO this might need to be checked
        info['number'] = '001'
    else:
        info['number'] = '002'
    formatted = '{satellite}-{beam_mode}-grd-{polarization}-' \
                '{year}{month:02d}{start_day:02d}t{start_hour:02d}{start_minute:02d}{start_second:02d}-' \
                '{year}{month:02d}{end_day:02d}t{end_hour:02d}{end_minute:02d}{end_second:02d}-' \
                '{product_id6}-{product_id7}-{number}.{extension}'.format(**info).lower()
    if prefix is not None:
        formatted = '{prefix}{formatted}'.format(formatted=formatted,
                                                 prefix=prefix)

    return formatted


def rename_files(image_id, dir, ext, prefix=None):
    """Wrapper to handle renaming files from AWS S3 pattern to SAFE format"""

    # rename the measurement files
    if prefix is None:
        search_pattern = '*.{ext}'.format(ext=ext)
    else:
        search_pattern = '{prefix}*.{ext}'.format(prefix=prefix,
                                                  ext=ext)
    for f in glob.glob1(dir, search_pattern):
        new_name = format_filename(f, image_id, extension=ext, prefix=prefix)
        shutil.move(os.path.join(dir, f), os.path.join(dir, new_name))


