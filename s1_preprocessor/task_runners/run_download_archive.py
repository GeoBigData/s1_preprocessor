from __future__ import absolute_import
import os
import json
from s1_preprocessor import download_archive
from s1_preprocessor.utils import convert_type


def main():

    # get the inputs
    string_ports = '/mnt/work/input/ports.json'

    # create output directory
    out_path = '/mnt/work/output/data'
    if os.path.exists(out_path) is False:
        os.makedirs(out_path)

    # read the inputs
    with open(string_ports) as ports:
        inputs = json.load(ports)
    image_id = inputs.get('image_id', None)
    username = inputs.get('username', None)
    password = inputs.get('password', None)

    # make sure image_id was specified
    if image_id is None:
        raise ValueError("image_id was not specified")
    if username is None:
        raise ValueError("username was not specified")
    if password is None:
        raise ValueError("password was not specified")

    # convert the inputs to the correct dtypes
    image_id = convert_type(image_id, str, 'String')
    username = convert_type(username, str, 'String')
    password = convert_type(password, str, 'String')

    # run the processing
    download_archive.main([image_id,
                           out_path,
                           '-U', username,
                           '-P', password])


if __name__ == '__main__':
    main()
