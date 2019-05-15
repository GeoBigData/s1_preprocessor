from __future__ import absolute_import
import os
import json
from s1_preprocessor import compile_archive
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
    aws_access_key_id = inputs.get('aws_access_key_id', None)
    aws_secret_access_key = inputs.get('aws_secret_access_key', None)
    aws_session_token = inputs.get('aws_session_token', None)

    # make sure image_id was specified
    if image_id is None:
        raise ValueError("image_id was not specified")

    # convert the inputs to the correct dtypes
    image_id = convert_type(image_id, str, 'String')
    aws_access_key_id = convert_type(aws_access_key_id, str, 'String')
    aws_secret_access_key = convert_type(aws_secret_access_key, str, 'String')
    aws_session_token = convert_type(aws_session_token, str, 'String')

    # run the processing
    compile_archive.main([image_id,
                          out_path,
                          '-K', aws_access_key_id,
                          '-S', aws_secret_access_key,
                          '-T', aws_session_token])


if __name__ == '__main__':
    main()
