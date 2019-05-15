import os
import click
import pyroSAR
from pyroSAR.snap import geocode
import spatialist
from shapely.geometry import box
import utm


@click.command()
@click.argument('s1_archive')
@click.argument('out_path')
@click.option('--t_srs', required=False, type=str, default='utm',
              help="A target geographic reference system in WKT, EPSG, PROJ4 or OPENGIS format. "
                   "If EPSG, specify like: '4326'."
                   "Use 'utm' to automatically select UTM zone. Default: 'utm'")
@click.option('--tr', required=False, type=float, default=10,
              help="The target resolution in meters. Default: 10")
@click.option('--polarization', required=False, type=str, default='all',
              help="The polarizations to be processed. "
                   "Must be one of: {'VV', 'HH', 'VH', 'HV', 'all'}. Default: 'all'")
@click.option('--bbox', required=False, type=str, default=None,
              help="Bbox for subsetting the scene, provided as a comma-delimited string in EPGS:4326 coordinates. "
                   "e.g.: xmin,ymin,xmax,ymax."
                   "Default: None.")
@click.option('--shapefile', required=False, type=str, default=None,
              help="Path to a polygon shapefile for subsetting the scene to a test site. "
                   "This variable is overridden if a bbox is provided."
                   "Default: None.")
@click.option('--scaling', required=False, type=str, default='db',
              help="Should the output be in 'linear' or decibel ('db') scaling? Default: 'db'.")
@click.option('--geocoding_type', required=False, type=str, default='Range-Doppler',
              help="The type of geocoding applied; "
                   "can be either 'Range-Doppler' or 'SAR simulation cross correlation'. Default: 'Range-Doppler'.")
@click.option('--remove_s1_border_noise', required=False, type=bool, default=True,
              help="Enables removal of S1 GRD border noise. Default: True.")
@click.option('--remove_s1_thermal_noise', required=False, type=bool, default=False,
              help="Enables removal of S1 thermal noise. "
                   "Enabling may cause failures due to S1 format changes. Default: False.")
@click.option('--offset_left', required=False, type=int, default=None,
              help="Offset from left edge in pixels. "
                   "This variable is overridden if a shapefile or bbox is defined. Default: None")
@click.option('--offset_right', required=False, type=int, default=None,
              help="Offset from right edge in pixels. "
                   "This variable is overridden if a shapefile or bbox is defined. Default: None")
@click.option('--offset_top', required=False, type=int, default=None,
              help="Offset from top edge in pixels. "
                   "This variable is overridden if a shapefile or bbox is defined. Default: None")
@click.option('--offset_bottom', required=False, type=int, default=None,
              help="Offset from bottom edge in pixels. "
                   "This variable is overridden if a shapefile or bbox is defined. Default: None")
@click.option('--external_dem_file', required=False, type=str, default=None,
              help="The absolute path to an external DEM file. Default: None")
@click.option('--external_dem_no_data_value', required=False, type=float, default=None,
              help="The no data value of the external DEM. If not specified, the function will try to read it from the"
                   "specified external DEM. Default: None")
@click.option('--external_dem_apply_egm', required=False, type=bool, default=True,
              help="Apply Earth Gravitational Model to external DEM? Default: True.")
@click.option('--terrain_flattening', required=False, type=bool, default=True,
              help="Apply topographic normalization on the data? Default: True.")
@click.option('--basename_extension', required=False, type=str, default=None,
              help="Name of additional parameters to append to the basename, e.g. 'orbitNumber_rel'")
@click.option('--test', required=False, type=bool, default=False,
              help="If set to True the workflow xml file is only written and not executed. Default: False.")
@click.option('--export_extra', required=False, type=str, default=None,
              help="A list of image file IDs to be exported to outdir. The following IDs are currently supported:"
                   "incidenceAngleFromEllipsoid, localIncidenceAngle, projectedLocalIncidenceAngle, DEM."
                   "Should be specified as comma delimited string. Default: None")
@click.option('--group_size', required=False, type=int, default=2,
              help="The number of workers executed together in one gpt call. Default: 2")
@click.option('--cleanup', required=False, type=bool, default=True,
              help="Should all files written to the temporary directory during function "
                   "execution be deleted after processing? Default: True")
@click.option('--return_wf', required=False, type=bool, default=True,
              help="Should all files written to the temporary directory during function "
                   "Return the full name of the written workflow XML file?? Default: False")
def main(s1_archive, out_path, t_srs='utm', tr=10, polarization='all', bbox=None, shapefile=None, scaling='db',
         geocoding_type='Range-Doppler', remove_s1_border_noise=True, remove_s1_thermal_noise=False, offset_left=None,
         offset_right=None, offset_top=None, offset_bottom=None, external_dem_file=None, external_dem_no_data_value=None,
         external_dem_apply_egm=True, terrain_flattening=True, basename_extension=None, test=False, export_extra=None,
         group_size=2, cleanup=True, return_wf=False):

        # identify the scene from input archive
        print("Identifying S1 scene from input archive.")
        scene = pyroSAR.identify(s1_archive)
        print("Success")

        # deal with offsets
        offset = (offset_left, offset_right, offset_top, offset_bottom)
        if set(offset) == set([None]):
                offset = None

        if t_srs.lower() == 'utm':
                # get the bbox
                scene_extent = scene.bbox().extent
                scene_bbox = box(scene_extent['xmin'], scene_extent['ymin'], scene_extent['xmax'], scene_extent['ymax'])
                # get the lat and long from the aoi centroid
                long = scene_bbox.centroid.x
                lat = scene_bbox.centroid.y

                # use the longitude to get the utm zone (3rd element in returned list
                c = utm.from_latlon(lat, long)
                utm_zone = c[2]

                # build the epsg code
                if lat >= 0.0:
                        t_srs = int("326%s" % (str(utm_zone)))
                else:
                        t_srs = int("327%s" % (str(utm_zone)))
        else:
                # try to convert to an integer -- if it doesn't work, leave as is
                try:

                        t_srs = int(t_srs)
                except ValueError:
                        pass

        # deal with basename extensions
        if basename_extension is None:
                basename_extensions = None
        else:
                basename_extensions = [basename_extension]

        # deal with export_extra
        if export_extra is not None:
                export_extra = list(map(str, export_extra.split(',')))

        # make the output directory if it doesn't exist
        if os.path.exists(out_path) is False:
                os.mkdir(out_path)

        # if bbox is provided, convert to format expected by pyroSAR
        if bbox is not None:
                bbox = map(float, bbox.split(','))
                shapefile = spatialist.bbox(dict(zip(['xmin', 'ymin', 'xmax', 'ymax'], bbox)),
                                            crs=spatialist.auxil.crsConvert(4326, 'epsg'))

        print("Geocoding image according to input options.")
        geocode(infile=scene,
                outdir=out_path,
                t_srs=t_srs,
                tr=tr,
                polarizations=[polarization],
                shapefile=shapefile,
                scaling=scaling,
                geocoding_type=geocoding_type,
                removeS1BoderNoise=remove_s1_border_noise,
                removeS1ThermalNoise=remove_s1_thermal_noise,
                offset=offset,
                externalDEMFile=external_dem_file,
                externalDEMNoDataValue=external_dem_no_data_value,
                externalDEMApplyEGM=external_dem_apply_egm,
                terrainFlattening=terrain_flattening,
                basename_extensions=basename_extensions,
                test=test,
                export_extra=export_extra,
                groupsize=group_size,
                cleanup=cleanup,
                returnWF=return_wf
                )
        print("Processing completed successfully.")


if __name__ == '__main__':
        main()


