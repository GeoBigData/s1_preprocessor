import os
import gbdxtools
import boto3
gbdx = gbdxtools.Interface()


image_id = 'S1A_IW_GRDH_1SDV_20190313T161522_20190313T161557_026321_02F156_A8A9'

sts = boto3.client('sts',
                   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
temp_creds = sts.get_session_token()['Credentials']


compile_archive_task = gbdx.Task('s1_compile_archive:0.0.1',
                                 image_id=image_id,
                                 aws_access_key_id=temp_creds['AccessKeyId'],
                                 aws_secret_access_key=temp_creds['SecretAccessKey'],
                                 aws_session_token=temp_creds['SessionToken'])

geocode_task = gbdx.Task('s1_geocode:0.0.1',
                         data=compile_archive_task.outputs.data.value,
                         polarization='VV',
                         scaling='db',
                         bbox='34.523478,-19.504881,34.713695,-19.653439')

tasks = [compile_archive_task,
         geocode_task]

workflow = gbdx.Workflow(tasks)
workflow.savedata(compile_archive_task.outputs.data, location='mgleason/s1_preprocessor_testing/compile_archive')
workflow.savedata(geocode_task.outputs.data, location='mgleason/s1_preprocessor_testing/geocode')
workflow.execute()

print(workflow.id)

