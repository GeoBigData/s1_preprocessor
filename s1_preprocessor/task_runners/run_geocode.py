from __future__ import absolute_import
import os
import json
import glob
from s1_preprocessor import geocode
from s1_preprocessor.utils import convert_type


def main():

    # get the inputs
    string_ports = '/mnt/work/input/ports.json'
    input_data = '/mnt/work/input/data'

    # create output directory
    out_path = '/mnt/work/output/data'
    if os.path.exists(out_path) is False:
        os.makedirs(out_path)

    # read the inputs
    with open(string_ports) as ports:
        inputs = json.load(ports)
    t_srs = inputs.get('t_srs', 'utm')
    tr = inputs.get('tr', 10)
    polarization = inputs.get('polarization', 'all')
    bbox = inputs.get('bbox', None)
    shapefile = inputs.get('shapefile', None)
    scaling = inputs.get('scaling', 'db')
    geocoding_type = inputs.get('geocoding_type', 'Range-Doppler')
    remove_s1_border_noise = inputs.get('remove_s1_border_noise', True)
    remove_s1_thermal_noise = inputs.get('remove_s1_thermal_noise', False)
    offset_left = inputs.get('offset_left', None)
    offset_right = inputs.get('offset_right', None)
    offset_top = inputs.get('offset_top', None)
    offset_bottom = inputs.get('offset_bottom', None)
    external_dem_file = inputs.get('external_dem_file', None)
    external_dem_no_data_value = inputs.get('external_dem_no_data_value', None)
    external_dem_apply_egm = inputs.get('external_dem_apply_egm', True)
    terrain_flattening = inputs.get('terrain_flattening', True)
    basename_extension = inputs.get('basename_extension', None)
    test = inputs.get('test', False)
    export_extra = inputs.get('export_extra', None)
    group_size = inputs.get('group_size', 2)
    cleanup = inputs.get('cleanup', True)
    return_wf = inputs.get('return_wf', True)

    # convert the inputs to the correct dtypes
    t_srs = convert_type(t_srs, str, 'String')
    tr = convert_type(tr, float, 'Float')
    polarization = convert_type(polarization, str, 'String')
    bbox = convert_type(bbox, str, 'String')
    shapefile = convert_type(shapefile, str, 'String')
    scaling = convert_type(scaling, str, 'String')
    geocoding_type = convert_type(geocoding_type, str, 'String')
    remove_s1_border_noise = convert_type(remove_s1_border_noise, bool, 'Boolean')
    remove_s1_thermal_noise = convert_type(remove_s1_thermal_noise, bool, 'Boolean')
    offset_left = convert_type(offset_left, int, 'Integer')
    offset_right = convert_type(offset_right, int, 'Integer')
    offset_top = convert_type(offset_top, int, 'Integer')
    offset_bottom = convert_type(offset_bottom, int, 'Integer')
    external_dem_file = convert_type(external_dem_file, str, 'String')
    external_dem_no_data_value = convert_type(external_dem_no_data_value, float, 'Float')
    external_dem_apply_egm = convert_type(external_dem_apply_egm, bool, 'Boolean')
    terrain_flattening = convert_type(terrain_flattening, bool, 'Boolean')
    basename_extension = convert_type(basename_extension, str, 'String')
    test = convert_type(test, bool, 'Boolean')
    export_extra = convert_type(export_extra, str, 'String')
    group_size = convert_type(group_size, int, 'Integer')
    cleanup = convert_type(cleanup, bool, 'Boolean')
    return_wf = convert_type(return_wf, bool, 'Boolean')

    # get the SAFE file in the input folder
    zips = glob.glob1(input_data, '*.zip')
    if len(zips) == 0:
        raise ValueError("No zips found in input data port")
    if len(zips) > 1:
        raise ValueError("Multiple zips found in input data port")
    in_SAFE = os.path.join(input_data, zips[0])


    # run the processing
    geocode.main([in_SAFE,
                  out_path,
                  '--t_srs', t_srs,
                  '--tr', tr,
                  '--polarization', polarization,
                  '--bbox', bbox,
                  '--shapefile', shapefile,
                  '--scaling', scaling,
                  '--geocoding_type', geocoding_type,
                  '--remove_s1_border_noise', remove_s1_border_noise,
                  '--remove_s1_thermal_noise', remove_s1_thermal_noise,
                  '--offset_left', offset_left,
                  '--offset_right', offset_right,
                  '--offset_top', offset_top,
                  '--offset_bottom', offset_bottom,
                  '--external_dem_file', external_dem_file,
                  '--external_dem_no_data_value', external_dem_no_data_value,
                  '--external_dem_apply_egm', external_dem_apply_egm,
                  '--terrain_flattening', terrain_flattening,
                  '--basename_extension', basename_extension,
                  '--test', test,
                  '--export_extra', export_extra,
                  '--group_size', group_size,
                  '--cleanup', cleanup,
                  '--return_wf', return_wf
                  ])


if __name__ == '__main__':
    main()
